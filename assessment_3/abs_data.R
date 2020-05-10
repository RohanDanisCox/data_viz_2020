library(raustats)
library(tidyverse)
library(ggplot2)

### Let's assume Housing Finance is where I want to enquire. What are the interesting parts to it:

abs_dimensions('HF')

housing_finance <- abs_stats(dataset = 'HF',filter = 'all', start_date = '2018-11')

write_csv(housing_finance,'test.csv')

housing_finance <- abs_stats(dataset = 'HF',filter = list(DT = 5, ITEM = "140_1") , start_date = '2018-11')

abs_search("Total new housing", dataset="HF", code_only=TRUE)

abs_search("Average Loan", dataset="HF", code_only=TRUE)

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
       
       
       