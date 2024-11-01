"""Assumptions:Took 20 day MA as standard because the frequency of data is daily

Moving Average period: 20 days and 50 days
Bollinger Bands: 20-day period with 2 standard deviations
CCI: 20-day period with standard thresholds of +100 and -100

>Moving Average:

BUY when price is above 20 MA > 50 MA
SELL when price is below 20 MA < 50 MA
Else NEUTRAL


>Bollinger Bands:

BUY when price touches lower band
SELL when price touches upper band
NEUTRAL when price is between bands


>CCI:

BUY when CCI < -100 (oversold)
SELL when CCI > 100 (overbought)
NEUTRAL when CCI is between -100 and 100"""

# Import libraries :

import yfinance as yf
import pandas as pd
import numpy as np
from IPython.display import display
from datetime import datetime, timedelta

def fetch_currency_data():
    """Fetch EUR/INR data from Yahoo Finance"""
    euroinr = yf.download("EURINR=X",
                         start="2023-01-01",
                         end="2024-10-9",
                         interval="1d")
    euroinr.to_csv("euroinr.csv")

    return euroinr

# Comment out the following block if you have already processed the data

def preprocess_data(data):
    """Preprocess the data"""
    #data = pd.read_csv("euroinr.csv")
    data = data.dropna()
    data = data.reset_index(drop=True)

    data["Close"] = data["Close"].astype(float)
    data["High"] = data["High"].astype(float)
    data["Low"] = data["Low"].astype(float)

    data = data.rename(columns={'Price': 'calender_date'})
    data['calender_date'] = pd.to_datetime(data['calender_date'])
    data = data.set_index('calender_date')
    data.drop(["Adj Close","Volume"], axis=1, inplace=True)
    data.to_csv("euroinr_final.csv")
    return data

# Moving Averages

def calculate_moving_averages(data):
    """Calculate 20-day and 50-day moving averages and generate signals"""
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()

    # Generate MA signals
    data['MA_Signal'] = 'NEUTRAL'
    data.loc[data['MA20'] > data['MA50'], 'MA_Signal'] = 'BUY'
    data.loc[data['MA20'] < data['MA50'], 'MA_Signal'] = 'SELL'

    return data

# Bollinger Bands

def calculate_bollinger_bands(data, period=20, std_dev=2):
    """Calculate Bollinger Bands and generate signals"""
    data['BB_middle'] = data['Close'].rolling(window=period).mean()

    rolling_std = data['Close'].rolling(window=period).std()

    data['BB_upper'] = data['BB_middle'] + (rolling_std * std_dev)
    data['BB_lower'] = data['BB_middle'] - (rolling_std * std_dev)

    # Generate BB signals

    data['BB_Signal'] = 'NEUTRAL'
    data.loc[data['Close'] < data['BB_lower'], 'BB_Signal'] = 'BUY'
    data.loc[data['Close'] > data['BB_upper'], 'BB_Signal'] = 'SELL'

    return data

# CCI  

def calculate_cci(data, period=20):

    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    sma_tp = typical_price.rolling(window=period).mean()
    mad = typical_price.rolling(window=period).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)
    data['CCI'] = (typical_price - sma_tp) / (0.015 * mad)

    # Generate CCI signals
    data['CCI_Signal'] = 'NEUTRAL'
    data.loc[data['CCI'] < -100, 'CCI_Signal'] = 'BUY'
    data.loc[data['CCI'] > 100, 'CCI_Signal'] = 'SELL'

    return data

# One Day After sep-30 and week after sep-30

def tidy(data):

    # Get last day's value i.e : day after september 30
    last_day = data.iloc[-6]

    # week after september 30 :  gandhi jayanti is holiday so considering last days
    last_week = data.iloc[-6:]


    summary_data = {
        'Date': last_day.name.strftime('%Y-%m-%d'),
        'Close': last_day['Close'],
        'MA20': last_day['MA20'],
        'MA50': last_day['MA50'],
        'BB_upper': last_day['BB_upper'],
        'BB_lower': last_day['BB_lower'],
        'CCI': last_day['CCI']
    }

    summary = pd.DataFrame.from_dict(summary_data, orient='index', columns=['One Day Analysis'])
    summary = summary.T  # Transpose for better readability

    # Add one-week analysis
    one_week_summary = pd.DataFrame({
        'Period': f"{last_week.index[0].strftime('%Y-%m-%d')} to {last_week.index[-1].strftime('%Y-%m-%d')}",
        'Average Close': last_week['Close'].mean(),
        'Average MA20': last_week['MA20'].mean(),
        'Average MA50': last_week['MA50'].mean(),
        'Average BB_upper': last_week['BB_upper'].mean(),
        'Average BB_lower': last_week['BB_lower'].mean(),
        'Average CCI': last_week['CCI'].mean()
    }, index=['One Week Analysis'])

    # Concatenate one-day and one-week summaries
    summary = pd.concat([summary, one_week_summary])

    # Prepare signal DataFrame
    signals_df = pd.DataFrame({
        'Day after sep-30': [last_day['MA_Signal'], last_day['BB_Signal'], last_day['CCI_Signal']],
        ' Week after sep-30': [last_week['MA_Signal'].mode()[0], last_week['BB_Signal'].mode()[0], last_week['CCI_Signal'].mode()[0]]
    }, index=['Moving Average', 'Bollinger Bands', 'CCI'])

    # Print the summary as a table
    print(f"Day after september-30 : {summary_data['Date']},\n\nWeek after september-30 : {one_week_summary['Period']}\n\n")
    print(signals_df)

    return summary, signals_df

# Display the graphs : 

import matplotlib.pyplot as plt
import seaborn as sns

def plot_analysis(data):

    # subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 15))

    vertical_line_date = datetime(2024, 9, 30)

    #  Moving Averages
    ax1.plot(data.index, data['Close'], label='Close Price', color='blue', alpha=0.6)
    ax1.plot(data.index, data['MA20'], label='20-day MA', color='orange')
    ax1.plot(data.index, data['MA50'], label='50-day MA', color='red')

    ax1.axvline(x=vertical_line_date, color='black', linestyle='--', alpha=0.5, label='Sep 30, 2024')

    # Marking MA signals
    buy_signals = data[data['MA_Signal'] == 'BUY'].index
    sell_signals = data[data['MA_Signal'] == 'SELL'].index
    ax1.scatter(buy_signals, data.loc[buy_signals, 'Close'], color='green', marker='^',
                label='MA Buy Signal', alpha=0.7)
    ax1.scatter(sell_signals, data.loc[sell_signals, 'Close'], color='red', marker='v',
                label='MA Sell Signal', alpha=0.7)

    ax1.set_title('EUR/INR Price with Moving Averages -(Buy and sell)')
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True)

    # Bollinger Bands
    ax2.plot(data.index, data['Close'], label='Close Price', color='blue', alpha=0.6)
    ax2.plot(data.index, data['BB_upper'], label='BB Upper', color='gray', linestyle='--')
    ax2.plot(data.index, data['BB_middle'], label='BB Middle', color='gray')
    ax2.plot(data.index, data['BB_lower'], label='BB Lower', color='gray', linestyle='--')
    ax2.fill_between(data.index, data['BB_upper'], data['BB_lower'], alpha=0.1)

    ax1.axvline(x=vertical_line_date, color='black', linestyle='--', alpha=0.5, label='Sep 30, 2024')


    # Marking BB signals
    bb_buy_signals = data[data['BB_Signal'] == 'BUY'].index
    bb_sell_signals = data[data['BB_Signal'] == 'SELL'].index
    ax2.scatter(bb_buy_signals, data.loc[bb_buy_signals, 'Close'], color='green', marker='^',
                label='BB Buy Signal', alpha=0.7)
    ax2.scatter(bb_sell_signals, data.loc[bb_sell_signals, 'Close'], color='red', marker='v',
                label='BB Sell Signal', alpha=0.7)

    ax2.set_title('Bollinger Bands - (Buy and sell)')
    ax2.set_ylabel('Price')
    ax2.legend()
    ax2.grid(True)

    # CCI
    ax3.plot(data.index, data['CCI'], label='CCI', color='purple')
    ax3.axhline(y=100, color='r', linestyle='--', alpha=0.3)
    ax3.axhline(y=-100, color='r', linestyle='--', alpha=0.3)
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.2)

    ax1.axvline(x=vertical_line_date, color='black', linestyle='--', alpha=0.5, label='Sep 30, 2024')


    # Marking CCI signals
    cci_buy_signals = data[data['CCI_Signal'] == 'BUY'].index
    cci_sell_signals = data[data['CCI_Signal'] == 'SELL'].index
    ax3.scatter(cci_buy_signals, data.loc[cci_buy_signals, 'CCI'], color='green', marker='^',
                label='CCI Buy Signal', alpha=0.7)
    ax3.scatter(cci_sell_signals, data.loc[cci_sell_signals, 'CCI'], color='red', marker='v',
                label='CCI Sell Signal', alpha=0.7)

    ax3.set_title('Commodity Channel Index (CCI) - (Buy and sell)')
    ax3.set_ylabel('CCI Value')
    ax3.legend()
    ax3.grid(True)

    #plt.tight_layout()
    return fig

if __name__ == "__main__":
    fig = plot_analysis(df)
    fig2 = plot_analysis(df.tail(7))
    display(fig)
    display(fig2)
    plt.close(fig)
    plt.close(fig2)


# | Indicator       | Day after sep 30 | Week after sep 30 |
# |:---------------|:----------------:|:----------------:|
# | Moving Average |       BUY        |       BUY        |
# | Bollinger Bands|     NEUTRAL      |     NEUTRAL      |
# | CCI            |     NEUTRAL      |       BUY        |

# A detailed explanation of the code can be found here: 

# https://colab.research.google.com/drive/19bvwG_BKOStd9V4xM9b-uBPoK2I2Lod6?usp=sharing


# By Mahikshith - [https://github.com/mahikshith]