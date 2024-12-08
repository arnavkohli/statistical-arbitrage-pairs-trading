import pandas as pd
import statsmodels.api as sm



class PairBacktester:
    def __init__(
        self,
        portfolio,
        data_feed,
        pair_strategies):
    
        self._portfolio = portfolio
        self._data_feed = data_feed

        self._pair_strategies = pair_strategies

    def get_portfolio(self):
        return getattr(self, '_portfolio')
    
    def get_open_positions(self):
        return getattr(self, '_portfolio').get_open_positions()
    
    def get_active_strategies(self):
        return getattr(self, '_portfolio').get_active_strategy_ids()
    
    def get_pair_strategies(self):
        return getattr(self, '_pair_strategies')
    
    def find_pair_strategy_by_id(self, id):
        for strategy in self.get_pair_strategies():
            if strategy.get('_id') == id:   return strategy
        raise Exception(f'strategy with id `{id}` not found')
    
    def check_for_exit_signals(self, data_row):
        # Iterate through all open positions
        for position in self.get_open_positions():
            # Lookup strategy object using strategy_id from position
            pair_strategy = self.find_pair_strategy_by_id(position.get_strategy_id())

            if SignalProcessor.exit_signal(data_row, position, pair_strategy):
                self.get_portfolio().exit_position(
                    data_row,
                    position,
                    pair_strategy
                )

    def check_for_entry_signals(self, data_row):
        # Filter out stratgies which are already running
        active_strategy_ids = self.get_active_strategies()
        inactive_strategies = [strategy for strategy in self.get_pair_strategies() if strategy.get('_id') not in active_strategy_ids]
        
        for inactive_strategy in inactive_strategies:
            if SignalProcessor.entry_signal(data_row, inactive_strategy): # Add check for available funds
                self.get_portfolio().enter_position(
                    data_row=data_row,
                    strategy=inactive_strategy,
                )

    # def update_open_positions(self, data_row):
    #     for position in self.get_portfolio().get_open_positions():
    #         strategy = self.find_strategy_by_id(position.get('_strategy_id'))
    #         PositionManager.update_open_position_pnl(data_row, position)
    #         PositionManager.update_trailing_stoploss(data_row, position, strategy)

    # def log_open_positions(self, date):
    #     new_notional_abs_net = 0
    #     new_notional_net_perc = 0
    #     for position in self.get_portfolio().get_open_positions():
    #         summary = position.get_position_summary()
    #         summary['date'] = date
    #         self._daily_performance.append(summary)

    #         new_notional_abs_net += position.get_abs_net()
    #         # new_notional_net_perc += position.get_net_perc() * position.get('_capital_allocated_as_a_perc_of_total_capital')
        
    #     self.get_portfolio().set_notional_abs_net(date, new_notional_abs_net)
    #     self.get_portfolio().set_notional_net_perc(date, new_notional_net_perc)

    # def log_closed_positions(self, date):
    #     for position in self.get_portfolio().get_closed_positions():
    #         if position.get_exit_date() == date:
    #             summary = position.get_position_summary()
    #             summary['date'] = date
    #             self._daily_performance.append(summary)

    #             self.get_portfolio().add_total_abs_net(date, position.get_abs_net())
    #             # self.get_portfolio().add_total_net_perc(date, position.get('_net_perc') * position.get('_capital_allocated_as_a_perc_of_total_capital') )
    
    def trade(self):
        for date, data_row in self._data_feed.iterrows():
            
            ## Update current positions

            self.check_for_exit_signals(data_row)

            self.check_for_entry_signals(data_row)

            # Update open_positions
            self.update_open_positions(data_row)

            self.log_open_positions(date)
            self.log_closed_positions(date)
        


# class PairsBacktester:
#     def __init__(self, pairs_processed_data, ticker1, ticker2, ticker1_wt, ticker2_wt):
#         self._pairs_processed_data = pairs_processed_data
#         self._ticker1 = ticker1
#         self._ticker2 = ticker2

#         self._ticker1_wt = ticker1_wt
#         self._ticker2_wt = ticker2_wt

#         self._ticker_wts = {self._ticker1 : self._ticker1_wt, self._ticker2: self._ticker2_wt}

#         self.trades = []

#         self.realised_return = 0
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
#         self.current_trade['long_ticker_wt'] = self._ticker_wts[long_ticker]
#         self.current_trade['short_ticker_wt'] = self._ticker_wts[short_ticker]
    
#     def update_position_pnl(self, index, row):
#         self._pairs_processed_data.loc[index, 'long_pnl_perc'] = (row[self.current_trade['long_ticker']] - self.current_trade['long_entry_price']) / self.current_trade['long_entry_price']
#         self._pairs_processed_data.loc[index, 'short_pnl_perc'] = (self.current_trade['short_entry_price'] - row[self.current_trade['short_ticker']]) / self.current_trade['short_entry_price']
#         self._pairs_processed_data.loc[index, 'net_pnl_perc'] = self._pairs_processed_data.loc[index, 'long_pnl_perc']*self._ticker_wts[self.current_trade['long_ticker']] + \
#             self._pairs_processed_data.loc[index, 'short_pnl_perc']*self._ticker_wts[self.current_trade['short_ticker']] 

    
#     # def calculate_trade_statistics(self, equal_wts=True):
#     #     if len(self.trades) == 0:
#     #         return

#     #     self.trades['short_net_perc'] = (self.trades['short_entry_price'] - self.trades['short_exit_price']) / self.trades['short_entry_price']
#     #     self.trades['long_net_perc'] = (self.trades['long_exit_price'] - self.trades['long_entry_price']) / self.trades['long_entry_price']

#     #     self.trades['entry_date'] = pd.to_datetime(self.trades['entry_date'])
#     #     self.trades['exit_date'] = pd.to_datetime(self.trades['exit_date'])
#     #     self.trades['duration'] = (self.trades['exit_date'] - self.trades['entry_date']).apply(lambda x: pd.Timedelta(x).days)
        

#     #     if equal_wts:
#     #         self._ticker1_wt, self._ticker2_wt = 0.5, 0.5
#     #     else:
#     #         self._ticker1_wt = self.model.params[f'{self._ticker1}'] / (1 + self.model.params[f'{self._ticker1}'])
#     #         self._ticker2_wt = 1 / (1 + self.model.params[f'{self._ticker1}'])

#     #     self.trades['net_perc'] = self.trades.apply(
#     #         lambda row: (row['short_net_perc']*self._ticker2_wt + row['long_net_perc']*self._ticker1_wt) if row['short_ticker'] == self._ticker2 else \
#     #         (row['short_net_perc']*self._ticker1_wt + row['long_net_perc']*self._ticker2_wt), axis=1
#     #     )

#     def overval_trade_exit_signal(self, row):
#         return row['current_residual'] < row['residual_mean']
    

#     def check_for_overval_trade_exit(self, index, row):
#         # Exit trade overval trade
#         if row['current_residual'] < row['residual_mean']:

#             self._pairs_processed_data.loc[index, 'signal'] = 'exit overval: target'
#             self.in_overval_trade = False

#             self.realised_return += self._pairs_processed_data.loc[index, 'net_pnl_perc']

#             self.set_exit_info(
#                 exit_date=row['date'],
#                 short_exit_price=row[f'{self._ticker2}'],
#                 long_exit_price=row[f'{self._ticker1}'],
#                 exit_reason='target'
#             )

#             self.exit_trade()
        
#         elif row['current_residual'] > row['res_overval_stoploss']:

#             self._pairs_processed_data.loc[index, 'signal'] = 'exit overval: stoploss'
#             self.in_overval_trade = False

#             self.realised_return += self._pairs_processed_data.loc[index, 'net_pnl_perc']

#             self.set_exit_info(
#                 exit_date=row['date'],
#                 short_exit_price=row[f'{self._ticker2}'],
#                 long_exit_price=row[f'{self._ticker1}'],
#                 exit_reason='stoploss'
#             )

#             self.exit_trade()
    
#     def check_for_underval_trade_exit(self, index, row):
#         # Exit trade underval trade
#         if row['current_residual'] > row['residual_mean']:

#             self._pairs_processed_data.loc[index, 'signal'] = 'exit underval: target'
#             self.in_underval_trade = False

#             self.realised_return += self._pairs_processed_data.loc[index, 'net_pnl_perc']
            

#             self.set_exit_info(
#                 exit_date=row['date'],
#                 short_exit_price=row[f'{self._ticker1}'],
#                 long_exit_price=row[f'{self._ticker2}'],
#                 exit_reason='target'
#             )

#             self.exit_trade()
        
#         elif row['current_residual'] < row['res_underval_stoploss']:

#             self._pairs_processed_data.loc[index, 'signal'] = 'exit underval: stoploss'
#             self.in_underval_trade = False

#             self.realised_return += self._pairs_processed_data.loc[index, 'net_pnl_perc']
            

#             self.set_exit_info(
#                 exit_date=row['date'],
#                 short_exit_price=row[f'{self._ticker1}'],
#                 long_exit_price=row[f'{self._ticker2}'],
#                 exit_reason='stoploss'
#             )

#             self.exit_trade()
    
#     def check_for_overval_trade_entry(self, index, row):
#         if row['current_residual'] > row['res_overval_cutoff'] and row['previous_residual'] < row['res_overval_cutoff']:
#             self._pairs_processed_data.loc[index, 'signal'] = 'enter overval'
#             self.in_overval_trade = True

#             self.set_entry_info(
#                 pair=(self._ticker1, self._ticker2),
#                 residual_state='overval',
#                 entry_date=row['date'],
#                 short_ticker=self._ticker2,
#                 long_ticker=self._ticker1,
#                 short_entry_price=row[f'{self._ticker2}'],
#                 long_entry_price=row[f'{self._ticker1}']
#             )
    
#     def check_for_underval_trade_entry(self, index, row):
#         if row['current_residual'] < row['res_underval_cutoff'] and row['previous_residual'] > row['res_overval_cutoff']:
#             self._pairs_processed_data.loc[index, 'signal'] = 'enter underval'
#             self.in_underval_trade = True

#             self.set_entry_info(
#                 pair=(self._ticker1, self._ticker2),
#                 residual_state='underval',
#                 entry_date=row['date'],
#                 short_ticker=self._ticker1,
#                 long_ticker=self._ticker2,
#                 short_entry_price=row[f'{self._ticker1}'],
#                 long_entry_price=row[f'{self._ticker2}']
#             )
    
#     def trade(self):
#         for index, row in self._pairs_processed_data.iterrows():
#             # print (row)
#             if self.in_overval_trade:
#                 self.update_position_pnl(index, row)
#                 self.check_for_overval_trade_exit(index, row)


#             elif self.in_underval_trade:
#                 self.update_position_pnl(index, row)
#                 self.check_for_underval_trade_exit(index, row)

#             else:

#                 self.check_for_overval_trade_entry(index, row)

#                 self.check_for_underval_trade_entry(index, row)
            
#             self._pairs_processed_data.loc[index, 'realised_return'] = self.realised_return

#         self.trades = pd.DataFrame(self.trades)
#         # self.calculate_trade_statistics()      