import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt


st.title("Bitcoin Prices over past few days")

days = st.slider('Days', 1, 365, 90)
currency = st.radio('Currency',['cad','usd', 'inr'])



API_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=cad&days=90&interval=daily"
payload = {'vs_currency': currency,'days': days,'interval':'daily'}
req = requests.get(API_URL, payload)
if req.status_code == 200: 
    bitcoin = req.json()
    
    bitcoin_prices = bitcoin["prices"]
    
    df = pd.DataFrame(data=bitcoin_prices, columns=["Date", "Price"])
    
    # Convert epoch time to YYYY-MM-DD format 
    df['Date'] = pd.to_datetime(df['Date'],unit='ms')
    df['PriceDifference'] = df['Price'].diff().fillna(0)
    
    df.plot.line(x='Date', y='Price')
    
    # Streamlit charts
    fig, ax = plt.subplots(figsize=(16,6))
    ax.plot(df['Date'], df['Price'])
    ax.set_ylim(ymin=0)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel(currency,fontsize=18)
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(16,6))
    ax.bar(df['Date'], df['PriceDifference'])
    # ax.set_ylim(ymin=0)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel("Difference in price from previous day",fontsize=18)
    st.pyplot(fig)
    
    

                          
    
    