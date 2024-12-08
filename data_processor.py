import statsmodels.api as sm
import pandas as pd

class DataProcessor:

    @staticmethod
    def get_processed_data(pair_tickers, pair_closing_prices, pair_regression_model):
        if len(pair_tickers) > 2:   raise Exception("'pair_tickers' can't have more than 2 tickers")
        for ticker in pair_tickers:
            if ticker not in pair_closing_prices.columns:   raise Exception(f"'{ticker}' not found in pair_closing_prices dataframe")
        

        ticker1 = pair_closing_prices[pair_tickers[0]]
        ticker2 = pair_closing_prices[pair_tickers[1]]

        X_new = sm.add_constant(ticker1)
        Y_preds = pair_regression_model.predict(X_new)
        Y_actual = ticker2
        test_residuals = Y_actual - Y_preds
        test_residuals.name = 'current_residual'

        processed_data = pd.merge(
            left=pair_closing_prices,
            left_index=True,
            right=test_residuals,
            right_index=True
        )

        processed_data['date'] = processed_data.index

        processed_data['previous_residual'] = processed_data['current_residual'].shift(1)

        processed_data['residual_mean'] = pair_regression_model.resid.mean()
        processed_data['residual_std'] = pair_regression_model.resid.std()

        processed_data['res_overval_cutoff'] = pair_regression_model.resid.mean() + pair_regression_model.resid.std()
        processed_data['res_underval_cutoff'] = pair_regression_model.resid.mean() - pair_regression_model.resid.std()

        processed_data['res_overval_stoploss'] = pair_regression_model.resid.mean() + 2*pair_regression_model.resid.std()
        processed_data['res_underval_stoploss'] = pair_regression_model.resid.mean() - 2*pair_regression_model.resid.std()

        return processed_data






