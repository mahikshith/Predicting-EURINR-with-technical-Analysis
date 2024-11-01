# Predicting-EURINR-with-technical-Analysis
 
>Introduction :

The Fundamental Idea of this Analysis is to help traders and Investors make better decision while buying and selling a stock using Technical Analysis with Moving Averages , Bollinger Bands and CCI

The data we considered is from January 1, 2023, to sept 30, 2024.

Took 20 day MA as standard because the frequency of data is daily

Moving Average period: 20 days and 50 days
Bollinger Bands: 20-day period with 2 standard deviations
CCI: 20-day period with standard thresholds of +100 and -100

BUY when price is above 20 MA > 50 MA ,  SELL when price is below 20 MA < 50 MA Else NEUTRAL

BUY when price touches lower Bollinger band vice versa for upper band else Neutral

BUY when CCI [Commodity Channel Index] < -100 (oversold) , SELL when CCI > 100 (overbought)

NEUTRAL when CCI is between -100 and 100   

Remember most of the technical Indicators are Lagging Indicators 

>Approach :

Import and pre-process the data

Calculate Moving Averages - Buy and sell triggers

Bollinger Bands with ± 2 standard deviation

CCI with ± 100 channels

Analyzing daily trends 

Calculate metrics for day after sep-30 and week after sep-30 

Graphs for visual aid for end users

We have to consider the last week window period into the data while analyzing since we assumed using 20 moving average for daily analysis.
If we take the data for last week separately from Analysis then we would be getting NaN since we are using 20 MA i.e the first 20 data points for MA would be NaN. 
All the metrics have been calculated based on their respective formulae

Reiterating the fact that these decision triggers are based on 20 MA ; these decisions are influenced by time frame that we choose
Technical indicators + Funda mental Analysis combination should be considered for long term investing for stocks as they are affected by a lot of economic factors

![image](https://github.com/user-attachments/assets/54a65e70-679c-4617-98c5-56f27eae8785)




