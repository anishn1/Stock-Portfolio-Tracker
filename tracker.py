import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import datetime

st.title("Stock Portfolio Tracker")

if "rows" not in st.session_state:
    st.session_state.rows = [{"ticker": "", "date": datetime.date.today() , "investment": 0.0}]

def removeRow(index):
    st.session_state.rows.pop(index)
    st.rerun()

for i, row in enumerate(st.session_state.rows):
    col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
    with col1:
        row["ticker"] = st.text_input("Enter Stock Ticker (e.g. AAPL)", value=row["ticker"], key = f"ticker_{i}").upper()
    with col2:
        row["date"] = st.date_input("Investment Date", value=row["date"], key = f"date_{i}")
    with col3:
        row["investment"] = st.number_input("Initial Investment (£)", min_value=0.0, value=row["investment"], key = f"investment_{i}")
    with col4:
        if st.button("❌", key=f"delete_{i}"):
            removeRow(i)
            


def addRow():
    st.session_state.rows.append({"ticker": "", "date": datetime.date.today() , "investment": 0.0})

def toGBP(amount, currency):
    if currency == "GBP":
        return amount
    exchName = f"{currency}GBP=X"
    exchangeData = yf.download(exchName, period="1d")
    rate = exchangeData["Close"].iloc[-1].item()
    return amount * rate



st.button("➕ Add Another Investment", on_click=addRow)

if st.button("Track Portfolio"):
    portfolioRes = []
    portfolioDF = pd.DataFrame()
    for row in st.session_state.rows:
        ticker = row["ticker"]
        date = row["date"]
        investment = row["investment"]
        if not ticker:
            st.warning("Please enter a ticker.")
            continue
        data = yf.download(ticker, start=date, auto_adjust=False)
        if data.empty:
            st.warning(f"No data found for {ticker} from {date}. Skipped.")
            continue
        info = yf.Ticker(ticker).info
        currency = info.get("currency", "GBP")

        startPrice = float(data["Close"].iloc[0].item())
        latestPrice = float(data["Close"].iloc[-1].item())
        startPriceGBP = startPrice
        if not currency == "GBP":
            startPriceGBP = toGBP(startPriceGBP, currency)
        shares = investment/startPriceGBP
        currVal = shares * latestPrice
        currValgbp = currVal
        if not currency == "GBP":
            currValgbp = toGBP(currVal, currency)
        profit = currValgbp - investment
        portfolioRes.append({"Ticker": ticker, "Invested Amount": investment, "Date Invested": date, "Shares": shares, "Current Value": currValgbp, "Profit/Loss": profit})
        portfolio_series =  data["Close"] * shares
        if not currency == "GBP":
            portfolio_series = toGBP(portfolio_series, currency)
        portfolio_series.name = ticker
        portfolioDF = pd.concat([portfolioDF, portfolio_series], axis=1)
        portfolioDF = portfolioDF.groupby(portfolioDF.columns, axis=1).sum()
    
    if portfolioRes:
        resultsDF = pd.DataFrame(portfolioRes)
        st.dataframe(resultsDF.style.format({
            "Invested Amount": "£{:,.2f}",
            "Current Value": "£{:,.2f}",
            "Profit/Loss": "£{:,.2f}"
        }))
        portfolioDF["Total Portfolio Value"] = portfolioDF.sum(axis=1)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=portfolioDF.index, y=portfolioDF["Total Portfolio Value"], mode = "lines", name = "Total Portfolio Value"))
        fig.update_layout(xaxis_title = "Date", yaxis_title = "Portfolio Value (£)")

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No valid investments entered")