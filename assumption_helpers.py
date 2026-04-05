from sklearn.linear_model import LinearRegression
from statsmodels.tsa.stattools import adfuller
import yfinance as yf
import numpy as np
from constants import training_period

def cointegration_test(ticker1, ticker2, verbose=True):
    ''' Given 2 stocks, identifies if they are cointegrated in the training period (using Engle-Granger test)

    Args:
        - ticker1, ticker2 (str): stock tickers for the assets

    Return:
        - p_value_bool, p_value (bool, float): boolean for whether pair is cointegrated, and corresponding p_value'''

    train_start, train_end = training_period
    prices = yf.download([ticker1, ticker2], start=train_start, end=train_end, auto_adjust=True)['Close']
    log_prices = np.log(prices)
    lin_reg = LinearRegression()
    X = log_prices.loc[:, [ticker1]]
    y = log_prices[ticker2]
    lin_reg.fit(X, y)
    y_pred = lin_reg.predict(X)
    residuals = y - y_pred
    p_value = adfuller(residuals, regression='n', autolag='AIC')[1]
    if verbose:
        print('Is the Pair Cointegrated?')
        if p_value <= 0.20:
            print(f'{ticker1} & {ticker2}: Cointegrated! -- p-value: {round(p_value, 2)}')
        else:
            print(f'{ticker1} & {ticker2}: Not Cointegrated... -- p-value: {round(p_value, 2)}')

    return p_value <= 0.20, p_value

def is_spread_stationary(ticker1, ticker2, verbose=True):
    ''' Given 2 stocks, identifies if the spread is stationary in the training period

    Args:
        - ticker1, ticker2 (str): stock tickers for the assets

    Return:
        - p_value_bool, p_value (bool, float): boolean for whether pair's spread is stationary, and corresponding p_value'''

    train_start, train_end = training_period
    prices = yf.download([ticker1, ticker2], start=train_start, end=train_end, auto_adjust=True)['Close']
    prices[f'Log {ticker1}'] = np.log(prices[ticker1])
    prices[f'Log {ticker2}'] = np.log(prices[ticker2])

    # Find hedge ratio (coefficient of linear relationship between log prices)
    lin_reg = LinearRegression()
    lin_reg.fit(prices.loc[:, [f'Log {ticker1}']], prices[f'Log {ticker2}'])
    hedge_ratio = lin_reg.coef_
    # Calculate spread
    prices['Spread'] = prices[f'Log {ticker2}'] - prices[f'Log {ticker1}'] * hedge_ratio + lin_reg.intercept_

    p_value = adfuller(prices['Spread'])[1]
    if verbose:
        print('Is the Spread Stationary?')
        if p_value <= 0.20:
            print(f'Yes! Spread is Stationary (p_value = {round(p_value, 2)})')
        else:
            print(f'No! Spread is not Stationary (p_value = {round(p_value, 2)})')

    return p_value <= 0.20, p_value