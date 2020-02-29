# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 21:02:33 2020

@author: Nate P
"""
import pandas as pd
import requests
import datetime
from bs4 import BeautifulSoup as bs
"""
name = input('What is your name ')
print(name)

age = input('What is your age? ')
print(int(age))

song = input('What is your favorite song? ')
print(song)
"""
"""Will return to input issue. """

"""Function converting dates in the format 'mm/dd/yyyy' to epoch"""
date = '05/06/2011'
practice_date = datetime.datetime(int(date.split(r'/')[2]), int(date.split(r'/')[0]), int(date.split(r'/')[1]), 0, 0)

print(practice_date.timestamp())

### Epoch to datetime is show below

print(datetime.datetime.fromtimestamp(1581120000))
 
### Create 'time' part of datetime. In order to scrape from yahoo, need to convert dates into datetime set to 19:00:00 hours. Do so using code below.
print(datetime.time(19))

### Can I scrape yahoo finance data?

yahoo_finance_requests = requests.get('https://finance.yahoo.com/quote/AAPL/history?period1=1550113766&period2=1581649766&interval=1wk&filter=history&frequency=1wk').text
yahoo_finance_soup = bs(yahoo_finance_requests, features = 'html.parser')

yahoo_finance_soup_table_data = [[td.text for td in tr.findAll('td')] for tr in yahoo_finance_soup.findAll('tr')[1:len(yahoo_finance_soup.findAll('tr')) -1]]
yahoo_finance_soup_table_headers = [th.text for th in yahoo_finance_soup.findAll('tr')[0]]

for row in yahoo_finance_soup_table_data:
    if 'Dividend' in row[1].split():
        yahoo_finance_soup_table_data.remove(row)

yahoo_finance_df = pd.DataFrame(yahoo_finance_soup_table_data)
yahoo_finance_df.columns = yahoo_finance_soup_table_headers

### Lets make some functions