
from sklearn.linear_model import LinearRegression
import yfinance as yf
import numpy as np
from scipy.stats import norm, t
from constants import training_period, testing_period, window, nu

def build_spread(ticker1, ticker2):

    # We start 2 months behind so that we have mu and sigma values for the trading period starting in 2023
    test_start, test_end = testing_period
    prices = yf.download([ticker1, ticker2], start=test_start, end=test_end, auto_adjust=True)['Close']
    prices[f'Log {ticker1}'] = np.log(prices[ticker1])
    prices[f'Log {ticker2}'] = np.log(prices[ticker2])

    returns1 = prices[f'Log {ticker1}'].diff()
    returns2 = prices[f'Log {ticker2}'].diff()

    #Construct hedge ratio, and shift by 1 to ensure our strategy is built on past data
    prices['Hedge Ratio'] = (
            returns2.rolling(252).cov(returns1) /
            returns1.rolling(252).var()
    )
    prices['Hedge Ratio'] = prices['Hedge Ratio'].shift(1)

    #Build the spread (which is lagged by 1 day since the hedge ratio is lagged by 1 day)
    prices['Spread'] = prices[f'Log {ticker2}'] - prices[f'Log {ticker1}'] * prices['Hedge Ratio']

    #Calculate Spread Volatility (for position sizing later)
    prices['Spread Volatility'] = (prices['Spread'].rolling(60).std().ewm(span=20).mean()).clip(lower=1e-3).shift(1)

    return prices

def add_z_score_signal(prices):
    #Z-Score Signal
    #Rolling 60 day window for mu and sigma (for z score)
    prices['Equilibrium'] = prices['Spread'].rolling(60).mean()
    prices['Volatility'] = prices['Spread'].rolling(60).std()
    prices['Z Score Signal'] = ((prices['Spread'] - prices['Equilibrium']) / prices['Volatility']).shift(1)
    #Normalizes onto 0 to 1 scale (to compare with copula signals)
    prices['Z Score Signal (Normalized)'] = norm.cdf(prices['Z Score Signal'])

    prices['Z Score enter_short_thr'] = 2
    prices['Z Score enter_long_thr'] = -2
    prices['Z Score exit_lower_thr'] = -0.25
    prices['Z Score exit_upper_thr'] = 0.25

    return prices

def add_gaussian_t_copula_signals(ticker1, ticker2, prices):

    returns1 = prices[f'Log {ticker1}'].diff()
    returns2 = prices[f'Log {ticker2}'].diff()

    # Initialize copula signal (0.5 is default probability value)
    prices['Gaussian Copula Signal'] = 0.5
    prices['t Copula Signal'] = 0.5

    for signal in ['Gaussian Copula', 't Copula']:

        # Rolling 60-day copula calculation using empirical CDF
        for i in range(window, len(prices)):

            # Take past 60 log returns for each stock
            r1_window = returns1.iloc[i - window:i]
            r2_window = returns2.iloc[i - window:i]

            def empirical_cdf(x_data, value):
                """Compute percentile of value relative to x"""
                return ((x_data < value).sum() + 0.5 * (x_data == value).sum()) / (len(x_data) + 1)

            # Convert to stock return distribution to uniform distribution with cdf
            # Now values between 0 and 1
            # Note: We smooth the values to avoid values that are exactly 0 or 1
            eps = 1e-6
            u1_window = [empirical_cdf(r1_window, r1_value) for r1_value in r1_window]
            u1_window = np.clip(u1_window, eps, 1 - eps)
            u2_window = [empirical_cdf(r2_window, r2_value) for r2_value in r2_window]
            u2_window = np.clip(u2_window, eps, 1 - eps)

            # Map uniform -> Gaussian or t space (standard normals)
            # Note: 1 of 3 if statements between Gaussian Copula and t Copula
            z1_window = norm.ppf(u1_window) if signal == 'Gaussian Copula' else t.ppf(u1_window, df=nu)
            z2_window = norm.ppf(u2_window) if signal == 'Gaussian Copula' else t.ppf(u2_window, df=nu)

            # Rolling correlation (over past 60 days)
            rho = np.corrcoef(z1_window, z2_window)[0, 1]

            # Current day stock return values (no data leakage since this is 1 day in the future)
            r1_today = returns1.iloc[i]
            r2_today = returns2.iloc[i]

            # Convert current day return to uniform
            u1_today = empirical_cdf(r1_window, r1_today)
            u1_today = np.clip(u1_today, eps, 1 - eps)
            u2_today = empirical_cdf(r2_window, r2_today)
            u2_today = np.clip(u2_today, eps, 1 - eps)

            # Convert uniform to Gaussian (standard normal)
            # Note: 2 of 3 if statements between Gaussian Copula and t Copula
            z1_today = norm.ppf(u1_today) if signal == 'Gaussian Copula' else t.ppf(u1_today, df=nu)
            z2_today = norm.ppf(u2_today) if signal == 'Gaussian Copula' else t.ppf(u2_today, df=nu)

            # Conditional probability mispricing (use norm.cdf for Gaussian Copula
            if signal == 'Gaussian Copula':
                term_1 = z1_today - rho * z2_today
                term_2 = 1 - rho ** 2
                conditional_prob = norm.cdf(term_1 / np.sqrt(term_2))
                prices.iloc[i, -2] = conditional_prob
            else:
                # For t Copula, we can use the cumulative distribution function of the t-distribution with adjusted degrees of freedom
                df_adj = nu * (1 - rho ** 2) / (1 + rho ** 2)
                term_1 = z1_today - rho * z2_today
                term_2 = (1 - rho ** 2) * (nu + z2_today ** 2) / (nu + 1)
                conditional_prob = t.cdf(term_1 / np.sqrt(term_2), df=nu + 1)
                # print(term_1, term_2, conditional_prob)
                prices.iloc[i, -1] = conditional_prob

    signal_smoothed = prices[f'Gaussian Copula Signal']
    prices['Gaussian Copula enter_short_thr'] = signal_smoothed.rolling(window).quantile(0.85).shift(1)
    prices['Gaussian Copula enter_long_thr'] = signal_smoothed.rolling(window).quantile(0.15).shift(1)
    prices['Gaussian Copula exit_lower_thr'] = signal_smoothed.rolling(window).quantile(0.40).shift(1)
    prices['Gaussian Copula exit_upper_thr'] = signal_smoothed.rolling(window).quantile(0.60).shift(1)

    signal_smoothed = prices[f't Copula Signal']
    prices['t Copula enter_short_thr'] = signal_smoothed.rolling(window).quantile(0.85).shift(1)
    prices['t Copula enter_long_thr'] = signal_smoothed.rolling(window).quantile(0.15).shift(1)
    prices['t Copula exit_lower_thr'] = signal_smoothed.rolling(window).quantile(0.40).shift(1)
    prices['t Copula exit_upper_thr'] = signal_smoothed.rolling(window).quantile(0.60).shift(1)

    #Centered around 0
    prices['Gaussian Copula Signal (Normalized)'] = prices['Gaussian Copula Signal'] - 0.5
    prices['t Copula Signal (Normalized)'] = prices['t Copula Signal'] - 0.5

    return prices

def add_hybrid_signal_average(prices):
    # Simple average of the 3 signals
    prices['Hybrid (Average) Signal'] = (prices['Z Score Signal (Normalized)']
                               + prices['Gaussian Copula Signal (Normalized)']
                               + prices['t Copula Signal (Normalized)']) / 3


    signal_smoothed = prices[f'Hybrid (Average) Signal']
    prices['Hybrid (Average) enter_short_thr'] = signal_smoothed.rolling(window).quantile(0.85).shift(1)
    prices['Hybrid (Average) enter_long_thr'] = signal_smoothed.rolling(window).quantile(0.15).shift(1)
    prices['Hybrid (Average) exit_lower_thr'] = signal_smoothed.rolling(window).quantile(0.40).shift(1)
    prices['Hybrid (Average) exit_upper_thr'] = signal_smoothed.rolling(window).quantile(0.60).shift(1)
    return prices

def add_hybrid_signal_regression(prices):

    X = prices.loc[:, ['Z Score Signal (Normalized)', 'Gaussian Copula Signal (Normalized)', 't Copula Signal (Normalized)']]
    #y is Daily Spread Change
    y = prices['Spread'].shift(-1) - prices['Spread']
    lin_reg = LinearRegression()

    prices['Z Score Signal (Weight)'] = 0.0
    prices['Gaussian Copula Signal (Weight)'] = 0.0
    prices['t Copula Signal (Weight)'] = 0.0
    prices['Hybrid (Regression) Signal'] = 0.0

    for i in range(window, len(prices)):

        X_window = X.iloc[i - window:i, :].fillna(0)
        y_window = y.iloc[i - window:i].fillna(0)
        X_today = X.iloc[i, :].values.reshape(-1, )
        # print(X_window)
        lin_reg.fit(X_window, y_window)
        weights = lin_reg.coef_
        intercept = lin_reg.intercept_
        prices.iloc[i, -4] = weights[0]
        prices.iloc[i, -3] = weights[1]
        prices.iloc[i, -2] = weights[2]
        prices.iloc[i, -1] = weights[0] * X_today[0] + weights[1] * X_today[1] + weights[2] * X_today[2] + intercept


    signal_smoothed = prices[f'Hybrid (Regression) Signal']
    prices['Hybrid (Regression) enter_short_thr'] = signal_smoothed.rolling(window).quantile(0.85).shift(1)
    prices['Hybrid (Regression) enter_long_thr'] = signal_smoothed.rolling(window).quantile(0.15).shift(1)
    prices['Hybrid (Regression) exit_lower_thr'] = signal_smoothed.rolling(window).quantile(0.40).shift(1)
    prices['Hybrid (Regression) exit_upper_thr'] = signal_smoothed.rolling(window).quantile(0.60).shift(1)

    return prices

