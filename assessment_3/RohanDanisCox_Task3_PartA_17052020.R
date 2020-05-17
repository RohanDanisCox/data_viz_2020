library(raustats)
library(tidyverse)
library(ggplot2)
library(stringr)

# Download Catalogue Table from ABS

fhb_raw <- abs_cat_stats("5601.0", tables = c("24"), releases = "Feb 2020")

fhb_raw_1 <- first_home_buyers_raw %>%
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

write_csv(fhb_new_loan_commitments,"fhb_new_loan_commitments.csv")