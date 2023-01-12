"""
Forex API Source: https://twelvedata.com/
Free API access is available upon sign up.
To import complete package from twelvedata use: $ pip install twelvedata[pandas,matplotlib,plotly,websocket-client]
However in this code, we want to customize the input, so we will use regular url request.
"""


### ============== ###
### GET USER INPUT ###
### ============== ###

# Import index file
import user_index

# Combine all user inputs as API parameter
params = ""
def UserParams(key, value):
    global params
    if value == 'NONE':
        pass
    else:
        params += "&" + key + "=" + value
        return params

# Get base currency input
print("Base currencies available: " + ", ".join(user_index.symbol_base))
user_base_symbol = input("Choose Base Currency: ").upper()
print()

# Get quote currency input, by eliminate the choice of base currency
symbol_quote = user_index.symbol_quote
symbol_quote.remove(user_base_symbol)
print("Quote currencies available: " + ", ".join(symbol_quote))
user_quote_symbol = input("Choose Quote Currency: ").upper()
print()

user_currency_pair = user_base_symbol + "/" + user_quote_symbol
UserParams("symbol", user_currency_pair)

# Get interval input
print("Interval available: " + ", ".join(user_index.interval))
user_interval = input("Choose Interval: ").lower()
print()
UserParams("interval", user_interval)

# Get output-size input
user_output_size = int(input("Enter Output Size (min = 1, max = 5000) : "))
print()
if user_output_size >= 1 and user_output_size <= 5000:
    UserParams("outputsize", str(user_output_size))
elif user_output_size > 5000:
    UserParams("outputsize", "5000")
else:
    UserParams("outputsize", 'NONE')


# Give option to choose whether to set dates or not
start_date_option = input('Assign Start Datetime ? (yes / no) : ').lower()
print()

if start_date_option == 'yes':
    user_start_date = input("Enter Start Datetime with format yyyy-mm-dd hh:mm : ")
    UserParams("start_date", user_start_date + ":00")
    print()

end_date_option = input('Assign End Datetime ? (yes / no) : ').lower()
print()

if end_date_option == 'yes':
    user_end_date = input("Enter End Datetime with format yyyy-mm-dd hh:mm : ")
    UserParams("end_date", user_end_date + ":00")
    print()


# Get timezone input
user_timezone = input("Input Timezone (GMT-4 or GMT+8) : ").upper()
print()
if user_timezone in user_index.timezone.keys():
    user_timezone_converted = user_index.timezone[user_timezone]
    UserParams("timezone", user_timezone_converted)

# print(params)


### ========================= ###
### CONNECT TO TWELVEDATA API ###
### ========================= ###

import requests
import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import numpy as np

# Get the API key
API_KEY = os.getenv('API_KEY')

# Hit the API through URL
url = f"https://api.twelvedata.com/time_series?&apikey={API_KEY}{params}"
try:
    response = requests.get(url).json()['values']
except:
    print("URL cannot be accessed. Check your parameter input!")

# Convert result to dataframe
df = pd.DataFrame(response).sort_values(by=['datetime'], ignore_index=True)
df.index = np.arange(1, len(df)+1)


title = f"{user_base_symbol}/{user_quote_symbol} interval {user_interval}"
print(f"Result Table {title}: ")
print(df)


### ======================== ###
### CREATE CANDLESTICK CHART ###
### ======================== ###

import plotly
import plotly.graph_objects as go

# Define the chart parameter
candlestick = go.Candlestick(
                x=df['datetime'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close']
                )

fig = go.Figure(data=[candlestick])

# Remove slider
fig.update_layout(xaxis_rangeslider_visible=False)

# Add title to chart
fig.update_layout(
    width=1300, height=800,
    title={'text': title,
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
 
# Show chart
fig.show()


