import pandas as pd
import statsmodels.api as sm

class PairsBacktester:

    def __init__(self, TESTING_DATA, ticker1, ticker2, model):
        self.ticker1 = ticker1
        self.ticker2 = ticker2 
        self.model = model

        self.residuals = model.resid
        self.residuals_mean = self.residuals.mean()
        self.residuals_std = self.residuals.std()

        self.res_overval_cutoff = self.residuals_mean + self.residuals_std
        self.res_underval_cutoff = self.residuals_mean - self.residuals_std

        self.data1 = TESTING_DATA[[ticker1]].squeeze()
        self.data2 = TESTING_DATA[[ticker2]].squeeze()
        self.testing_data = pd.merge(
            left=self.data1,
            left_index=True,
            right=self.data2,
            right_index=True
        )


        X_new = sm.add_constant(self.data1)
        Y_preds = self.model.predict(X_new)
        Y_actual = self.data2
        test_residuals = Y_actual - Y_preds


        # print (test_residuals)
        test_residuals = pd.DataFrame({
            'date': test_residuals.index,
            'residual': test_residuals.values
        })
        
        self.testing_data = pd.merge(
            left=self.testing_data,
            left_index=True,
            right=test_residuals,
            right_on='date'
        )


        self.testing_data['signal'] = 'None'

        self.trades = []

        # Temp variables to store trade data
        self.current_trade = {}

        # Denotes if an overvalued residual trade is active (curr_residual > residual_mean + residual_std)
        self.in_overval_trade = False

        # Denotes if an undervalued residual trade is active (curr_residual < residual_mean - residual_std)
        self.in_underval_trade = False

    def exit_trade(self):
        self.trades.append(self.current_trade)
        self.current_trade = {}
    
    def set_exit_info(self, exit_date, short_exit_price, long_exit_price):
        self.current_trade['exit_date'] = exit_date
        self.current_trade['short_exit_price'] = short_exit_price
        self.current_trade['long_exit_price'] = long_exit_price
    
    def set_entry_info(self, pair, residual_state, entry_date, short_ticker, long_ticker, short_entry_price, long_entry_price):
        self.current_trade['pair'] = pair
        self.current_trade['residual_state'] = residual_state
        self.current_trade['entry_date'] = entry_date
        self.current_trade['short_ticker'] = short_ticker
        self.current_trade['long_ticker'] = long_ticker
        self.current_trade['short_entry_price'] = short_entry_price
        self.current_trade['long_entry_price'] = long_entry_price
    
    def calculate_trade_statistics(self, equal_wts=True):
        if len(self.trades) == 0:
            return

        self.trades['short_net_perc'] = (self.trades['short_entry_price'] - self.trades['short_exit_price']) / self.trades['short_entry_price']
        self.trades['long_net_perc'] = (self.trades['long_exit_price'] - self.trades['long_entry_price']) / self.trades['long_entry_price']

        self.trades['entry_date'] = pd.to_datetime(self.trades['entry_date'])
        self.trades['exit_date'] = pd.to_datetime(self.trades['exit_date'])
        self.trades['duration'] = (self.trades['exit_date'] - self.trades['entry_date']).apply(lambda x: pd.Timedelta(x).days)
        

        if equal_wts:
            self.ticker1_wt, self.ticker2_wt = 0.5, 0.5
        else:
            self.ticker1_wt = self.model.params[f'{self.ticker1}'] / (1 + self.model.params[f'{self.ticker1}'])
            self.ticker2_wt = 1 / (1 + self.model.params[f'{self.ticker1}'])

        self.trades['net_perc'] = self.trades.apply(
            lambda row: (row['short_net_perc']*self.ticker2_wt + row['long_net_perc']*self.ticker1_wt) if row['short_ticker'] == self.ticker2 else \
            (row['short_net_perc']*self.ticker1_wt + row['long_net_perc']*self.ticker2_wt), axis=1
        )
    
    def trade(self):
        for index, row in self.testing_data.iterrows():
            if self.in_overval_trade:
                # Exit trade overval trade
                if row['residual'] < self.residuals_mean:

                    self.testing_data.loc[index, 'signal'] = 'exit overval'
                    self.in_overval_trade = False

                    self.set_exit_info(
                        exit_date=row['date'],
                        short_exit_price=row[f'{self.ticker2}'],
                        long_exit_price=row[f'{self.ticker1}']
                    )

                    self.exit_trade()

            elif self.in_underval_trade:
                # Exit trade underval trade
                if row['residual'] > self.residuals_mean:

                    self.testing_data.loc[index, 'signal'] = 'exit underval'
                    self.in_underval_trade = False
                    

                    self.set_exit_info(
                        exit_date=row['date'],
                        short_exit_price=row[f'{self.ticker1}'],
                        long_exit_price=row[f'{self.ticker2}']
                    )

                    self.exit_trade()

            else:

                if row['residual'] > self.res_overval_cutoff:

                    self.testing_data.loc[index, 'signal'] = 'enter overval'
                    self.in_overval_trade = True

                    self.set_entry_info(
                        pair=(self.ticker1, self.ticker2),
                        residual_state='overval',
                        entry_date=row['date'],
                        short_ticker=self.ticker2,
                        long_ticker=self.ticker1,
                        short_entry_price=row[f'{self.ticker2}'],
                        long_entry_price=row[f'{self.ticker1}']
                    )


                elif row['residual'] < self.res_underval_cutoff:
                    self.testing_data.loc[index, 'signal'] = 'enter underval'
                    self.in_underval_trade = True

                    self.set_entry_info(
                        pair=(self.ticker1, self.ticker2),
                        residual_state='underval',
                        entry_date=row['date'],
                        short_ticker=self.ticker1,
                        long_ticker=self.ticker2,
                        short_entry_price=row[f'{self.ticker1}'],
                        long_entry_price=row[f'{self.ticker2}']
                    )
                else:
                    self.testing_data.loc[index, 'signal'] = 'none'

        self.trades = pd.DataFrame(self.trades)
        self.calculate_trade_statistics()      