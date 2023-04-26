import streamlit as st
from datetime import date
import yfinance as yf
from plotly import graph_objs as go
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import time
import pandas_ta as ta
import os
import sys
from io import BytesIO

import keras
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Dense
from keras.layers import TimeDistributed


###############################################
#
#               Setting
#
################################################

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.set_page_config(page_title="EveGPT", page_icon="🐲")
st.markdown('<div style="background-color:#F4D03F;padding:10px;border-radius:10px;">', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #FF9E44;'>EveGPT</h1>", unsafe_allow_html=True)
Group = """
            <div style="background-color:#F4D03F;padding:10px;border-radius:10px;">
                <div style="color: black;">
                Group 6:
                Yang Fan (Blithe)
                Li Xinran (Anna)
                Zhu Jiarui (Janet)
                Fung Ho Kit (Justin)
                </br>
                Instructor: Dr. Matthias Buehlmaier
                </div>
            </div>
        """
st.markdown(Group, unsafe_allow_html=True)
path = os.getcwd()
path
sys.path.insert(0, ".")
try:
    local_css("./style.css")
except:
    local_css("/app/fina4350-nlp/Part4_EveGPT/style.css")



###############################################
#
#               Raw Data
#
################################################

start = "2020-07-20"
today = date.today().strftime("%Y-%m-%d")
st.write(f"Today is {today}")

stocks = ["AAPL",
            "TSLA",
            "GOOG",
            "AMZN",
            "MSFT",
            "NVDA"]
selected_Stocks = st.selectbox("Select stock", stocks)
#n_years = st.slider("Year of prediction",1,4)
#period = n_years*365

def load_data(ticker):
    tickers = yf.Tickers(ticker)
    data = tickers.tickers[ticker].history(start=start)
    data.index = pd.to_datetime(data.index).date
    #data.reset_index(inplace = True)
    return data

data_load_state = st.text("load data...")
StockPrice = load_data(selected_Stocks)
data_load_state.text("load data...done!")

st.write("Raw data")
st.write(StockPrice.tail())

def plot_raw_data(Data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Data.index, y= Data["Open"], name = "stock_open"))
    fig.add_trace(go.Scatter(x=Data.index, y= Data["Close"], name = "stock_Close"))
    fig.layout.update(title_text="Time series data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
plot_raw_data(StockPrice)


st.markdown('<div style="background-color:#F4D03F;padding:10px;border-radius:10px;">', unsafe_allow_html=True)

###############################################
#
#              Scraping
#
################################################


def load_scrapped_text(ticker):
    try:
        Path = f"data/{ticker}.xlsx"
        scraped_text = pd.read_excel(Path).iloc[::-1].set_index("date")
    except:
        Path = f"/app/fina4350-nlp/Part4_EveGPT/data/{ticker}.xlsx"
        scraped_text = pd.read_excel(Path).iloc[::-1].set_index("date")

    scraped_text = pd.read_excel(Path).iloc[::-1].set_index("date")
    scraped_text.index = pd.to_datetime(scraped_text.index).date
    return scraped_text
def load_sentiment_score(ticker):
    Path = f"../Part3_FinBert/output/predictions_{ticker}.csv"
    Sentiment = pd.read_csv(Path).iloc[::-1]\
                            .set_index("date")\
                            .drop(['Unnamed: 0'],axis=1)
    #Sentiment.index = pd.to_datetime(Sentiment["date"]).date
    Sentiment.column = ["Scores for title", "Score for summary"]
    return Sentiment

data_load_state = st.text("load data...")
scraped_text = load_scrapped_text(selected_Stocks)
Sentiment = load_sentiment_score(selected_Stocks)
data_load_state.text("load data...done!")

st.write("Scraped Text")
st.write(scraped_text.tail(10))

st.write("Sentiment score retrival")
st.write(Sentiment.tail(10))


###############################################
#
#               Run prediction
#
################################################

company = selected_Stocks
Starting = "2020-07-20"
Ending = "2023-04-14"

tickers = yf.Tickers(company)
StockPrice = tickers.tickers[company].history(start=Starting,end=Ending)
StockPrice.index = pd.to_datetime(StockPrice.index).date

Path = f"../Part3_FinBert/output/predictions_{company}.csv"
Sentiment = pd.read_csv(Path).iloc[::-1]\
                            .reset_index()\
                            .drop(['Unnamed: 0', "index"],axis=1)

Sentiment = Sentiment[Sentiment["date"] >= Starting]
Sentiment['date'] = pd.to_datetime(Sentiment['date'])
Sentiment.set_index('date', inplace=True)
Sentiment.index = pd.to_datetime(Sentiment.index).date

missing_rows_index = StockPrice.index.difference(Sentiment.index)
new_data = {'score_title': 0, 'score_summary': 0}
new_row = pd.DataFrame(new_data, index=missing_rows_index)
Sentiment = pd.concat((new_row,Sentiment),axis=0,sort=False)
index_to_keep = pd.Series(True, index=StockPrice.index)
mask = Sentiment.index.isin(index_to_keep.index)
Sentiment = Sentiment[mask]
Full_data = pd.concat((StockPrice,Sentiment),axis=1)

Full_data['RSI']=ta.rsi(Full_data.Close, length=30)
Full_data['EMAF']=ta.ema(Full_data.Close, length=30)
Full_data['EMAM']=ta.ema(Full_data.Close, length=30)
Full_data['EMAS']=ta.ema(Full_data.Close, length=30)

Full_data['TargetNextClose'] = Full_data['Close'].shift(-1)
Full_data['TargetNextClose'] = Full_data['Close'].shift(-1)
Full_data.iloc[:, 0:-1].dropna(inplace=True)
Full_data.drop(['Volume'], axis=1, inplace=True)
data_set = Full_data.iloc[30:-1, 6:12]
st.write(data_set)

sc = MinMaxScaler(feature_range=(0,1))
data_set_scaled = sc.fit_transform(data_set)
X = []
backcandles = 10 # Look back period

print(data_set_scaled.shape[0])
for j in range(6):
    X.append([])
    for i in range(backcandles, data_set_scaled.shape[0]):
        X[j].append(data_set_scaled[i-backcandles:i, j])

#move axis from 0 to position 2
X=np.moveaxis(X, [0], [2])
print(X.shape)

loaded_model = keras.models.load_model('EveGPT')
loaded_model.summary()
y_pred = loaded_model.predict(X)

y = Full_data.iloc[40:-1, 12:]
print(y)
sc = MinMaxScaler(feature_range=(0,1))
y_test = sc.fit_transform(y)

def plot_result():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = y.index,y = y_test.ravel(), name = 'original', line=dict(color='white')))
    fig.add_trace(go.Scatter(x = y.index,y = y_pred.ravel(), name = 'predition',  line=dict(color='#FF9E44')))
    fig.layout.update(title_text="Prediction", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
plot_result()

st.markdown('<div style="background-color:#F4D03F;padding:10px;border-radius:10px;">', unsafe_allow_html=True)
