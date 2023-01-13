import streamlit as st
st.set_page_config(layout="centered")


### ============ ###
### INTRODUCTION ###
### ============ ###

st.caption("created by agnes_septilia")
st.write("")

st.markdown("<h1 style='text-align: center; color: black;'>FOREX DATA GENERATOR</h1>", unsafe_allow_html=True)

st.markdown("***")
st.markdown("<h3 style='text-align: center; color: black;'>Welcome to Forex Data Generator!</h3>", unsafe_allow_html=True)
st.write("")
st.write("In this project, you can generate Forex data in a Table or Candlestick chart form.")
st.write("Simply input the parameters you need, then click 'SUBMIT' button to proceed.") 
st.write("The data is taken from Forex API source: https://twelvedata.com/")
st.markdown("***")
st.write("")


### ============== ###
### GET USER INPUT ###
### ============== ###

import numpy as np
import pandas as pd
import datetime

# Import index file
import user_index

st.markdown("<h5 style='text: bold; color: black, text-align: center;'>INPUT PARAMETERS</h5>", unsafe_allow_html=True)
st.write("")


# Create empty dict and function to capture user inputs
user_input = {}
def UserInputs (key, value):
    global user_input
    user_input[key]= value
    return user_input

# Combine all user inputs as API parameter
params = ""
def UserParams(key, value):
    global params
    params += "&" + key + "=" + value
    return params


# Get user currency pair
currency_pair_help = "If you want to search EUR/USD pair, then EUR is the base currency, and USD is the quote currency"
user_base_symbol = st.selectbox("Choose Base Currency : ", user_index.symbol_base, index=6, help=currency_pair_help)
user_quote_symbol = st.selectbox("Choose Quote Currency : ", user_index.symbol_quote, index=6, help=currency_pair_help)
st.write("")

# Create error if the base currency is the same as quote currency
if user_base_symbol == user_quote_symbol:
    st.error("The Quote Currency should be different than Base Currency", icon="🚨")
    st.stop()

# Assign currency pair to UserInputs and UserParams
user_currency_pair = user_base_symbol + "/" + user_quote_symbol
UserInputs("Currency Pair", user_currency_pair)
UserParams("symbol", user_currency_pair)


# Get interval input
time_interval_help = "The unit of time between two data"
user_interval = st.selectbox("Choose Time Interval : ", user_index.interval, help=time_interval_help)
UserInputs("Time Interval", user_interval)
UserParams("interval", user_interval)
st.write("")


# Get Output size
output_size_help = "Amount of data you want to fetch -- Maximum is 5000"
user_output_size = st.slider("Choose Output Size : ", min_value=0, max_value=5000, step=200, help=output_size_help)
UserInputs("Output Size", str(user_output_size))
UserParams("outputsize", str(user_output_size))
st.write("")

# Create error if the Output Size is zero
if user_output_size == 0:
    st.error("The Output Size should be more than 0", icon="🚨")
    st.stop()


# Give option to choose whether to set dates or not
st.write("Apply Datetime Period (optional) : ")
start_date_option = st.checkbox('Start Datetime')
end_date_option = st.checkbox('End Datetime')
st.write("")

if start_date_option:
    user_start_date = st.date_input("Choose Start Datetime : ")
    user_start_time = st.time_input("Start Time", label_visibility="collapsed")
    user_start_datetime = str(user_start_date) + " " + str(user_start_time)
    UserInputs("Start Datetime", user_start_datetime)
    UserParams("start_date", user_start_datetime)
    st.write("")
else: 
    UserInputs("Start Datetime", "None")

if end_date_option:
    user_end_date = st.date_input("Choose End Datetime : ")
    user_end_time = st.time_input("End Time", label_visibility="collapsed")
    user_end_datetime = str(user_end_date) + " " + str(user_end_time)
    UserInputs("End Datetime", user_end_datetime)
    UserParams("end_date", user_end_datetime)
    st.write("")
else:
    UserInputs("End Datetime", "None")

if start_date_option == True and end_date_option == True:
    # Create error if the both start and end date is same
    if user_start_datetime == user_end_datetime:
        st.error("Start Datetime cannot be the same as End Datetime", icon="🚨")
        st.stop()
        
    # Create error if start date is more than end date
    if user_start_datetime > user_end_datetime:
        st.error("Start Datetime should be earlier than End Datetime", icon="🚨")
        st.stop()


# Get timezone input
st.write("Choose TimeZone")
user_timezone = st.selectbox("Choose Timezone : ", user_index.timezone, index=11, label_visibility="collapsed")
user_timezone_converted = user_index.timezone[user_timezone]
UserInputs("Timezone", user_timezone)
UserParams("timezone", user_timezone_converted)


# Show result of inputs
st.markdown("---")
st.write("Check your inputs before continue:")
st.dataframe(pd.DataFrame(user_input, index=[0]).T.rename(columns={0:'value'}))


### ========================= ###
### CONNECT TO TWELVEDATA API ###
### ========================= ###

# Get the API key from local env
# import os
# from dotenv import load_dotenv
# load_dotenv()
# API_KEY = os.getenv('API_KEY')   

# Get the API key from streamlit secret
API_KEY = st.secrets["API_KEY"]

# Hit the API through URL
import requests

url = f"https://api.twelvedata.com/time_series?&apikey={API_KEY}{params}"
response = requests.get(url).json()['values']

# Convert result to dataframe
df = pd.DataFrame(response).sort_values(by=['datetime'], ignore_index=True)
df.index = np.arange(1, len(df)+1)

# Add title
title = f"{user_base_symbol}/{user_quote_symbol} interval {user_interval}"



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
    title={'text': title,
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})



### ======================== ###
### SHOW RESULT AND DOWNLOAD ###
### ======================== ###

# Create function to convert dataframe to csv
@st.cache
def ConvertDF(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = ConvertDF(df)


# 'Submit' Button actions
if st.button("Submit"):
    # show dataframe
    st.markdown("---")
    st.write(f"Result of {title} data in table form: ")
    st.dataframe(df)

    # show download csv
    current_timestamp = datetime.datetime.now()
    current_timestamp = current_timestamp.strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f"{title} - {current_timestamp}.csv",
        mime='text/csv'
    )

    st.write("")
    st.write("")

    # Show chart
    st.write(f"Result of {title} data in candlestick chart form: ")
    st.caption("To download the chart, click on the camera icon on the top-right side of the chart")
    st.plotly_chart(fig)


    # Epilog
    st.write("")
    st.markdown("***")
    st.write("Thank you for using this Forex Data Generator on Streamlit!")
    st.write("Link to github code: https://github.com/agnes-septilia/streamlit_forex_data.git")
    st.write("")
    st.caption("created by agnes septilia")
