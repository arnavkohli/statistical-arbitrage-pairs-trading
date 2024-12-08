import pandas as pd
import statsmodels.api as sm



class PairsBacktester:
    def __init__(self, pairs_processed_data, ticker1, ticker2, ticker1_wt, ticker2_wt):
        self._pairs_processed_data = pairs_processed_data
        self._ticker1 = ticker1
        self._ticker2 = ticker2

        self._ticker1_wt = ticker1_wt
        self._ticker2_wt = ticker2_wt

        self._ticker_wts = {self._ticker1 : self._ticker1_wt, self._ticker2: self._ticker2_wt}

        self.trades = []

        self.realised_return = 0
        # Temp variables to store trade data
        self.current_trade = {}

        # Denotes if an overvalued residual trade is active (curr_residual > residual_mean + residual_std)
        self.in_overval_trade = False

        # Denotes if an undervalued residual trade is active (curr_residual < residual_mean - residual_std)
        self.in_underval_trade = False
    
    def exit_trade(self):
        self.trades.append(self.current_trade) 
        self.current_trade = {}
    
    def set_exit_info(self, exit_date, short_exit_price, long_exit_price, exit_reason):
        self.current_trade['exit_date'] = exit_date
        self.current_trade['short_exit_price'] = short_exit_price
        self.current_trade['long_exit_price'] = long_exit_price
        self.current_trade['exit_reason'] = exit_reason
    
    def set_entry_info(self, pair, residual_state, entry_date, short_ticker, long_ticker, short_entry_price, long_entry_price):
        self.current_trade['pair'] = pair
        self.current_trade['residual_state'] = residual_state
        self.current_trade['entry_date'] = entry_date
        self.current_trade['short_ticker'] = short_ticker
        self.current_trade['long_ticker'] = long_ticker
        self.current_trade['short_entry_price'] = short_entry_price
        self.current_trade['long_entry_price'] = long_entry_price
    
    def update_position_pnl(self, index, row):
        self._pairs_processed_data.loc[index, 'long_pnl_perc'] = (row[self.current_trade['long_ticker']] - self.current_trade['long_entry_price']) / self.current_trade['long_entry_price']
        self._pairs_processed_data.loc[index, 'short_pnl_perc'] = (self.current_trade['short_entry_price'] - row[self.current_trade['short_ticker']]) / self.current_trade['short_entry_price']
        self._pairs_processed_data.loc[index, 'net_pnl_perc'] = self._pairs_processed_data.loc[index, 'long_pnl_perc']*self._ticker_wts[self.current_trade['long_ticker']] + \
            self._pairs_processed_data.loc[index, 'short_pnl_perc']*self._ticker_wts[self.current_trade['short_ticker']] 

    
    def calculate_trade_statistics(self, equal_wts=True):
        if len(self.trades) == 0:
            return

        self.trades['short_net_perc'] = (self.trades['short_entry_price'] - self.trades['short_exit_price']) / self.trades['short_entry_price']
        self.trades['long_net_perc'] = (self.trades['long_exit_price'] - self.trades['long_entry_price']) / self.trades['long_entry_price']

        self.trades['entry_date'] = pd.to_datetime(self.trades['entry_date'])
        self.trades['exit_date'] = pd.to_datetime(self.trades['exit_date'])
        self.trades['duration'] = (self.trades['exit_date'] - self.trades['entry_date']).apply(lambda x: pd.Timedelta(x).days)
        

        if equal_wts:
            self._ticker1_wt, self._ticker2_wt = 0.5, 0.5
        else:
            self._ticker1_wt = self.model.params[f'{self._ticker1}'] / (1 + self.model.params[f'{self._ticker1}'])
            self._ticker2_wt = 1 / (1 + self.model.params[f'{self._ticker1}'])

        self.trades['net_perc'] = self.trades.apply(
            lambda row: (row['short_net_perc']*self._ticker2_wt + row['long_net_perc']*self._ticker1_wt) if row['short_ticker'] == self._ticker2 else \
            (row['short_net_perc']*self._ticker1_wt + row['long_net_perc']*self._ticker2_wt), axis=1
        )
    
    def check_for_overval_trade_exit(self, index, row):
        # Exit trade overval trade
        if row['current_residual'] < row['residual_mean']:

            self._pairs_processed_data.loc[index, 'signal'] = 'exit overval: target'
            self.in_overval_trade = False

            self.realised_return += self._pairs_processed_data.loc[index, 'net_pnl_perc']
            # self._pairs_processed_data.loc[index, 'realised_return'] = self.realised_return

            self.set_exit_info(
                exit_date=row['date'],
                short_exit_price=row[f'{self._ticker2}'],
                long_exit_price=row[f'{self._ticker1}'],
                exit_reason='target'
            )

            self.exit_trade()
        
        elif row['current_residual'] > row['res_overval_stoploss']:

            self._pairs_processed_data.loc[index, 'signal'] = 'exit overval: stoploss'
            self.in_overval_trade = False

            self.realised_return += self._pairs_processed_data.loc[index, 'net_pnl_perc']
            # self._pairs_processed_data.loc[index, 'realised_return'] = self.realised_return

            self.set_exit_info(
                exit_date=row['date'],
                short_exit_price=row[f'{self._ticker2}'],
                long_exit_price=row[f'{self._ticker1}'],
                exit_reason='stoploss'
            )

            self.exit_trade()
    
    def check_for_underval_trade_exit(self, index, row):
        # Exit trade underval trade
        if row['current_residual'] > row['residual_mean']:

            self._pairs_processed_data.loc[index, 'signal'] = 'exit underval: target'
            self.in_underval_trade = False

            self.realised_return += self._pairs_processed_data.loc[index, 'net_pnl_perc']
            # self._pairs_processed_data.loc[index, 'realised_return'] = self.realised_return
            

            self.set_exit_info(
                exit_date=row['date'],
                short_exit_price=row[f'{self._ticker1}'],
                long_exit_price=row[f'{self._ticker2}'],
                exit_reason='target'
            )

            self.exit_trade()
        
        elif row['current_residual'] < row['res_underval_stoploss']:

            self._pairs_processed_data.loc[index, 'signal'] = 'exit underval: stoploss'
            self.in_underval_trade = False

            self.realised_return += self._pairs_processed_data.loc[index, 'net_pnl_perc']
            # self._pairs_processed_data.loc[index, 'realised_return'] = self.realised_return
            

            self.set_exit_info(
                exit_date=row['date'],
                short_exit_price=row[f'{self._ticker1}'],
                long_exit_price=row[f'{self._ticker2}'],
                exit_reason='stoploss'
            )

            self.exit_trade()
    
    def check_for_overval_trade_entry(self, index, row):
        if row['current_residual'] > row['res_overval_cutoff'] and row['previous_residual'] < row['res_overval_cutoff']:
            self._pairs_processed_data.loc[index, 'signal'] = 'enter overval'
            self.in_overval_trade = True

            self.set_entry_info(
                pair=(self._ticker1, self._ticker2),
                residual_state='overval',
                entry_date=row['date'],
                short_ticker=self._ticker2,
                long_ticker=self._ticker1,
                short_entry_price=row[f'{self._ticker2}'],
                long_entry_price=row[f'{self._ticker1}']
            )
    
    def check_for_underval_trade_entry(self, index, row):
        if row['current_residual'] < row['res_underval_cutoff'] and row['previous_residual'] > row['res_overval_cutoff']:
            self._pairs_processed_data.loc[index, 'signal'] = 'enter underval'
            self.in_underval_trade = True

            self.set_entry_info(
                pair=(self._ticker1, self._ticker2),
                residual_state='underval',
                entry_date=row['date'],
                short_ticker=self._ticker1,
                long_ticker=self._ticker2,
                short_entry_price=row[f'{self._ticker1}'],
                long_entry_price=row[f'{self._ticker2}']
            )
    
    def trade(self):
        for index, row in self._pairs_processed_data.iterrows():
            # print (row)
            if self.in_overval_trade:
                self.update_position_pnl(index, row)
                self.check_for_overval_trade_exit(index, row)


            elif self.in_underval_trade:
                self.update_position_pnl(index, row)
                self.check_for_underval_trade_exit(index, row)

            else:

                self.check_for_overval_trade_entry(index, row)

                self.check_for_underval_trade_entry(index, row)
            
            self._pairs_processed_data.loc[index, 'realised_return'] = self.realised_return

        self.trades = pd.DataFrame(self.trades)
        self.calculate_trade_statistics()      
        

# class PairsBacktester:

#     def __init__(self, TESTING_DATA, ticker1, ticker2, model):
#         self._ticker1 = ticker1
#         self._ticker2 = ticker2 
#         self.model = model

#         self.residuals = model.resid
#         row['residual_mean'] = self.residuals.mean()
#         row['residual_std'] = self.residuals.std()

#         row['res_overval_cutoff'] = row['residual_mean'] + row['residual_std']
#         row['res_underval_cutoff'] = row['residual_mean'] - row['residual_std']

#         row['res_overval_stoploss'] = row['residual_mean'] + 2*row['residual_std']
#         row['res_underval_stoploss'] = row['residual_mean'] - 2*row['residual_std']

#         self.data1 = TESTING_DATA[[ticker1]].squeeze()
#         self.data2 = TESTING_DATA[[ticker2]].squeeze()
#         self._pairs_processed_data = pd.merge(
#             left=self.data1,
#             left_index=True,
#             right=self.data2,
#             right_index=True
#         )


#         X_new = sm.add_constant(self.data1)
#         Y_preds = self.model.predict(X_new)
#         Y_actual = self.data2
#         test_residuals = Y_actual - Y_preds


#         # print (test_residuals)
#         test_residuals = pd.DataFrame({
#             'date': test_residuals.index,
#             'residual': test_residuals.values
#         })
        
#         self._pairs_processed_data = pd.merge(
#             left=self._pairs_processed_data,
#             left_index=True,
#             right=test_residuals,
#             right_on='date'
#         )

#         self._pairs_processed_data['prev_residual'] = self._pairs_processed_data['residual'].shift(1)
#         self._pairs_processed_data['signal'] = 'None'

#         self.trades = []

#         # Temp variables to store trade data
#         self.current_trade = {}

#         # Denotes if an overvalued residual trade is active (curr_residual > residual_mean + residual_std)
#         self.in_overval_trade = False

#         # Denotes if an undervalued residual trade is active (curr_residual < residual_mean - residual_std)
#         self.in_underval_trade = False

#     def exit_trade(self):
#         self.trades.append(self.current_trade)
#         self.current_trade = {}
    
#     def set_exit_info(self, exit_date, short_exit_price, long_exit_price, exit_reason):
#         self.current_trade['exit_date'] = exit_date
#         self.current_trade['short_exit_price'] = short_exit_price
#         self.current_trade['long_exit_price'] = long_exit_price
#         self.current_trade['exit_reason'] = exit_reason
    
#     def set_entry_info(self, pair, residual_state, entry_date, short_ticker, long_ticker, short_entry_price, long_entry_price):
#         self.current_trade['pair'] = pair
#         self.current_trade['residual_state'] = residual_state
#         self.current_trade['entry_date'] = entry_date
#         self.current_trade['short_ticker'] = short_ticker
#         self.current_trade['long_ticker'] = long_ticker
#         self.current_trade['short_entry_price'] = short_entry_price
#         self.current_trade['long_entry_price'] = long_entry_price
    
#     def calculate_trade_statistics(self, equal_wts=True):
#         if len(self.trades) == 0:
#             return

#         self.trades['short_net_perc'] = (self.trades['short_entry_price'] - self.trades['short_exit_price']) / self.trades['short_entry_price']
#         self.trades['long_net_perc'] = (self.trades['long_exit_price'] - self.trades['long_entry_price']) / self.trades['long_entry_price']

#         self.trades['entry_date'] = pd.to_datetime(self.trades['entry_date'])
#         self.trades['exit_date'] = pd.to_datetime(self.trades['exit_date'])
#         self.trades['duration'] = (self.trades['exit_date'] - self.trades['entry_date']).apply(lambda x: pd.Timedelta(x).days)
        

#         if equal_wts:
#             self._ticker1_wt, self._ticker2_wt = 0.5, 0.5
#         else:
#             self._ticker1_wt = self.model.params[f'{self._ticker1}'] / (1 + self.model.params[f'{self._ticker1}'])
#             self._ticker2_wt = 1 / (1 + self.model.params[f'{self._ticker1}'])

#         self.trades['net_perc'] = self.trades.apply(
#             lambda row: (row['short_net_perc']*self._ticker2_wt + row['long_net_perc']*self._ticker1_wt) if row['short_ticker'] == self._ticker2 else \
#             (row['short_net_perc']*self._ticker1_wt + row['long_net_perc']*self._ticker2_wt), axis=1
#         )
    
#     def trade(self):
#         for index, row in self._pairs_processed_data.iterrows():
#             if self.in_overval_trade:
#                 # Exit trade overval trade
#                 if row['residual'] < row['residual_mean']:

#                     self._pairs_processed_data.loc[index, 'signal'] = 'exit overval: target'
#                     self.in_overval_trade = False

#                     self.set_exit_info(
#                         exit_date=row['date'],
#                         short_exit_price=row[f'{self._ticker2}'],
#                         long_exit_price=row[f'{self._ticker1}'],
#                         exit_reason='target'
#                     )

#                     self.exit_trade()
                
#                 elif row['residual'] > row['res_overval_stoploss']:

#                     self._pairs_processed_data.loc[index, 'signal'] = 'exit overval: stoploss'
#                     self.in_overval_trade = False

#                     self.set_exit_info(
#                         exit_date=row['date'],
#                         short_exit_price=row[f'{self._ticker2}'],
#                         long_exit_price=row[f'{self._ticker1}'],
#                         exit_reason='stoploss'
#                     )

#                     self.exit_trade()


#             elif self.in_underval_trade:
#                 # Exit trade underval trade
#                 if row['residual'] > row['residual_mean']:

#                     self._pairs_processed_data.loc[index, 'signal'] = 'exit underval: target'
#                     self.in_underval_trade = False
                    

#                     self.set_exit_info(
#                         exit_date=row['date'],
#                         short_exit_price=row[f'{self._ticker1}'],
#                         long_exit_price=row[f'{self._ticker2}'],
#                         exit_reason='target'
#                     )

#                     self.exit_trade()
                
#                 elif row['residual'] < row['res_underval_stoploss']:

#                     self._pairs_processed_data.loc[index, 'signal'] = 'exit underval: stoploss'
#                     self.in_underval_trade = False
                    

#                     self.set_exit_info(
#                         exit_date=row['date'],
#                         short_exit_price=row[f'{self._ticker1}'],
#                         long_exit_price=row[f'{self._ticker2}'],
#                         exit_reason='stoploss'
#                     )

#                     self.exit_trade()


#             else:

#                 if row['residual'] > row['res_overval_cutoff'] and row['prev_residual'] < row['res_overval_cutoff']:

#                     self._pairs_processed_data.loc[index, 'signal'] = 'enter overval'
#                     self.in_overval_trade = True

#                     self.set_entry_info(
#                         pair=(self._ticker1, self._ticker2),
#                         residual_state='overval',
#                         entry_date=row['date'],
#                         short_ticker=self._ticker2,
#                         long_ticker=self._ticker1,
#                         short_entry_price=row[f'{self._ticker2}'],
#                         long_entry_price=row[f'{self._ticker1}']
#                     )


#                 elif row['residual'] < row['res_underval_cutoff'] and row['prev_residual'] > row['res_overval_cutoff']:
#                     self._pairs_processed_data.loc[index, 'signal'] = 'enter underval'
#                     self.in_underval_trade = True

#                     self.set_entry_info(
#                         pair=(self._ticker1, self._ticker2),
#                         residual_state='underval',
#                         entry_date=row['date'],
#                         short_ticker=self._ticker1,
#                         long_ticker=self._ticker2,
#                         short_entry_price=row[f'{self._ticker1}'],
#                         long_entry_price=row[f'{self._ticker2}']
#                     )
#                 else:
#                     self._pairs_processed_data.loc[index, 'signal'] = 'none'

#         self.trades = pd.DataFrame(self.trades)
#         self.calculate_trade_statistics()      