## Ryan Dufresne
## cQuant.io Coding Challenge
import pandas as pd
import numpy as np
import os
pd.options.mode.chained_assignment = None  # Needed this for issues with dataframe modification
import matplotlib.pyplot as plt


## Task 1 ## Read in + Combine price data
# Directory syntax
dir = os.getcwd()
output = (dir+'\\Output')

# Reading in data from csvs to prices dataframes
prices_16 = pd.read_csv(dir+'\\historicalPriceData\\ERCOT_DA_Prices_2016.csv')
prices_17 = pd.read_csv(dir+'\\historicalPriceData\\ERCOT_DA_Prices_2017.csv')
prices_18 = pd.read_csv(dir+'\\historicalPriceData\\ERCOT_DA_Prices_2018.csv')
prices_19 = pd.read_csv(dir+'\\historicalPriceData\\ERCOT_DA_Prices_2019.csv')

# Combine all into single dataframe
prices = pd.concat([prices_16, prices_17, prices_18, prices_19])
ogprices = prices #Non-modified form of dataframe for future use

## Task 2 ##
prices['YrMnth'] = pd.to_datetime(prices['Date']).dt.strftime('%m/%Y')
prices['Year'] = prices['YrMnth'].apply(lambda x: x.split('/')[1])
prices['Month'] = prices['YrMnth'].apply(lambda x: x.split('/')[0])
avgByMonth = prices.groupby(['SettlementPoint','Year','Month']).agg({'Price': 'mean'})
avgByMonth.rename(columns={'Price':'AveragePrice'}) # I'm not sure how to rename columns after grouping/aggregation.

## Task 3 ## write avgs to csv
avgByMonth.to_csv(output+'\\AveragePriceByMonth.csv')

## Task 4 ## 
hrVlty = prices[prices['SettlementPoint'].astype(str).str.startswith('HB')] # Keep only HB values
hrVlty = hrVlty[hrVlty['Price'] > 0] # Only prices above 0 to avoid divison by 0
hrVlty['HourlyVolatility'] = np.log(hrVlty['Price'])
volByHour = hrVlty.groupby(['SettlementPoint', 'Year']).agg({'HourlyVolatility': 'std'})

## Task 5 ## write hourly volatility to csv
volByHour.to_csv(output+'\\HourlyVolatilityByYear.csv')

## Task 6 ## 
maxVlty = volByHour.groupby(['Year']).agg({'HourlyVolatility': 'max'}) # Similar problem, not sure how to keep the settlement point column without using it to group.
maxVlty.to_csv(output+'\\MaxVolatilityByYear.csv')

## Task 7 ## Again had problems with renaming, but got the dataframes.
settpoint = ' '
def spotter(settpoint):
        spotpoint = ogprices[ogprices['SettlementPoint'].astype(str).str.contains(settpoint, False)]
        spotpoint['Date'] = pd.to_datetime(spotpoint['Date']).dt.strftime('%Y-%m-%d %H:%M')
        spotpoint['Hour'] = spotpoint['Date'].apply(lambda x: x.split(' ')[1])
        spotpoint['Date'] = spotpoint['Date'].apply(lambda x: x.split(' ')[0])
        spotpoint = spotpoint[['SettlementPoint','Date','Hour','Price']]
        spotpoint.groupby('Date')
        spotpoint.set_index('SettlementPoint', inplace=True)
        spotpoint = spotpoint.pivot_table(index=['SettlementPoint','Date'], columns='Hour', values='Price',fill_value=0)
        spotpoint.to_csv(output+"\\formattedSpotHistory\\spot_"+settpoint+".csv")

names = pd.DataFrame({'SettlementPoint':ogprices.SettlementPoint.unique()})
Z = names['SettlementPoint'].to_numpy()
for x in Z:
    spotter(x)

## Bonus, Volatility Plot ## Tried to get plot with Year on x axis, Volatlity on y axis, but kept getting key errors
# plot = volByHour["Year"]["HourlyVolatility"].plot()
# plot.savefig(output+'\\VolPlot.png')
