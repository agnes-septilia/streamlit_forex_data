# streamlit_forex_data

This is the repository for Forex Data project for Streamlit.
The API data is taken from website https://twelvedata.com/. You can sign up for free to get your own API key.


The main files are written with Python language:

1. forex_data.py: which you can run without Streamlit integration. The purpose is for you to learn how the logic of code works. 

2. forex_data_streamlit.py: which is the code written for Streamlit integration.

3. user_index.py: the list of parameter options for user

Others are supporting files like example of .env file, and requirement.txt.


<h3 style='color: black;'>Project Workflow</h3>

1. The user will input the parameters, such as: currency pair, time interval, output size, datetime period, and timezone

2. All parameters will be generated as url parameters

3. Once got the response, the data will be shown in two form: dataframe and candlestick chart


<h3 style='color: black;'>Main Libraries</h3>

* streamlit

* pandas

* plotly

