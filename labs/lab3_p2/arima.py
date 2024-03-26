from read_mysql_data import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pmdarima as pm
from sklearn.metrics import mean_squared_error
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from pmdarima.pipeline import Pipeline
from pmdarima.arima import ARIMA
from pmdarima.preprocessing import BoxCoxEndogTransformer
import pickle
import os

res_path = os.path.join('.', 'results')

# make results folder if not exists
if not os.path.exists(res_path):
    os.makedirs(res_path)

data = pd.DataFrame()
data['Close'] = df['Close']
data.index = pd.to_datetime(df['Date'], format = '%Y-%m-%d %H:%M')
#data['Date'] = pd.to_datetime(data['Date'])
#data.set_index('Date', inplace=True)

# visualization
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Actual Stock Prices')
plt.title('Stock Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend()
plt.show()

# check if data is stationary with dickey-fuller test
from statsmodels.tsa.stattools import adfuller

result = adfuller(data['Close'])
print('ADF Statistic:', result[0])
print('p-value:', result[1])
print('Critical Values:', result[4])

# if not stationary, find the difference to make it stationary
if result[1] > 0.05:
    print('Time series is not stationary! Differencing!')
    data_diff = data['Close'].diff().dropna()
else:
    print('Time series is stationary!')
    data_diff = data['Close']

# visualization
plt.figure(figsize=(12, 6))
plt.plot(data_diff, label='Differenced Stock Prices')
plt.title('Differenced Stock Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price Difference')
plt.legend()
plt.show()

# train the dataset with boxcox instead
train_size = int(len(data) * 0.8)
train, test = data[:train_size], data[train_size:]

# analyze ACF and PACF to check for order
def plot_acf_pacf(data):
    f, ax = plt.subplots(nrows=2, ncols=1, figsize=(12, 6))
    plot_acf(data,ax=ax[0])
    plot_pacf(data,ax=ax[1], method='ols')

    plt.tight_layout()
    plt.show()

    p = input('Type order of p:\n')
    d = input('Type order of d:\n')
    q = input('Type order of q:\n')
    return int(p), int(d), int(q)

# ask if want automatic p,d,q input or manually by checking ACF and PACF plots
# courtesy of code from: https://github.com/alkaline-ml/pmdarima?tab=readme-ov-file
is_auto = input('Type auto or manual for automatic input or manual input:\n').strip()

if is_auto == 'auto':
    m_str = input('What interval is the dataset?\nType: daily/monthly/yearly and anything else for non-seasonality\n').lower().strip()

    if m_str == 'daily':
        m = 7
    elif m_str == 'monthly':
        m = 12
    else:
        m = 1

    # define and fit pipeline
    pipeline = Pipeline([
        ('boxcox', BoxCoxEndogTransformer(lmbda2=1e-6)),
        ('arima', pm.AutoARIMA(seasonal=True, m=m,
                               suppress_warnings=True,
                               trace=True, max_order=12))
    ])
    model_fit = pipeline.fit(train)

    # save model
    with open(os.path.join(res_path, f'{table_name}.pkl'), 'wb') as f_out:
        pickle.dump(model_fit, f_out)

    print(model_fit.summary())

else:
    p, d, q = plot_acf_pacf(train)
    # fit ARIMA model
    order = [p, d, q]  
    pipeline = Pipeline([('boxcox', BoxCoxEndogTransformer(lmbda2=1e-6)),
     ('arima', ARIMA(order=order))
     ])
    model_fit = pipeline.fit(train)

    # save model
    with open(os.path.join(res_path, f'{table_name}.pkl'), 'wb') as f_out:
        pickle.dump(model_fit, f_out)

    print(model_fit.summary())

# make predictions
#predictions = model_fit.predict(start=len(train), end=len(train) + len(test) - 1, typ='levels')
pred, confint = model_fit.predict(n_periods=test.shape[0], return_conf_int=True)

# make prediction a series
pred_series = pd.Series(pred)
pred_series.index = test.index

# make confidence intervals a dataframe
ci_df = pd.DataFrame(confint, columns = ['lower', 'upper'], index = test.index)

'''#predictions_cumsum = predictions.cumsum()
#predicted_prices = pd.Series(data['Close'].iloc[train_size] + predictions_cumsum, index=test.index)

# Fill NaN values at the beginning (if any)
first_non_nan_index = predictions_cumsum.first_valid_index()
predictions_cumsum.loc[first_non_nan_index:] = data['Close'].iloc[train_size] + predictions_cumsum.loc[first_non_nan_index:]

# Create a Series with the adjusted predictions
predicted_prices = pd.Series(predictions_cumsum, index=test.index)'''

# visualize actual vs predicted prices
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Actual Stock Prices')
plt.plot(pred_series, label='Predicted Stock Prices')
plt.fill_between(ci_df.index, ci_df['lower'], ci_df['upper'], color='grey', alpha=0.3)
plt.title('Actual vs Predicted Stock Prices')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend()
plt.show()

# evaluate the model
#print(len(data['Close'][train_size:])) #problem here
#print(len(predicted_prices))
#for d in data['Close'][train_size:]:
#	print(d)
#print("~~~~~~~~~~~~~~~~~~~~")
#for p in predicted_prices:
#	print(p)

mse = mean_squared_error(test.values, pred_series.values)
print('Mean Squared Error:', mse)

