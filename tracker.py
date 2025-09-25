import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("Stock Portfolio Tracker")

ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, MSFT)").upper()
date = st.date_input("Investment Date")
investment = st.number_input("Initial Investment (£)", min_value=0.0, value=1000.0)

if st.button("Track Portfolio"):
    data = yf.download(ticker, start=date)
    if not data.empty:
        startPrice = float(data["Close"].iloc[0].item())
        latestPrice = float(data["Close"].iloc[-1].item())
        shares = investment/startPrice
        currVal = shares * latestPrice
        st.write(f"Initial Investment: £{investment:.2f}")
        st.write(f"Current Value: £{currVal:.2f}")
        profit = currVal - investment
        st.write(f"Profit/Loss: £{profit:.2f} ({profit/investment*100:.2f}%)")
        fig, ax = plt.subplots()
        ax.plot(data.index, data["Close"], label=f"{ticker} Close Price")
        ax.set_title(f"{ticker} Price History")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (£)")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Invalid ticker given")