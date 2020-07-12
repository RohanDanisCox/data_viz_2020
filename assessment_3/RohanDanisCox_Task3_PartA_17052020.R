library(raustats)
library(tidyverse)
library(ggplot2)
library(stringr)
library(lubridate)
library(zoo)

# Download Catalogue Table from ABS

fhb_raw <- abs_cat_stats("5601.0", tables = c("24"), releases = "Feb 2020")

fhb_raw_1 <- fhb_raw %>%
  separate(data_item_description,
           into = c("households",
                    "housing_finance",
                    "owwner_occupier",
                    "first_home_buyers",
                    "region",
                    "new_loan_commitment",
                    "metric"),
           sep = " ;  ") %>%
  mutate(metric = str_remove(metric," ;"))

fhb_raw_2 <- fhb_raw_1 %>%
  select(date,region,series_type,metric,value) 

fhb_new_loan_commitments <- fhb_raw_2 %>%
  pivot_wider(names_from = metric, values_from = value)


# Max benefit from schemes

schemes_raw <- read_csv("first_home_schemes.csv") %>%
  mutate(start = dmy(start),
         end = dmy(end))

date_region <- fhb_new_loan_commitments %>%
  select(date,region) %>%
  filter(!region == "Total Australia") %>%
  distinct()

scheme_benefit <- date_region %>%
  left_join(schemes_raw, by = c("region" = "state")) %>%
  filter(date >= start & date <= end) %>%
  group_by(date,region) %>% 
  mutate(schemes = paste0(scheme," = ",max_benefit, collapse = ", ")) %>%
  ungroup() %>%
  group_by(date,region,type) %>%
  mutate(max_benefit_by_type = sum(max_benefit)) %>%
  ungroup() %>%
  select(-c(scheme,start,end)) %>%
  distinct() %>%
  group_by(date,region) %>%
  mutate(All = sum(max_benefit)) %>%
  select(-max_benefit) %>%
  distinct() %>%
  pivot_wider(names_from = type, values_from = max_benefit_by_type) %>%
  pivot_longer(4:8,names_to = "type", values_to = "max_benefit_available") %>%
  mutate(max_benefit_available = case_when(is.na(max_benefit_available) ~ 0,
                                           TRUE ~ max_benefit_available))

# Population

regions <- date_region %>% select(region) %>% distinct() %>% pull()

pop_raw <- abs_cat_stats("3101.0", tables = "4") %>%
  separate(data_item_description,
           into = c("estimated residential population",
                    "persons",
                    "region"),
           sep = " ;  ") %>%
  mutate(region = str_remove(region," ;"))

population <- pop_raw %>%
  filter(persons == "Persons") %>%
  filter(date >= min(fhb_new_loan_commitments$date)) %>%
  filter(region %in% regions) %>%
  select(date,region,persons = value) %>%
  right_join(date_region, by = c("date","region")) %>%
  group_by(region) %>%
  arrange(date) %>%
  mutate(persons = na.approx(persons, na.rm = FALSE)) %>%
  mutate(persons = case_when(date < dmy("01/09/2002") ~ min(persons, na.rm = TRUE),
                                date > dmy("01/09/2019") ~ max(persons, na.rm = TRUE),
                                TRUE ~ persons)) %>%
  ungroup() %>%
  mutate(persons = round(persons,0))

### Residential property prices

price_raw <- abs_cat_stats("6416.0", tables = "4") %>%
  separate(data_item_description,
           into = c("price",
                    "city"),
           sep = " ;  ") %>%
  mutate(city = str_remove(city," ;")) %>%
  filter(price == "Median Price of Established House Transfers (Unstratified)")


price <- price_raw %>%
  mutate(region = case_when(city == "Sydney" ~ "New South Wales",
                            city == "Melbourne" ~ "Victoria",
                            city == "Brisbane" ~ "Queensland",
                            city == "Adelaide" ~ "South Australia",
                            city == "Perth" ~ "Western Australia",
                            city == "Hobart" ~ "Tasmania",
                            city == "Darwin" ~ "Northern Territory",
                            city == "Canberra" ~ "Australian Capital Territory"),
         median_price_of_capital_city = value * 1000) %>%
  select(date,region,median_price_of_capital_city) %>%
  filter(!is.na(region)) %>%
  full_join(date_region, by = c("date","region")) %>%
  group_by(region) %>%
  arrange(date) %>%
  mutate(median_price_of_capital_city = round(na.approx(median_price_of_capital_city, na.rm = FALSE),0)) 

## Join up tables

data_raw <- fhb_new_loan_commitments %>%
  left_join(scheme_benefit, by = c("date", "region")) %>%
  left_join(population, by = c("date", "region")) %>%
  left_join(price, by = c("date", "region")) %>%
  filter(region != "Total Australia")

data <- data_raw %>%
  mutate(total_new_loan_commitments = Number,
         new_loan_commitments_per_100000 = Number / (persons/100000),
         value_in_millions = Value * 1000000,
         value_per_person = value_in_millions/persons,
         max_benefit_as_percent_median_house_price = max_benefit_available/median_price_of_capital_city) %>%
  select(date,region,series_type,type,schemes,total_new_loan_commitments,new_loan_commitments_per_100000,
         value_in_millions, value_per_person,max_benefit_available,max_benefit_as_percent_median_house_price)

data_2 <- data %>%
  mutate_at(vars(6:11),as.numeric) %>%
  pivot_longer(cols = 6:11) %>%
  mutate(facet = case_when(name %in% c("total_new_loan_commitments","new_loan_commitments_per_100000",
                                       "value_in_millions", "value_per_person") ~ "New Loan Commitment",
                           name %in% c("max_benefit_available","max_benefit_as_percent_median_house_price") ~ "Maximum Benefit"))


write_csv(data_2,"fhb_new_loan_commitments.csv")
