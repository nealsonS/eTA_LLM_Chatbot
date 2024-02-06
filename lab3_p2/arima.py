from read_mysql_data import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error


data = pd.DataFrame()
data['Close'] = df['Close']
dates = []
for i in range(len(df['Close'])):
	dates.append(i)  #dummy dates for now
data['Date'] = dates
#data['Date'] = pd.to_datetime(data['Date'])
#data.set_index('Date', inplace=True)

# Plot the stock prices
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Actual Stock Prices')
plt.title('Stock Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend()
plt.show()

# Check if the data is stationary (using Dickey-Fuller test)
from statsmodels.tsa.stattools import adfuller

result = adfuller(data['Close'])
print('ADF Statistic:', result[0])
print('p-value:', result[1])
print('Critical Values:', result[4])

# If the data is not stationary, difference it to make it stationary
if result[1] > 0.05:
    data_diff = data['Close'].diff().dropna()
else:
    data_diff = data['Close']

# Plot the differenced data
plt.figure(figsize=(12, 6))
plt.plot(data_diff, label='Differenced Stock Prices')
plt.title('Differenced Stock Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price Difference')
plt.legend()
plt.show()

# Split the data into training and testing sets
train_size = int(len(data_diff) * 0.8)
train, test = data_diff[0:train_size], data_diff[train_size:]

# Fit ARIMA model
order = (5, 1, 5)  # Example order parameters (p, d, q)
model = ARIMA(train, order=order)
model_fit = model.fit()

# Make predictions
predictions = model_fit.predict(start=len(train), end=len(train) + len(test) - 1, typ='levels')

# Invert differencing to get predictions in original scale
predictions_cumsum = predictions.cumsum()
#predicted_prices = pd.Series(data['Close'].iloc[train_size] + predictions_cumsum, index=test.index)

# Fill NaN values at the beginning (if any)
first_non_nan_index = predictions_cumsum.first_valid_index()
predictions_cumsum.loc[first_non_nan_index:] = data['Close'].iloc[train_size] + predictions_cumsum.loc[first_non_nan_index:]

# Create a Series with the adjusted predictions
predicted_prices = pd.Series(predictions_cumsum, index=test.index)

# Plot actual vs predicted prices
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Actual Stock Prices')
plt.plot(predicted_prices, label='Predicted Stock Prices')
plt.title('Actual vs Predicted Stock Prices')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend()
plt.show()

# Evaluate the model
print(len(data['Close'][train_size:])) #problem here
print(len(predicted_prices))
#for d in data['Close'][train_size:]:
#	print(d)
#print("~~~~~~~~~~~~~~~~~~~~")
#for p in predicted_prices:
#	print(p)
mse = mean_squared_error(data['Close'][train_size:], predicted_prices)
print('Mean Squared Error:', mse)

