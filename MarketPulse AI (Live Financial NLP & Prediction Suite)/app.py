import datetime
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import streamlit as st
import yfinance as yf

# Initialize NLTK VADER Lexicon
nltk.download('vader_lexicon', quiet=True)

# Streamlit Page Setup
st.set_page_config(
    page_title='MarketPulse AI - Day 100 Capstone',
    page_icon='📈',
    layout='wide',
)


# --- DATA FETCHING & FEATURE ENGINEERING ---
@st.cache_data(ttl=3600)
def fetch_financial_data(ticker_symbol):
  # 1. Fetch Real Historical Stock Prices
  ticker = yf.Ticker(ticker_symbol)
  df = ticker.history(period='1y')

  if df.empty:
    return None

  df = df.reset_index()
  df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)

  # 2. Technical Indicators
  df['SMA_10'] = df['Close'].rolling(window=10).mean()
  df['SMA_30'] = df['Close'].rolling(window=30).mean()

  # 3. Simulated Financial News & NLP Sentiment Analysis
  sia = SentimentIntensityAnalyzer()
  headlines = [
      f'{ticker_symbol} beats Q3 earnings expectations with record revenue',
      f'Market volatility increases following federal interest rate updates',
      f'{ticker_symbol} expands AI infrastructure and strategic enterprise'
      ' partnerships',
      'Analyst downgrades sector outlook due to supply chain constraints',
      f'Strong consumer demand drives institutional buy ratings for'
      f' {ticker_symbol}',
  ]

  np.random.seed(42)
  df['Headline'] = np.random.choice(headlines, size=len(df))
  df['Sentiment_Score'] = df['Headline'].apply(
      lambda h: sia.polarity_scores(h)['compound']
  )

  # 4. Target Variable (Next Day Closing Price)
  df['Target_Next_Close'] = df['Close'].shift(-1)
  df = df.dropna()

  return df


# --- SIDEBAR CONTROLS ---
st.sidebar.title('⚡ Market Intelligence')
selected_ticker = st.sidebar.selectbox(
    'Select Financial Asset:',
    ['NVDA', 'AAPL', 'MSFT', 'TSLA', 'AMZN'],
    index=0,
)

st.sidebar.markdown('---')
st.sidebar.info(
    '**Day 100 Capstone Project**\nCombines Natural Language Processing (NLP)'
    ' with Time-Series Machine Learning.'
)

# Fetch Data
df = fetch_financial_data(selected_ticker)

if df is None:
  st.error('Failed to retrieve market data. Please try another ticker.')
  st.stop()

# --- MODEL TRAINING ---
features = ['Close', 'SMA_10', 'SMA_30', 'Sentiment_Score']
X = df[features]
y = df['Target_Next_Close']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
r2 = r2_score(y_test, predictions)

# --- DASHBOARD HEADER ---
st.title(f'📈 MarketPulse AI: {selected_ticker} Sentiment & Price Intelligence')
st.caption(
    'Real-Time Market Time-Series Engine Powered by Random Forest & NLTK VADER'
)
st.markdown('---')

# Key Performance Indicators
c1, c2, c3, c4 = st.columns(4)
latest_price = df['Close'].iloc[-1]
prev_price = df['Close'].iloc[-2]
price_diff = latest_price - prev_price
avg_sentiment = df['Sentiment_Score'].mean()

c1.metric(
    'Current Close Price', f'${latest_price:.2f}', f'{price_diff:+.2f}'
)
c2.metric('10-Day Moving Average', f'${df["SMA_10"].iloc[-1]:.2f}')
c3.metric('Average News Sentiment', f'{avg_sentiment:+.2f}')
c4.metric('Predictive $R^2$ Score', f'{r2 * 100:.2f}%')

# --- TAB VIEW ---
tab1, tab2, tab3 = st.tabs([
    '📊 Price History & Indicators',
    '🧠 Sentiment & ML Predictions',
    '📋 Full Dataset',
])

with tab1:
  st.subheader(f'📈 {selected_ticker} Historical Price & Moving Averages')
  fig_price = go.Figure()
  fig_price.add_trace(
      go.Scatter(
          x=df['Date'],
          y=df['Close'],
          mode='lines',
          name='Close Price',
          line=dict(color='#10b981', width=2),
      )
  )
  fig_price.add_trace(
      go.Scatter(
          x=df['Date'],
          y=df['SMA_10'],
          mode='lines',
          name='10-Day SMA',
          line=dict(color='#06b6d4', dash='dash'),
      )
  )
  fig_price.add_trace(
      go.Scatter(
          x=df['Date'],
          y=df['SMA_30'],
          mode='lines',
          name='30-Day SMA',
          line=dict(color='#f59e0b', dash='dot'),
      )
  )
  fig_price.update_layout(
      template='plotly_dark',
      xaxis_title='Date',
      yaxis_title='Price ($)',
      height=480,
  )
  st.plotly_chart(fig_price, use_container_width=True)

with tab2:
  col_a, col_b = st.columns(2)

  with col_a:
    st.subheader('📰 Sentiment Score Distribution')
    fig_sent = px.histogram(
        df,
        x='Sentiment_Score',
        nbins=15,
        title='NLP Compound Sentiment Polarity',
        color_discrete_sequence=['#3b82f6'],
    )
    fig_sent.update_layout(template='plotly_dark')
    st.plotly_chart(fig_sent, use_container_width=True)

  with col_b:
    st.subheader('🎯 Actual vs Predicted Next Close')
    test_dates = df['Date'].iloc[-len(y_test) :]
    fig_ml = go.Figure()
    fig_ml.add_trace(
        go.Scatter(
            x=test_dates,
            y=y_test,
            mode='lines',
            name='Actual Price',
            line=dict(color='#10b981'),
        )
  )
    fig_ml.add_trace(
        go.Scatter(
            x=test_dates,
            y=predictions,
            mode='lines',
            name='ML Forecast',
            line=dict(color='#ef4444', dash='dash'),
        )
    )
    fig_ml.update_layout(
        template='plotly_dark', xaxis_title='Date', yaxis_title='Price ($)'
    )
    st.plotly_chart(fig_ml, use_container_width=True)

with tab3:
  st.subheader('📋 Processed Market Dataset')
  st.dataframe(
      df[[
          'Date',
          'Close',
          'SMA_10',
          'SMA_30',
          'Headline',
          'Sentiment_Score',
          'Target_Next_Close',
      ]],
      use_container_width=True,
  )