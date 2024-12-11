import pandas as pd
import statsmodels.api as sm

from objects.signalprocessor import SignalProcessor
from objects.positionmanager import PositionManager

class PairsBacktester:
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
    
    def get_closed_positions(self):
        return getattr(self, '_portfolio').get_closed_positions()
    
    def get_active_strategies(self):
        return getattr(self, '_portfolio').get_active_strategy_ids()
    
    def get_pair_strategies(self):
        return getattr(self, '_pair_strategies')
    
    def find_pair_strategy_by_id(self, id):
        for strategy in self.get_pair_strategies():
            if strategy.get_id() == id:   return strategy
        raise Exception(f'strategy with id `{id}` not found')
    
    def check_for_exit_signals(self, data_row):
        # Iterate through all open positions
        for position in self.get_open_positions():
            # Lookup strategy object using strategy_id from position
            pair_strategy = self.find_pair_strategy_by_id(position.get_strategy_id())
            pair_position_type = position.get_type()
            if pair_position_type == 'underval':
                if SignalProcessor.underval_exit_signal(data_row, position, pair_strategy):
                    self.get_portfolio().exit_position(data_row, position)

            elif pair_position_type == 'overval':
                if SignalProcessor.overval_exit_signal(data_row, position, pair_strategy):
                    self.get_portfolio().exit_position(data_row, position)
        

    def check_for_entry_signals(self, data_row):
        # Filter out stratgies which are already running
        active_strategy_ids = self.get_active_strategies()
        inactive_strategies = [strategy for strategy in self.get_pair_strategies() if strategy.get_id() not in active_strategy_ids]
        
        for inactive_strategy in inactive_strategies:
            if SignalProcessor.overval_entry_signal(data_row, inactive_strategy):
                self.get_portfolio().enter_overval_position(data_row, inactive_strategy)
            elif SignalProcessor.underval_entry_signal(data_row, inactive_strategy):
                self.get_portfolio().enter_underval_position(data_row, inactive_strategy)

    def update_open_positions(self, data_row):
        for position in self.get_portfolio().get_open_positions():
            PositionManager.update_position_pnl(data_row, position)

    def log_open_positions(self, date):
        new_notional_abs_net = 0
        new_notional_net_perc = 0
        for position in self.get_portfolio().get_open_positions():
            summary = position.info()
            summary['date'] = date
            # self._daily_performance.append(summary)

            new_notional_abs_net += position.get_abs_net()
            new_notional_net_perc += position.get_abs_net() / self.get_portfolio().get_capital_investment()
        
        self.get_portfolio().set_notional_abs_net(date, new_notional_abs_net)
        self.get_portfolio().set_notional_net_perc(date, new_notional_net_perc)

    def log_closed_positions(self, date):
        for position in self.get_portfolio().get_closed_positions():
            if position.get_exit_date() == date:
                summary = position.info()
                summary['date'] = date
                # self._daily_performance.append(summary)

                self.get_portfolio().add_total_abs_net(date, position.get_abs_net())
                self.get_portfolio().add_total_net_perc(date, position.get_abs_net() / self.get_portfolio().get_capital_investment() )
    
    def trade(self):
        for date, data_row in self._data_feed.iterrows():
            
            ## Update current positions
            self.update_open_positions(data_row)

            self.check_for_exit_signals(data_row)

            self.check_for_entry_signals(data_row)

            # # Update open_positions

            self.log_open_positions(date)
            self.log_closed_positions(date)
        