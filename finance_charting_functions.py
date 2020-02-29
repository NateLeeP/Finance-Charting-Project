# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 23:30:39 2020

@author: Nate P
"""
import datetime
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as Date
import numpy as np
def convert_to_epoch(date):
    """Converts date in mm/dd/yyyy format to an epoch that Yahoo Finance will understand. The time will be 19:00:00, which is the time for Yahoo Finance dates"""
    """Datetime.date creates a datetime Date object. The arguments are year, month, day """
    temp_date = datetime.date(int(date.split(r'/')[2]), int(date.split(r'/')[0]), int(date.split(r'/')[1]))
    temp_datetime = datetime.datetime.combine(temp_date, datetime.time(19))
    """Had to convert to int!! The earlier float was causing problems. Yahoo finance did not understand the float"""
    epoch = int(temp_datetime.timestamp())
    return epoch

def format_url(ticker, start_date, end_date):
    """Format the Yahoo Finance URL. Finance URL accepts dates in epochs. For now, url will be set to 'weeks'"""
    """Dates need to be in format of mm/dd/yyyy"""
    start_date_epoch = convert_to_epoch(start_date)
    end_date_epoch = convert_to_epoch(end_date)
    """Format URL after converting dates to epoch. Notice: Capturing weekly returns."""
    url = 'https://finance.yahoo.com/quote/{0}/history?period1={1}&period2={2}&interval=1wk&filter=history&frequency=1wk'.format(ticker, start_date_epoch, end_date_epoch)
    return url

def scrape_data(url):
    """GET requests using request library"""
    yahoo_finance_requests = requests.get(url).text
    """Parse request using beautiful Soup"""
    yahoo_finance_soup = bs(yahoo_finance_requests, features = 'html.parser')
    """Extract table data using list comprehension"""
    yahoo_finance_soup_table_data = [[td.text for td in tr.findAll('td')] for tr in yahoo_finance_soup.findAll('tr')[1:len(yahoo_finance_soup.findAll('tr')) -1]]
    yahoo_finance_soup_table_headers = [th.text for th in yahoo_finance_soup.findAll('tr')[0]]
    """Some rows contain only dividends. Need to remove these to build DataFrame properly. Below for loop deletes dividend rows """
    for row in yahoo_finance_soup_table_data:
        if 'Dividend' in row[1].split():
            yahoo_finance_soup_table_data.remove(row)
    
    yahoo_finance_df = pd.DataFrame(yahoo_finance_soup_table_data)
    yahoo_finance_df.columns = yahoo_finance_soup_table_headers
    """Function is useless without return!! You missed return statement """
    """Reversed df using iloc. Convenient, quick way. Should have used for Disney project"""
    yahoo_finance_df = yahoo_finance_df.iloc[::-1]
    yahoo_finance_df.index = range(len(yahoo_finance_df))
    
    return yahoo_finance_df

#appl_df = scrape_data(format_url('APPL','01/01/2019', '12/31/2019'))

#print(format_url('APPL','01/01/2019','12/31/2019'))

## May be preventing me from scraping. Not sure. Scrape worked earlier. Might have to hit apply??? Not something I can do via python. Revisit tomorrow.


#apple_df = scrape_data(format_url('TSLA','01/02/2019','12/31/2019'))

"""Success! However, dataframe is in reverse. I would prefer organized by earliest date to latest. How do we do this?
    FIXED!!! Simple, use iloc to index dataframe in reverse"""
    
"""NEXT STEPS: Sucessfully plot return over time. Will build function for this """
def convert_to_float(dollar_value):
    """Scraped finance data has columns formatted incorrectly. This function converts each data point in a series to a float (assuming the series CAN be converted to an int)"""
    dollar_value = float(dollar_value)
    return dollar_value

def percent_change(series):
    """Looking to compare % change (or growth) of two tickers. Comparing abosulte values is not helpful. Want to know how much each increased and decreased"""
    percent_change_series = []
    for i in series.index:
        if i == 0:
            percent_change_series.append(0)
        else:
            percent_change_series.append((series[i] - series[i-1]) / series[i-1])
    return percent_change_series
    
def generate_graph(date_series, value_series):
    """Function to generate graph for ticker. Function will take date series (the time interval chosen) and value series (percent_change)"""
    
    
    

def plot_ticker_graphs(start_date, end_date, ticker1, ticker2 = 'VFINX'):
    """ Compare two tickers. Default comparison ticker is the Vangaurd 500 index fund. Reason: Vanguard is familiar name in ETF space """
    ticker1_df = scrape_data(format_url(ticker1, start_date, end_date))
    ticker2_df = scrape_data(format_url(ticker2, start_date, end_date))
    
    ticker1_date = pd.to_datetime(ticker1_df['Date'])
    ticker1_value = np.cumsum(pd.Series(percent_change(ticker1_df['Close*'].apply(convert_to_float))) * 100)
    
    ticker2_date = pd.to_datetime(ticker2_df['Date'])
    ticker2_value = np.cumsum(pd.Series(percent_change(ticker2_df['Close*'].apply(convert_to_float))) * 100)
    
    
    fig, ax = plt.subplots()
    fig.set_size_inches(10,6)
    ax.plot(ticker1_date, ticker1_value, label = ticker1)
    ax.plot(ticker2_date, ticker2_value, label = ticker2)
    
    ax.set_xlim(Date.date2num(ticker1_date[0]), Date.date2num(ticker1_date[len(ticker1_date) -1]))
    ax.legend()
    fig.suptitle(ticker1 + ' vs ' + ticker2 + ' Performance', fontsize = 14, fontweight = 'bold')
    ax.set_title('Weekly returns from ' + month_dict[ticker1_date[0].month] + ' \'' + str(ticker1_date[0].year)[2:]
                + ' to ' + month_dict[ticker1_date[len(ticker1_date) - 1].month] + ' \'' + str(ticker1_date[len(ticker1_date) -1].year)[2:])
    ax.set_xlabel('Month', fontsize = 14)
    ax.set_ylabel('Cumulative Percent Change', fontsize = 14)
    ax.set_xticklabels([convert_date_to_string(x) for x in ax.get_xticks()])
    
    
    plt.show()


""" Practice graph creation (on apple_df) without constantly scraping """
""" Date and value """
def my_set_xtick_labels(xticklabels):
    """
    Parameter is a matplotlib tick label object
    Return a list with xticklabels. Helps make graph more reader friendly """
def convert_date_to_string(matplotlib_date):
    """Parameter is a datetime.date object, returns dates in form 'Month + 'year'"""
    
    datetime = Date.num2date(matplotlib_date)
    
    date_temp = month_dict[datetime.month] + ' \'' + str(datetime.year)[2:]
    
    return date_temp
month_dict = {1:'JAN', 2:'FEB',3:'MAR',4:'APRL', 5:'MAY',6:'JUN', 7:'JULY',8:'AUG',9:'SEPT',10:'OCT',11:'NOV',12:'DEC'}

#apple_ticker = 'AAPL'
"""
apple_date = pd.to_datetime(apple_df['Date'])
apple_value = np.cumsum(pd.Series(percent_change(apple_df['Close*'].apply(convert_to_float))) * 100)

fig, ax = plt.subplots()
fig.set_size_inches(15,6)
ax.plot(apple_date, apple_value, label = 'AAPL')

ax.set_xlim(Date.date2num(apple_date[0]), Date.date2num(apple_date[52]))
ax.legend()
ax.set_xticklabels([convert_date_to_string(x) for x in ax.get_xticks()])
"""# Stopping point. Getting close to finding a way to create monthly x tick labels using passed dates. A function could be necessary"""



















