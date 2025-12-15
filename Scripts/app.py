import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "final_output.csv"

stock_df = pd.read_csv(csv_path)

stock_df['date'] = pd.to_datetime(stock_df['date'])
stock_df = stock_df.sort_values(['Ticker', 'date'])
yearly_return = stock_df.groupby('Ticker').apply(
    lambda x: ((x['close'].iloc[-1] - x['open'].iloc[0]) / x['open'].iloc[0]) * 100
).reset_index(name='Yearly Return')

green_count = (yearly_return['Yearly Return'] > 0).sum()
red_count = (yearly_return['Yearly Return'] < 0).sum()

average_price = stock_df['close'].mean().round(2)
average_prices = stock_df[['open', 'close', 'high', 'low']].mean().round(2)
average_volume = stock_df['volume'].mean().round(2)

col1, col2, = st.columns([1,1])
with col1:
    st.header('Market Stock Analysis')
    
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Green Stocks</div>
        <div class="metric-value valueGreen">{green_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Loss Stocks</div>
        <div class="metric-value valueRed">{red_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Average Price</div>
        <div class="metric-value">₹{average_price}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Average Volume</div>
        <div class="metric-value">{average_volume}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Green vs Red</div>
        <div class="metric-value"><span class="valueGreen">{green_count}</span> / <span class="valueRed">{red_count}</span> </div>
    </div>
    """, unsafe_allow_html=True)


top10_green = yearly_return.sort_values('Yearly Return', ascending=False).head(10)
top10_loss = yearly_return.sort_values('Yearly Return', ascending=True).head(10)

col1, col2, = st.columns([1,1])
with col1:
    st.subheader('Top 10 Green Stock')
    st.dataframe(top10_green, hide_index=True)

with col2:
    st.subheader('Top 10 Loss Stock')
    st.dataframe(top10_loss, hide_index=True)
    

col1, = st.columns(1)
with col1:
    st.subheader('Volatility Analysis')

stock_df['date'] = pd.to_datetime(stock_df['date'])
stock_df = stock_df.sort_values(['Ticker', 'date'])

stock_df['daily_return'] = stock_df.groupby('Ticker')['close'].pct_change()

volatility_df = stock_df.groupby('Ticker')['daily_return'].std().reset_index()
volatility_df.columns = ['Ticker', 'Volatility']
volatility_df = volatility_df.dropna()
top10_volatility = volatility_df.sort_values('Volatility', ascending=False).head(10)

col1, col2, = st.columns([1,2])
with col1:
    st.dataframe(top10_volatility, hide_index=True)

with col2:
    plt.figure(figsize=(12,6))
    plt.bar(top10_volatility['Ticker'], top10_volatility['Volatility'])
    plt.xlabel("Stock Ticker")
    plt.ylabel("Volatility (Standard Deviation of Daily Returns)")
    plt.title("Top 10 Most Volatile Stocks (Yearly)")
    plt.xticks(rotation=20)
    plt.tight_layout()
    st.pyplot(plt)
    
col1, = st.columns(1)
with col1:
    st.subheader('Cummulative Return')
    
col1, = st.columns(1)
with col1:
    stock_df['date'] = pd.to_datetime(stock_df['date'])
    stock_df = stock_df.sort_values(['Ticker', 'date'])
    stock_df['daily_return'] = stock_df.groupby('Ticker')['close'].pct_change()
    stock_df['cumulative_return'] = (1 + stock_df['daily_return']).groupby(stock_df['Ticker']).cumprod() - 1
    final_returns = stock_df.groupby('Ticker')['cumulative_return'].last().sort_values(ascending=False)
    top5_tickers = final_returns.head(5).index.tolist()
    
    plot_df = stock_df[stock_df['Ticker'].isin(top5_tickers)]
    plt.figure(figsize=(6, 4))

    for ticker in top5_tickers:
        df_temp = plot_df[plot_df['Ticker'] == ticker]
        plt.plot(df_temp['date'], df_temp['cumulative_return'], label=ticker)

        plt.xlabel("Date")
        plt.ylabel("Cumulative Return")
        plt.title("Cumulative Return Over Time – Top 5 Performing Stocks")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
    st.pyplot(plt)


col1, = st.columns(1)
with col1:
    st.subheader('Sector-wise Performance')

    BASE_DIR = Path(__file__).resolve().parent
    csv_path = BASE_DIR / "Sector_data - Sheet1.csv"

    sector_df = pd.read_csv(csv_path)

    stock_df['date'] = pd.to_datetime(stock_df['date'])
    stock_df = stock_df.sort_values(['Ticker', 'date'])

    yearly_return = (
        stock_df.sort_values(['Ticker', 'date'])
            .groupby('Ticker')
            .agg(
                start_price=('close', 'first'),
                end_price=('close', 'last')
            )
    )

    yearly_return['Yearly Return'] = (
        (yearly_return['end_price'] - yearly_return['start_price']) 
        / yearly_return['start_price']
    )


    sector_df['Ticker'] = sector_df['Symbol'].apply(lambda x: x.split(': ')[-1].strip())

    merged_df = yearly_return.merge(sector_df, on='Ticker', how='left')
    sector_performance = merged_df.groupby('Sector')['Yearly Return'].mean().reset_index()
    
    plt.figure(figsize=(12, 6))
    plt.bar(sector_performance['Sector'], sector_performance['Yearly Return'])
    plt.xlabel("Sector")
    plt.ylabel("Average Yearly Return (%)")
    plt.title("Average Yearly Return by Sector")
    plt.xticks(rotation=90)
    plt.tight_layout()
    
col1, col2, = st.columns([1,2])
with col1:
    st.dataframe(sector_performance, hide_index=True)

with col2:
    st.pyplot(plt)
    

col1, = st.columns(1)
with col1:
    st.subheader('Stock Price Correlation')

    price_pivot = stock_df.pivot(index='date', columns='Ticker', values='close')

    returns = price_pivot.pct_change().dropna()
    corr_matrix = returns.corr()
    
    plt.figure(figsize=(16, 10))
    plt.imshow(corr_matrix, cmap='coolwarm', interpolation='nearest')
    plt.colorbar()

    plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=90)
    plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)

    plt.title("Stock Price Correlation Heatmap")
    plt.tight_layout()
    st.pyplot(plt)

st.markdown("""
<style>
.metric-box {
    background-color: #ffffff;
    # padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    padding: 30px;
}
.metric-title {
    font-size: 20px;
    font-weight: bold;
    color: #555;
}
.metric-value {
    font-size: 30px;
    font-weight: bold;
    color: #1f77b4;
}
.st-emotion-cache-1w723zb {
    width: 100%;
    padding: 3rem 1rem 0rem;
    max-width: 90%;
}

.valueGreen {
    color: green
}

.valueRed {
    color: red
}
</style>
""", unsafe_allow_html=True)
