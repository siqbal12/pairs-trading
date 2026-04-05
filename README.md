To run the Pairs Trading Strategy:
- Go to pairs_trading.py
    - Type in the tickers you would like to trade and if you would like to include transaction costs
    - If the pair is cointegrated and its spread is stationary, then the trading strategy will begin!
        - This will produce 5 plots showcasing the results along with a pd.DataFrame of the strategy performance
    - Else,
        - The strategy will not run since this initial assumption is not verified
     
Some pairs which are cointegrated and whose spread is stationary:
- USO & UNG (Crude Oil ETF & Natural Gas ETF)
- KO & PEP (Coca-Cola & Pepsi)
- NVDA & AAPL (Nvidia & Apple)
