STEPS:

1. Please use lab3_p1/stock_editor.py to add any stock you want to your MySQL server!
DISCLAIMER:
PLEASE USE TIME INTERVAL: "1y"/"1mo"/"1d" for best results!
Honestly, 'max' time range sometimes contains unecessary data that skews the model
it's up to you, but I would just recommend to include only "5y"
Also if you include 'max' range and '1d' time interval,
	the model may be very slow at training

2. Please use lab3_p2/arima.py to create a model for your stock table
DISCLAIMER:
It saves the model on lab3_p2/results
Please don't move the model to somewhere else as mock_invest.py reads from this folder

3. Please run lab3_p2/mock_invest.py to run a mock investment
DISCLAIMER:
It saves a csv file of the portfolio at results as well!

Notes:
- The signal_gen.py is just a python script with a function that 
	contains signal generation functions
	
- Sometimes the model prediction is to never buy/sell and that happens when the
	Moving averages short term and long term never collides!
	
- Signal generation is based on simple moving averages crossing

- The database on MySQL used in the scripts is lab3 (that stores the tables)

- arima_imputed.py was our attempt at making an imputed version of arima but the
	resampling was tricky so we stopped
	
- The model is boxcox to an arima model 
	(manually typed p,d,q from seeing ACF and PACF plots)
	OR
	(using autoARIMA to try every combination and find lowest AIC)
