training_period = ('2021-01-01', '2024-01-01')
testing_period = ('2022-11-01', '2026-01-01')
target_vol=0.10
cost_per_unit=0.001
window=60
nu=5
signal_thresholds = {
    'Z Score': {
        'enter_short': 2,
        'enter_long': -2,
        'exit_lower': 0.25,
        'exit_upper': -0.25
    },
    'Gaussian Copula': {
        'enter_short': 0.95,
        'enter_long': 0.05,
        'exit_lower': 0.45,
        'exit_upper': 0.55
    },
    't Copula': {
        'enter_short': 0.95,
        'enter_long': 0.05,
        'exit_lower': 0.40,
        'exit_upper': 0.60
    }
}
