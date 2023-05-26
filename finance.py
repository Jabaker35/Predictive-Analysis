# Import necessary libraries
import yfinance as yf
import pandas as pd
import yahoo_fin.stock_info as si

# Fetch NASDAQ ticker symbols using yahoo_fin package
# The tickers are returned as a DataFrame
nasdaq = pd.DataFrame(si.tickers_nasdaq())

# Convert the DataFrame into a set (an unordered collection of unique elements)
# We use a set to easily remove duplicates
sym = set(symbol for symbol in nasdaq[0].values.tolist())

# Define a list of suffixes that we want to exclude from our symbol set
my_list = ['W', 'R', 'P', 'Q']

# Initialize sets to store the ticker symbols we want to keep and discard
sav_set = set()
del_set = set()

# Loop through the symbol set
for symbol in sym:
    # If a symbol has more than 4 characters and its last character is in our suffix list...
    if len(symbol) > 4 and symbol[-1] in my_list:
        # ...add it to the discard set
        del_set.add(symbol)
    else:
        # Otherwise, add it to the save set
        sav_set.add(symbol)

# Sort the symbols in the save set and select the first 10
tickers = sorted(sav_set)[:10]

# Initialize an empty list to store stock movement data
movementlist = []

# Loop through each ticker symbol
for stock in tickers:
    # Download the stock's 5-day price history using yfinance
    thestock = yf.download(tickers=stock, period="5d", interval="1d", ignore_tz=True, prepost=False)

    # Find the minimum low price and the maximum high price over the 5-day period
    low = thestock['Low'].min()
    high = thestock['High'].max()

    # Calculate the percentage change between the high and low prices
    deltapercent = 100 * (high - low) / low

    # Fetch the opening price of the stock
    # If there are at least 5 days of history, also fetch the closing price of the stock
    # Otherwise, use the opening price as the closing price
    if len(thestock) >= 5:
        Close = thestock.iloc[4]["Close"]
        Open = thestock.iloc[0]["Open"]
    else:
        Close = Open = thestock.iloc[0]["Open"]

    # Calculate the percentage change in price from opening to closing
    # If the opening price is zero (to avoid division by zero), set the price change to zero
    deltaprice = 100 * (Close - Open) / Open if Open != 0 else 0

    # Append the stock symbol, high price, low price, percentage change, and price change to the movement list
    pair = [stock, high, low, deltapercent, deltaprice]
    movementlist.append(pair)

# Convert the movement list into a DataFrame
movement = pd.DataFrame(movementlist, columns=['stock', 'high', 'low', 'deltapercent', 'deltaprice'])

# Write the DataFrame to a CSV file named 'latest_movement.csv'
# The 'header=True' argument means that the column names will be written to the file
# The 'index=True' argument means that the row indices will be written to the file
# 'encoding='utf-8'' specifies the character encoding to be used for the file
movement.to_csv('latest_movement.csv', header=True, index=True, encoding='utf-8')
