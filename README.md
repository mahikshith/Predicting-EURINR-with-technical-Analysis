# Predicting-EURINR-with-technical-Analysis
 
### Introduction :

The Fundamental Idea of this Analysis is to help traders and Investors make better decision while buying and selling a stock using Technical Analysis with Moving Averages , Bollinger Bands and CCI

The data we considered is from January 1, 2023, to sept 30, 2024 and we make prediction for a buy or sell for a day , week after september 30

Took 20 day MA as standard because the frequency of data is daily

Moving Average period: 20 days and 50 days
Bollinger Bands: 20-day period with 2 standard deviations
CCI: 20-day period with standard thresholds of +100 and -100

BUY when price is above 20 MA > 50 MA ,  SELL when price is below 20 MA < 50 MA Else NEUTRAL

BUY when price touches lower Bollinger band vice versa for upper band else Neutral

BUY when CCI [Commodity Channel Index] < -100 (oversold) , SELL when CCI > 100 (overbought)

NEUTRAL when CCI is between -100 and 100   

Remember most of the technical Indicators are Lagging Indicators 

>### Approach :

Import the data from EUR/INR from Yahoo-finance,  pre-process the data

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

>### Moving Average Analysis : 

We took the closing price for calculating 20 MA & 50 MA 

If the small MA [20 -yellow] crosses Big MA [50-red] in upward trend a buy signal has been triggered (shown with green marker) and vice versa for sell signal (red marker) 

If 20 MA = 50 MA then neutral (No buy or sell has been triggered)

All the Analysis is based on the closing price.

![image](https://github.com/user-attachments/assets/145ca048-97f7-4109-9127-7200ce94bf80)

>### Bollinger bands : 

When the closing price hits upper band (20 MA + 2 Std ) then a sell signal has been triggered where as the closing price is closer to lower band (20 MA – 2 Std) then a buy , if the market is sideways or fluctuating in the middle band then neutral. 

The below Analysis for entire data , we can also the analysis for one day , one week after sep 30 in the table in the previous slide and graph for the same has been shown in the upcoming slides 

![image](https://github.com/user-attachments/assets/23d0a06d-0ebd-45d2-99ff-6a68f91ded6d)

>### CCI (Commodity Channel Index) :

 The CCI is a momentum-based oscillator used to identify overbought and oversold conditions in a market. 
 
 It measures the current price level relative to an average price level over a given period. Average of the high, low, and closing prices for each period (typical price) and calculate the simple MA (20) for typical price , then we calculate mean absolute deviation for every datapoint.
 
#### CCI = (Typical Price - SMA of TP) / (0.015 * MAD) 

BUY when CCI [Commodity Channel Index] < -100 (oversold) , SELL when CCI > 100 (overbought) , NEUTRAL when CCI is between -100 and 100.

![image](https://github.com/user-attachments/assets/88ecaf6e-330a-4d49-bb48-17092ecf7378)


#### Finally , making a prediction for a day and week after september 30 : 

![image](https://github.com/user-attachments/assets/32aa25c8-4674-4324-81d2-bf77adf34c48)

![image](https://github.com/user-attachments/assets/da6f3ca7-3e23-4ce2-ba3a-0f1242c9155b)









