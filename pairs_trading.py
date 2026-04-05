from assumption_helpers import cointegration_test, is_spread_stationary
from data_tools import data_processing, get_strategy_results

def pairs_trading(ticker1, ticker2, transaction_costs_included=True):
    cointegrated, p_value = cointegration_test(ticker1, ticker2)
    stationary, p_value_stationarity = is_spread_stationary(ticker1, ticker2)
    if cointegrated and stationary:
        prices = data_processing(ticker1, ticker2)
        summary_df = get_strategy_results(ticker1, ticker2, prices, transaction_costs_included=transaction_costs_included)
        return summary_df, prices

    #Try flipping to ticker2 & ticker1
    cointegrated, p_value = cointegration_test(ticker2, ticker1)
    stationary, p_value_stationarity = is_spread_stationary(ticker2, ticker1)
    if cointegrated and stationary:
        prices = data_processing(ticker2, ticker1)
        summary_df = get_strategy_results(ticker2, ticker1, prices, transaction_costs_included=transaction_costs_included)
        return summary_df, prices

    return False, False

#User inputs!
ticker1 = 'KO'
ticker2 = 'PEP'
transaction_costs_included = True

strategy_df, prices = pairs_trading(ticker1, ticker2, transaction_costs_included=transaction_costs_included)

x = True
