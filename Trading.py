from matplotlib import pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

ALPHA_VANTAGE_API = '8419TBA0B4AAB8NS'
ts = TimeSeries(key = ALPHA_VANTAGE_API, output_format = 'pandas')
ti = TechIndicators(key = ALPHA_VANTAGE_API, output_format = 'pandas')

ticker = 'TXMD'

#get data from the stock
data, meta = ts.get_daily(symbol=ticker, outputsize = 'full')
data_MACD, _ = ti.get_macd(symbol = ticker, interval = 'daily', 
	series_type = 'close', fastperiod = 26, slowperiod = 52, signalperiod = 12)
data_SMA, _ = ti.get_sma(symbol = ticker, interval = 'daily', series_type = 'close', time_period = '10')


daily_values = data['4. close'].values
daily_volumes = data['5. volume'].values
daily_sma = data_SMA['SMA'].values #NOTE: daily SMA is in reverse (earliest to latest)
days = data.index

macd_signal = data_MACD['MACD_Signal'].values
macd = data_MACD['MACD'].values


####
period = 90
fig, ax1 = plt.subplots()
ax1.set_xlabel('time (days)')
ax1.set_ylabel('price ($)', color = 'red')
ax1.plot(days[:period], daily_values[:period], color = 'red')
ax1.tick_params(axis = 'y', labelcolor = 'red')

ax2 = ax1.twinx()
ax2.set_ylabel('MACD', color = 'blue')
ax2.plot(days[:period], macd_signal[:period], color = 'blue', label = 'Signal')
ax2.plot(days[:period], macd[:period], color = 'green', label = 'MACD')
ax2.tick_params(axis = 'y', labelcolor = 'blue')

fig.tight_layout()
plt.suptitle(ticker + ' price and MACD Signal')
plt.legend()
plt.show()


fig, ax1 = plt.subplots()
ax1.set_xlabel('time (days)')
ax1.set_ylabel('price ($)', color = 'red')
ax1.plot(days[:period], daily_values[:period], color = 'red')
ax1.tick_params(axis = 'y', labelcolor = 'red')

ax2 = ax1.twinx()
ax2.set_ylabel('Volume change (%)', color = 'blue')
ax2.plot(days[:period], daily_volumes[:period], color = 'blue')
ax2.tick_params(axis = 'y', labelcolor = 'blue')

fig.tight_layout()
plt.suptitle(ticker + ' price + volume %')
plt.legend()
plt.show()

print('Closing Price: ', round(daily_values[0],2))
