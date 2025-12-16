import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Stock Analysis",
    page_icon = BASE_DIR / "stockImg.png",
    layout="wide"
)


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
    
col1, col2, col3, col4 = st.columns(4)

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

# with col5:
#     st.markdown(f"""
#     <div class="metric-box">
#         <div class="metric-title">Green vs Red</div>
#         <div class="metric-value"><span class="valueGreen">{green_count}</span> / <span class="valueRed">{red_count}</span> </div>
#     </div>
#     """, unsafe_allow_html=True)


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
    csv_path = BASE_DIR / "Sector_data.csv"

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

col1, = st.columns(1)
with col1:
    st.subheader('Top 5 Gainers and Losers (Month-wise)')
    
    stock_df['date'] = pd.to_datetime(stock_df['date'], utc=True)
    stock_df = stock_df.sort_values(['Ticker', 'date'])

    monthly_data = stock_df.groupby([
        'Ticker', 
        stock_df['date'].dt.to_period('M') 
    ])['close'].agg(['first', 'last']).reset_index()

    monthly_data['Monthly_Return'] = (monthly_data['last'] - monthly_data['first']) / monthly_data['first']

    monthly_data['Month'] = monthly_data['date'].dt.strftime('%Y-%m')
    monthly_data = monthly_data.drop(columns=['date', 'first', 'last'])

    def get_top_n(group, n=5):
        """Sorts the group and returns the Top N Gainers and Top N Losers"""
        gainers = group.sort_values(by='Monthly_Return', ascending=False).head(n)
        losers = group.sort_values(by='Monthly_Return', ascending=True).head(n)
        return pd.concat([gainers, losers])

    monthly_breakdown = monthly_data.groupby('Month').apply(get_top_n).reset_index(drop=True)

    all_months = monthly_breakdown['Month'].unique()

    charts_data = {}

    for month in all_months:
        month_df = monthly_breakdown[monthly_breakdown['Month'] == month].copy()
        charts_data[month] = month_df
        
    output_file_name = BASE_DIR / "monthly_top5_gainers_losers.csv"
    monthly_breakdown.to_csv(output_file_name, index=False)

    num_plots = min(12, len(all_months))
    if num_plots > 0:
        fig, axes = plt.subplots(num_plots, 2, figsize=(14, 6 * num_plots))
        axes = axes.flatten()

        plot_index = 0
        for i in range(num_plots):
            month = all_months[i]
            month_data = charts_data[month].sort_values('Monthly_Return', ascending=False)
            
            gainers_df = month_data.head(5)
            losers_df = month_data.tail(5)
            
            ax_gainer = axes[plot_index]
            gainers_df = gainers_df.sort_values('Monthly_Return', ascending=True) 
            ax_gainer.barh(gainers_df['Ticker'], gainers_df['Monthly_Return'], color='green')
            ax_gainer.set_title(f'Top 5 Gainers: {month}', fontsize=12)
            ax_gainer.set_xlabel('Return (%)', fontsize=10)
            ax_gainer.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2%}'))
            plot_index += 1
            
            ax_loser = axes[plot_index]
            losers_df = losers_df.sort_values('Monthly_Return', ascending=False) 
            ax_loser.barh(losers_df['Ticker'], losers_df['Monthly_Return'], color='red')
            ax_loser.set_title(f'Top 5 Losers: {month}', fontsize=12)
            ax_loser.set_xlabel('Return (%)', fontsize=10)
            ax_loser.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2%}'))
            plot_index += 1

        plt.tight_layout()
        st.pyplot(plt)
    else:
        print("Not enough data to generate demonstration plots.")
    
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
