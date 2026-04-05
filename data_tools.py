import pandas as pd
from assumption_helpers import cointegration_test, is_spread_stationary
from data_processing_helpers import build_spread, add_z_score_signal, add_gaussian_t_copula_signals, add_hybrid_signal_average, add_hybrid_signal_regression
from strategy_helpers import get_strategy_results, add_strategy_hybrid
from plotting_helpers import plot_all, plot_summary_df, plot_hybrid, plot_hybrid_weights, plot_real_prices

def data_processing(ticker1, ticker2):
    prices = build_spread(ticker1, ticker2)
    prices = add_z_score_signal(prices)
    prices = add_gaussian_t_copula_signals(ticker1, ticker2, prices)
    prices = add_hybrid_signal_average(prices)
    prices = add_hybrid_signal_regression(prices)
    prices = prices.dropna()
    return prices

def get_strategy_results(ticker1, ticker2, prices, visualize=True, transaction_costs_included=True):

    z_score_prices, z_score_results = add_strategy_hybrid(ticker1, ticker2, prices.copy(), signal='Z Score', transaction_costs_included=transaction_costs_included)
    gaussian_copula_prices, gaussian_copula_results = add_strategy_hybrid(ticker1, ticker2, prices.copy(), signal='Gaussian Copula', transaction_costs_included=transaction_costs_included)
    t_copula_prices, t_copula_results = add_strategy_hybrid(ticker1, ticker2, prices.copy(), signal='t Copula', transaction_costs_included=transaction_costs_included)
    hybrid_average_prices, hybrid_average_results = add_strategy_hybrid(ticker1, ticker2, prices.copy(), signal='Hybrid (Average)', transaction_costs_included=transaction_costs_included)
    hybrid_regression_prices, hybrid_regression_results = add_strategy_hybrid(ticker1, ticker2, prices.copy(), signal='Hybrid (Regression)', transaction_costs_included=transaction_costs_included)

    summary_dict = {'Annualized Return': [z_score_results['Annualized Return'], gaussian_copula_results['Annualized Return'], t_copula_results['Annualized Return'], hybrid_average_results['Annualized Return'], hybrid_regression_results['Annualized Return']],
                    'Annualized Volatility': [z_score_results['Annualized Volatility'], gaussian_copula_results['Annualized Volatility'], t_copula_results['Annualized Volatility'], hybrid_average_results['Annualized Volatility'], hybrid_regression_results['Annualized Volatility']],
                    'Sharpe Ratio': [z_score_results['Sharpe Ratio'], gaussian_copula_results['Sharpe Ratio'], t_copula_results['Sharpe Ratio'], hybrid_average_results['Sharpe Ratio'], hybrid_regression_results['Sharpe Ratio']],
                    'Max Drawdown': [z_score_results['Max Drawdown'], gaussian_copula_results['Max Drawdown'], t_copula_results['Max Drawdown'], hybrid_average_results['Max Drawdown'], hybrid_regression_results['Max Drawdown']]
                    }
    summary_df = pd.DataFrame(summary_dict, index=['Z Score', 'Gaussian Copula', 't Copula', 'Hybrid (Average)', 'Hybrid (Regression)']).T

    if visualize:
        plot_all(ticker1, ticker2, z_score_prices, gaussian_copula_prices, t_copula_prices)
        plot_hybrid(ticker1, ticker2, hybrid_average_prices, hybrid_regression_prices)
        plot_hybrid_weights(ticker1, ticker2, hybrid_regression_prices)
        plot_real_prices(ticker1, ticker2, prices)
        plot_summary_df(ticker1, ticker2, summary_df)
        print(summary_df)

    return summary_df

# def pairs_trading(ticker1, ticker2, transaction_costs_included=True):
#     cointegrated, p_value = cointegration_test(ticker1, ticker2)
#     stationary, p_value_stationarity = is_spread_stationary(ticker1, ticker2)
#     if cointegrated and stationary:
#         prices = data_processing(ticker1, ticker2)
#         summary_df = get_strategy_results(ticker1, ticker2, prices, transaction_costs_included=transaction_costs_included)
#         return summary_df, prices
#
#     #Try flipping to ticker2 & ticker1
#     cointegrated, p_value = cointegration_test(ticker2, ticker1)
#     stationary, p_value_stationarity = is_spread_stationary(ticker2, ticker1)
#     if cointegrated and stationary:
#         prices = data_processing(ticker2, ticker1)
#         summary_df = get_strategy_results(ticker2, ticker1, prices, transaction_costs_included=transaction_costs_included)
#         return summary_df, prices
#
#     return False, False
#
# strategy_df, prices = pairs_trading('PEP', 'KO', transaction_costs_included=True)