import streamlit as st
from datetime import date
import yfinance as yf
import matplotlib.pyplot as plt
from plotly import graph_objs as go



start = "2020-01-01"
today = date.today().strftime("%Y-%m-%d")


st.title("Stock prediction - EveGPT")
stocks = ["AAPL",
            "TSLA",
            "GOOG",
            "AMZN",
            "MSFT",
            "NVDA"]
selected_Stocks = st.selectbox("Select stock", stocks)
n_years = st.slider("Year of prediction",1,4)
period = n_years*365

def load_data(ticker):
    tickers = yf.Tickers(ticker)
    data = tickers.tickers[ticker].history(period="4y")
    data.reset_index(inplace = True)
    return data

data_load_state = st.text("load data...")
data = load_data(selected_Stocks)
data_load_state.text("load data...done!")



st.subheader("Raw data")
st.write(data.tail())

def plot_raw_data(Data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Data["Date"], y= Data["Open"], name = "stock_open"))
    fig.add_trace(go.Scatter(x=Data["Date"], y= Data["Close"], name = "stock_Close"))
    fig.layout.update(title_text="Time series data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
plot_raw_data(data)
