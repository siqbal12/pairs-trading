from constants import target_vol, cost_per_unit

def get_strategy_results(prices, verbose=False):

    # Average Return
    average_return = prices['Pairs Trading Return'].mean()
    annualized_return = average_return * 252
    if verbose:
        print('Average Return:', round(average_return, 2))
        print('Annualized Return:', round(annualized_return, 2))

    # Volatility
    vol = prices['Pairs Trading Return'].std()
    annual_vol = vol * (252 ** 0.5)
    if verbose:
        print('Volatility:', round(vol, 2))
        print('Annualized Volatility:', round(annual_vol, 2))

    # Sharpe Ratio
    sharpe = (annualized_return / annual_vol)
    if verbose:
        print('Sharpe Ratio:', round(sharpe, 2))

    # Max Drawdown
    peak = prices['Cumulative Return'].cummax()
    drawdown = (prices['Cumulative Return'] - peak) / peak
    max_drawdown = -1 * drawdown.min()
    if verbose:
        print('Max Drawdown:', round(max_drawdown, 2))

    return {'Average Return': average_return, 'Annualized Return': annualized_return,
            'Volatility': vol, 'Annualized Volatility': annual_vol,
            'Sharpe Ratio': sharpe, 'Max Drawdown': max_drawdown}

def fill_rolling_position(prices, signal):
    prices['Position'] = 0

    for i in range(1, len(prices)):
        prev_pos = prices['Position'].iloc[i-1]
        s = prices[f'{signal} Signal'].iloc[i]

        short_thr = prices[f'{signal} enter_short_thr'].iloc[i]
        long_thr  = prices[f'{signal} enter_long_thr'].iloc[i]
        exit_l    = prices[f'{signal} exit_lower_thr'].iloc[i]
        exit_u    = prices[f'{signal} exit_upper_thr'].iloc[i]

        if s >= short_thr:
            prices.iloc[i, prices.columns.get_loc('Position')] = -1
        elif s <= long_thr:
            prices.iloc[i, prices.columns.get_loc('Position')] = 1
        elif exit_l <= s <= exit_u:
            prices.iloc[i, prices.columns.get_loc('Position')] = 0
        else:
            prices.iloc[i, prices.columns.get_loc('Position')] = prev_pos

    return prices


def add_strategy_hybrid(ticker1, ticker2, prices, signal, position_sizing=True, transaction_costs_included=True):

    prices = fill_rolling_position(prices, signal)

    #If we are position sizing, size the position with respect to the spread volatility
    if position_sizing:
        prices['Position'] = prices['Position'] * (target_vol / prices['Spread Volatility'])
    #Shift to avoid lookahead bias
    prices['Position'] = prices['Position'].shift(1)

    # We can identify our position in
    prices[f'{ticker2} Position'] = prices['Position']
    prices[f'{ticker1} Position'] = -prices['Hedge Ratio'] * prices['Position']

    pos1_change = prices[f'{ticker1} Position'].diff().abs()
    pos2_change = prices[f'{ticker2} Position'].diff().abs()
    prices['Transaction Cost'] = cost_per_unit * (pos1_change + pos2_change) if transaction_costs_included else 0
    # Optional: add volatility scaling
    prices['Transaction Cost'] *= (1 + prices['Spread Volatility'])

    # Compute Profit n Loss (using regular price levels, NOT log prices)
    prices[f'{ticker1} Return'] = prices[f'{ticker1}'].pct_change()
    prices[f'{ticker2} Return'] = prices[f'{ticker2}'].pct_change()

    prices['Pairs Trading Return'] = (
            prices[f'{ticker1} Position'] * prices[f'{ticker1} Return'] +
            prices[f'{ticker2} Position'] * prices[f'{ticker2} Return'] -
            prices['Transaction Cost']
    )

    prices['Cumulative Return'] = (1 + prices['Pairs Trading Return']).cumprod()

    strategy_results = get_strategy_results(prices)

    return prices, strategy_results

