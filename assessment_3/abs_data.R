library(raustats)
library(tidyverse)
library(ggplot2)
library(stringr)

### Let's assume Housing Finance is where I want to enquire. What are the interesting parts to it:

abs_dimensions('HF')

housing_finance <- abs_stats(dataset = 'HF',filter = 'all', start_date = '2018-11')

write_csv(housing_finance,'test.csv')

housing_finance <- abs_stats(dataset = 'HF',filter = list(DT = 5, ITEM = "140_1") , start_date = '2018-11')

abs_search("Total new housing", dataset="HF", code_only=TRUE)

abs_search("Average Loan", dataset="HF", code_only=TRUE)


### The ABS Stats API is incredible, but won't work for this purpose as Housing Finance was replaced with different metrics
### maybe one day they will be incorporated. But for now I will need to use the catalogs

owner_occupiers <- abs_cat_stats("5601.0", tables = c("24"), releases = "Feb 2020")

investors <- abs_cat_stats("5601.0", tables = c("25"), releases = "Feb 2020")

owner_occupiers_2 <- owner_occupiers %>%
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

names(owner_occupiers_2)

selection <- owner_occupiers_2 %>%
  select(date,region,series_type,metric,value) 

new_loan_commitments <- selection %>%
  pivot_wider(names_from = metric, values_from = value)

write_csv(new_loan_commitments,"new_loan_commitments.csv")

owner_occupiers_2 %>%
  count(series_type)

owner_occupiers_2 %>%
  count(metric) 

value <- owner_occupiers_2 %>%
  filter(metric == "Value") %>%
  filter(region == "Total Australia")

ggplot(value,aes(date,value, colour = series_type,group = series_type)) + 
  geom_line()

number <- owner_occupiers_2 %>%
  filter(metric == "Number") %>%
  filter(region == "Total Australia")

ggplot(number,aes(date,value, colour = series_type,group = series_type)) + 
  geom_line()

nsw_value <- owner_occupiers_2 %>%
  filter(metric == "Value") %>%
  filter(region == "New South Wales")

ggplot(nsw_value,aes(date,value, colour = series_type,group = series_type)) + 
  geom_line

qld_value <- owner_occupiers_2 %>%
  filter(metric == "Value") %>%
  filter(region == "Queensland")

ggplot(qld_value,aes(date,value, colour = series_type,group = series_type)) + 
  geom_line()

all <- owner_occupiers_2 %>%
  filter(metric == "Value") %>%
  filter(series_type == "Seasonally Adjusted")

ggplot(all,aes(date,value, colour = region,group = region)) + 
  geom_line()

owner_occupier_total_housing <- abs_cat_stats("5601.0", tables = c("4"), releases = "Feb 2020")


?abs_cat_stats

Total new housing commitments

?abs_stats

names(housing_finance)

measures <- housing_finance %>%
  filter(!is.na(values)) %>%
  count(measure, data_item)

# What is going on with average loan size?

avg_loan <- housing_finance %>%
  filter(!is.na(values)) %>%
  filter(measure == "Average Loan Size ($ '000)")

seasonally_adjusted <- avg_loan %>%
  filter(adjustment_type == "Seasonally Adjusted")



cachelist <- abs_cachelist
rba_cache <- rba_table_cache()

rba_e2 <- rba_stats(table_no = "E2")
rba_d10 <- rba_stats(table_no = "D10")

datasets <- abs_datasets()

search <- abs_search("housing")

?raustats

lending_indicators <- abs_cat_stats("6416.0")

lending_indcators %>%
  distinct(data_item_description)

test <- separate(lending_indicators,data_item_description, into = c("A","B","C","D","E","F","G", "H", "I"),sep = "; ")

abs_cat_releases("5601.0")

?abs_cat_stats

housing_finance <- abs_stats(dataset = 'HF',filter = 'all', start_date = '2018-11')

lending_finance <- abs_stats(dataset = 'LENDING_BY_PURPOSE',filter = 'all', start_date = '2018-11')

lending_finance <- abs_stats(dataset = 'LENDING_FINANCE_SUMMARY',filter = 'all', start_date = '2018-11')

lending_finance %>%
  distinct(finance_type)

lending_finance %>%
  distinct(measure)

lending_finance %>%
  distinct(lender)

lending_finance %>%
  distinct(time)

qbis <- abs_stats(dataset = 'QBIS',filter = 'all', start_date = '2018-11')


LENDING_FINANCE_SUMMARY

na_removed <- housing_finance %>%
  filter(!is.na(values))

na_removed %>% 
  distinct(measure)

na_removed %>%
  distinct(data_item)

housing_finance <- abs_stats(dataset = 'HF',filter = 'all', start_date = '2018-10')

value <- housing_finance %>%
  filter(measure == "Value of Commitments ($ '000)") %>%
  filter(data_item == "Total new housing commitments excluding refinancing") %>%
  filter(lender == "All Lenders")
  

ggplot(value, aes(x = time, y = values, colour = region, group = region)) + 
  geom_line()

value %>%
  distinct(data_item)
?abs_stats

avg_loan <- na_removed %>%
  filter(measure == "Average Loan Size ($ '000)")

names(avg_loan)

ggplot(avg_loan, aes(values, lender))+
  geom_point()
       
       
       