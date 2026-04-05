import seaborn as sns
import matplotlib.pyplot as plt

def plot_cumulative_return(ticker1, ticker2, z_score_prices, gaussian_copula_prices, t_copula_prices):

    overall_max = max(z_score_prices['Cumulative Return'].max(), gaussian_copula_prices['Cumulative Return'].max(), t_copula_prices['Cumulative Return'].max())
    overall_min = min(z_score_prices['Cumulative Return'].min(), gaussian_copula_prices['Cumulative Return'].min(), t_copula_prices['Cumulative Return'].min())

    # Plot 1
    plt.subplot(3, 3, 1)
    plt.plot(z_score_prices.index, z_score_prices['Cumulative Return'], label='Z Score Return', color='blue')
    plt.plot(z_score_prices.index, [1] * len(z_score_prices.index), label='Baseline', color='red', ls='--')
    plt.title(f"({ticker1}, {ticker2}) -- Cumulative Return")
    plt.xlabel('Time')
    plt.ylabel('Cumulative Return')
    plt.title(f"({ticker1}, {ticker2}) -- Cumulative Return (Z Score)")
    plt.xticks(rotation=45)
    plt.ylim(overall_min * 0.9, overall_max * 1.1)
    plt.legend()

    # Plot 2
    plt.subplot(3, 3, 2)
    plt.plot(gaussian_copula_prices.index, gaussian_copula_prices['Cumulative Return'], label='Gaussian Copula Return', color='blue')
    plt.plot(gaussian_copula_prices.index, [1] * len(gaussian_copula_prices.index), label='Baseline', color='red', ls='--')
    plt.title(f"({ticker1}, {ticker2}) -- Cumulative Return")
    plt.xlabel('Time')
    plt.ylabel('Cumulative Return')
    plt.title(f"({ticker1}, {ticker2}) -- Cumulative Return (Gaussian Copula)")
    plt.xticks(rotation=45)
    plt.ylim(overall_min * 0.9, overall_max * 1.1)
    plt.legend()

    # Plot 3
    plt.subplot(3, 3, 3)
    plt.plot(t_copula_prices.index, t_copula_prices['Cumulative Return'], label='T Copula Return', color='blue')
    plt.plot(t_copula_prices.index, [1] * len(t_copula_prices.index), label='Baseline', color='red', ls='--')
    plt.title(f"({ticker1}, {ticker2}) -- Cumulative Return")
    plt.xlabel('Time')
    plt.ylabel('Cumulative Return')
    plt.title(f"({ticker1}, {ticker2}) -- Cumulative Return (T Copula)")
    plt.xticks(rotation=45)
    plt.ylim(overall_min * 0.9, overall_max * 1.1)
    plt.legend()

def plot_signals(ticker1, ticker2, z_score_prices, gaussian_copula_prices, t_copula_prices):

    plt.subplot(3, 3, 4)
    plt.plot(z_score_prices.index, z_score_prices['Z Score Signal'], label='Z Score Signal', color='purple')
    # plt.plot(z_score_prices.index, [signal_thresholds['Z Score']['enter_long']] * len(z_score_prices.index), label='Lower Threshold', color='red', ls='--')
    # plt.plot(z_score_prices.index, [signal_thresholds['Z Score']['enter_short']] * len(z_score_prices.index), label='Upper Threshold', color='red', ls='--')
    plt.plot(z_score_prices.index, z_score_prices['Z Score enter_long_thr'], label='Lower Threshold', color='red', ls='--')
    plt.plot(z_score_prices.index, z_score_prices['Z Score enter_short_thr'], label='Upper Threshold', color='red', ls='--')
    plt.xlabel('Time')
    plt.ylabel('Z Score Signal')
    plt.xticks(rotation=45)
    plt.title(f"({ticker1}, {ticker2}) -- Trading Signal (Z Score)")
    plt.legend()

    plt.subplot(3, 3, 5)
    plt.plot(gaussian_copula_prices.index, gaussian_copula_prices['Gaussian Copula Signal'], label='Gaussian Copula Signal', color='purple')
    # plt.plot(gaussian_copula_prices.index, [signal_thresholds['Gaussian Copula']['enter_long']] * len(gaussian_copula_prices.index), label='Lower Threshold', color='red', ls='--')
    # plt.plot(gaussian_copula_prices.index, [signal_thresholds['Gaussian Copula']['enter_short']] * len(gaussian_copula_prices.index), label='Upper Threshold', color='red', ls='--')
    plt.plot(gaussian_copula_prices.index, gaussian_copula_prices['Gaussian Copula enter_long_thr'], label='Lower Threshold', color='red', ls='--')
    plt.plot(gaussian_copula_prices.index, gaussian_copula_prices['Gaussian Copula enter_short_thr'], label='Upper Threshold', color='red', ls='--')
    plt.xlabel('Time')
    plt.ylabel('Gaussian Copula Signal')
    plt.xticks(rotation=45)
    plt.title(f"({ticker1}, {ticker2}) -- Trading Signal (Gaussian Copula)")
    plt.legend()

    plt.subplot(3, 3, 6)
    plt.plot(t_copula_prices.index, t_copula_prices['t Copula Signal'], label='t Copula Signal', color='purple')
    # plt.plot(t_copula_prices.index, [signal_thresholds['t Copula']['enter_long']] * len(t_copula_prices.index), label='Lower Threshold', color='red', ls='--')
    # plt.plot(t_copula_prices.index, [signal_thresholds['t Copula']['enter_short']] * len(t_copula_prices.index), label='Upper Threshold', color='red', ls='--')
    plt.plot(t_copula_prices.index, t_copula_prices['t Copula enter_long_thr'], label='Lower Threshold', color='red', ls='--')
    plt.plot(t_copula_prices.index, t_copula_prices['t Copula enter_short_thr'], label='Upper Threshold', color='red', ls='--')
    plt.xlabel('Time')
    plt.ylabel('t Copula Signal')
    plt.xticks(rotation=45)
    plt.title(f"({ticker1}, {ticker2}) -- Trading Signal (T Copula)")
    plt.legend()

def plot_positions(ticker1, ticker2, z_score_prices, gaussian_copula_prices, t_copula_prices):
    overall_max = max(z_score_prices['Position'].max(), gaussian_copula_prices['Position'].max(), t_copula_prices['Position'].max())
    overall_min = min(z_score_prices['Position'].min(), gaussian_copula_prices['Position'].min(), t_copula_prices['Position'].min())

    # Plot 1
    plt.subplot(3, 3, 7)
    plt.plot(z_score_prices.index, z_score_prices['Position'], label='Z Score Position', color='green')
    plt.plot(z_score_prices.index, [0] * len(z_score_prices.index), label='Baseline', color='red', ls='--')
    plt.xlabel('Time')
    plt.ylabel('Position')
    plt.xticks(rotation=45)
    plt.title(f"({ticker1}, {ticker2}) -- Position (Z Score)")
    plt.ylim(overall_min * 1.1, overall_max * 1.1)
    plt.legend()

    plt.subplot(3, 3, 8)
    plt.plot(gaussian_copula_prices.index, gaussian_copula_prices['Position'], label='Gaussian Copula Position', color='green')
    plt.plot(gaussian_copula_prices.index, [0] * len(gaussian_copula_prices.index), label='Baseline', color='red', ls='--')
    plt.xlabel('Time')
    plt.ylabel('Position')
    plt.xticks(rotation=45)
    plt.title(f"({ticker1}, {ticker2}) -- Position (Gaussian Copula)")
    plt.ylim(overall_min * 1.1, overall_max * 1.1)
    plt.legend()

    plt.subplot(3, 3, 9)
    plt.plot(t_copula_prices.index, t_copula_prices['Position'], label='t Copula Position', color='green')
    plt.plot(t_copula_prices.index, [0] * len(t_copula_prices.index), label='Baseline', color='red', ls='--')
    plt.xlabel('Time')
    plt.ylabel('Position')
    plt.xticks(rotation=45)
    plt.title(f"({ticker1}, {ticker2}) -- Position (t Copula)")
    plt.ylim(overall_min * 1.1, overall_max * 1.1)
    plt.legend()

def plot_all(ticker1, ticker2, z_score_prices, gaussian_copula_prices, t_copula_prices):
    plt.figure(figsize=(18, 12))
    plot_cumulative_return(ticker1, ticker2, z_score_prices, gaussian_copula_prices, t_copula_prices)
    plot_signals(ticker1, ticker2, z_score_prices, gaussian_copula_prices, t_copula_prices)
    plot_positions(ticker1, ticker2, z_score_prices, gaussian_copula_prices, t_copula_prices)
    plt.suptitle(f"({ticker1}, {ticker2}) -- Pairs Trading Performance", fontsize=20)
    plt.tight_layout()
    plt.show()

def plot_hybrid(ticker1, ticker2, hybrid_average_prices, hybrid_regression_prices):
    plt.figure(figsize=(18, 12))

    # Plot 1
    plt.subplot(3, 2, 1)
    plt.plot(hybrid_average_prices.index, hybrid_average_prices['Cumulative Return'], label='Hybrid (Average) Return', color='blue')
    plt.plot(hybrid_average_prices.index, [1] * len(hybrid_average_prices.index), label='Baseline', color='red', ls='--')
    plt.title(f"({ticker1}, {ticker2}) -- Cumulative Return")
    plt.xlabel('Time')
    plt.ylabel('Cumulative Return')
    plt.title(f"({ticker1}, {ticker2}) -- Cumulative Return (Hybrid (Average))")
    plt.xticks(rotation=45)
    # plt.ylim(overall_min * 0.9, overall_max * 1.1)
    plt.legend()

    plt.subplot(3, 2, 2)
    plt.plot(hybrid_regression_prices.index, hybrid_regression_prices['Cumulative Return'], label='Hybrid (Regression) Return', color='blue')
    plt.plot(hybrid_regression_prices.index, [1] * len(hybrid_regression_prices.index), label='Baseline', color='red', ls='--')
    plt.title(f"({ticker1}, {ticker2}) -- Cumulative Return")
    plt.xlabel('Time')
    plt.ylabel('Cumulative Return')
    plt.title(f"({ticker1}, {ticker2}) -- Cumulative Return (Hybrid (Regression))")
    plt.xticks(rotation=45)
    # plt.ylim(overall_min * 0.9, overall_max * 1.1)
    plt.legend()

    plt.subplot(3, 2, 3)
    plt.plot(hybrid_average_prices.index, hybrid_average_prices['Hybrid (Average) Signal'], label='Hybrid (Average) Signal', color='purple')
    plt.plot(hybrid_average_prices.index, hybrid_average_prices['Hybrid (Average) enter_long_thr'], label='Lower Threshold', color='red', ls='--')
    plt.plot(hybrid_average_prices.index, hybrid_average_prices['Hybrid (Average) enter_short_thr'], label='Upper Threshold', color='red', ls='--')
    plt.xlabel('Time')
    plt.ylabel('Hybrid (Average) Signal')
    plt.xticks(rotation=45)
    plt.title(f"({ticker1}, {ticker2}) -- Trading Signal (Hybrid (Average))")
    plt.legend()

    plt.subplot(3, 2, 4)
    plt.plot(hybrid_regression_prices.index, hybrid_regression_prices['Hybrid (Regression) Signal'], label='Hybrid (Regression) Signal', color='purple')
    plt.plot(hybrid_average_prices.index, hybrid_regression_prices['Hybrid (Regression) enter_long_thr'], label='Lower Threshold', color='red', ls='--')
    plt.plot(hybrid_average_prices.index, hybrid_regression_prices['Hybrid (Regression) enter_short_thr'], label='Upper Threshold', color='red', ls='--')
    plt.xlabel('Time')
    plt.ylabel('Hybrid (Regression) Signal')
    plt.xticks(rotation=45)
    plt.title(f"({ticker1}, {ticker2}) -- Trading Signal (Hybrid (Regression))")
    plt.legend()

    plt.subplot(3, 2, 5)
    plt.plot(hybrid_average_prices.index, hybrid_average_prices['Position'], label='Hybrid (Average) Position', color='green')
    plt.plot(hybrid_average_prices.index, [0] * len(hybrid_average_prices.index), label='Baseline', color='red', ls='--')
    plt.xlabel('Time')
    plt.ylabel('Position')
    plt.xticks(rotation=45)
    plt.title(f"({ticker1}, {ticker2}) -- Position (Hybrid (Average))")
    # plt.ylim(overall_min * 1.1, overall_max * 1.1)
    plt.legend()

    plt.subplot(3, 2, 6)
    plt.plot(hybrid_regression_prices.index, hybrid_regression_prices['Position'], label='Hybrid (Regression) Position', color='green')
    plt.plot(hybrid_regression_prices.index, [0] * len(hybrid_regression_prices.index), label='Baseline', color='red', ls='--')
    plt.xlabel('Time')
    plt.ylabel('Position')
    plt.xticks(rotation=45)
    plt.title(f"({ticker1}, {ticker2}) -- Position (Hybrid (Regression))")
    # plt.ylim(overall_min * 1.1, overall_max * 1.1)
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_hybrid_weights(ticker1, ticker2, hybrid_regression_prices):
    plt.figure(figsize=(12, 6))
    plt.plot(hybrid_regression_prices.index, hybrid_regression_prices['Z Score Signal (Weight)'], label='Z Score Weight', color='blue')
    plt.plot(hybrid_regression_prices.index, hybrid_regression_prices['Gaussian Copula Signal (Weight)'], label='Gaussian Copula Weight', color='orange')
    plt.plot(hybrid_regression_prices.index, hybrid_regression_prices['t Copula Signal (Weight)'], label='t Copula Weight', color='green')
    plt.xlabel('Time')
    plt.ylabel('Hybird Regression Weights')
    plt.xticks(rotation=45)
    plt.title(f"({ticker1}, {ticker2}) -- Hybrid Regression Weights Over Time")
    plt.legend()
    plt.show()

def plot_real_prices(ticker1, ticker2, prices):
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(prices.index, prices[ticker1], label=f'{ticker1} Price', color='blue')
    plt.plot(prices.index, prices[ticker2], label=f'{ticker2} Price', color='orange')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.title(f"({ticker1}, {ticker2}) -- Real Prices Over Time")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(prices.index, prices[f'Log {ticker1}'], label=f'{ticker1} Price (Log)', color='blue')
    plt.plot(prices.index, prices[f'Log {ticker2}'], label=f'{ticker2} Price (Log)', color='orange')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.title(f"({ticker1}, {ticker2}) -- Log Prices Over Time")
    plt.legend()

    plt.tight_layout()
    plt.show()


def plot_summary_df(ticker1, ticker2, summary_df):

    plt.figure(figsize=(12, 12))
    df_row_norm = summary_df.sub(summary_df.mean(axis=1), axis=0).div(summary_df.std(axis=1), axis=0)
    sns.heatmap(
        df_row_norm,
        annot=summary_df.round(2),  # show original values
        fmt="",
        cmap="coolwarm",
        center=0
    )
    plt.suptitle(f"({ticker1}, {ticker2}) -- Performance Summary", fontsize=16)
    plt.show()