from pairposition import PairPosition
from signalprocessor import SignalProcessor

class Portfolio:
    '''
        This class will only hold data regarding the portfolio.
    '''
    def __init__(self, total_capital_allocated):
        self._daily_performance = []

        self._total_positions = 0

        self._total_abs_net = 0
        self._total_net_perc = 0

        self._notional_abs_net = 0
        self._notional_net_perc = 0

        self._total_abs_nets = []
        self._total_net_percs = []

        self._notional_abs_nets = []
        self._notional_net_percs = []

        self._open_positions = []
        self._closed_positions = []

        self._total_capital_allocated = total_capital_allocated

        self._current_date = None
    
    def get_portfolio_net_percs(self):
        realised_net_percs = pd.DataFrame(self._total_net_percs).set_index('date')
        notional_net_percs = pd.DataFrame(self._notional_net_percs).set_index('date')
        merged = pd.merge(
            left=realised_net_percs,
            left_index=True,
            right=notional_net_percs,
            right_index=True,
            how='outer'
        ).ffill().fillna(0)
        merged['total_net_perc'] = merged['net_perc'] + merged['notional_net_perc']
        return merged
    
    def add_total_abs_net(self, date, abs_net):
        self._total_abs_net += abs_net
        self._total_abs_nets.append({'date': date, 'abs_net': self._total_abs_net})
    
    def add_total_net_perc(self, date, net_perc):
        self._total_net_perc += net_perc
        self._total_net_percs.append({'date': date, 'net_perc': self._total_net_perc})

    def set_notional_abs_net(self, date, notional_abs_net):
        self._notional_abs_net = notional_abs_net
        self._notional_abs_nets.append({'date': date, 'notional_abs_net': self._notional_abs_net})
    
    def set_notional_net_perc(self, date, notional_net_perc):
        self._notional_net_perc = notional_net_perc
        self._notional_net_percs.append({'date': date, 'notional_net_perc': self._notional_net_perc})
    
    def get(self, name):
        return getattr(self, name, None)
    
    def get_active_strategy_ids(self):
        return [open_position.get('_strategy_id') for open_position in self.get_open_positions()]

    def get_open_positions(self):
        return self._open_positions
    def append_open_position(self, position):
        self._open_positions.append(position)
    def remove_open_position(self, position):
        self._open_positions.remove(position)
    
    def get_closed_positions(self):
        return self._closed_positions
    def append_closed_position(self, position):
        self._closed_positions.append(position)
    def remove_closed_position(self, position):
        self._closed_positions.remove(position)
    
    def exit_position(self, data_row, position, strategy):
        date = data_row['date']

        if SignalProcessor.stoploss_hit(data_row, position):
            exit_price = ExecutionLayer.get_stoploss_fill_price(data_row, position)
        elif SignalProcessor.target_hit(data_row, position):
            exit_price = ExecutionLayer.get_target_fill_price(data_row, position)
        elif SignalProcessor.exit_condition_hit(data_row, position, strategy):
            exit_price = ExecutionLayer.get_exit_condition_fill_price(data_row, position, strategy)
        # Update exit information
        position.set_exit_date(date)
        position.set_exit_price(exit_price)
        # Update position data w.r.t. exit price
        PositionManager.update_closed_position_pnl(exit_price, position)
        # Update position status
        position.set_is_position_active(is_active=False)
        # Remove from open positions
        self.remove_open_position(position)
        # Append to closed positions
        self.append_closed_position(position)
    
    def enter_position(self, data_row, strategy):
        entry_date = data_row['date']
        entry_price = ExecutionLayer.get_entry_fill_price(data_row, strategy)

        capital_allocation_perc = strategy.get('_capital_allocation_perc')
        capital_allocated = self._total_capital_allocated * capital_allocation_perc

        new_position = PairPosition(

        )

        PositionManager.set_exit_prices(data_row, new_position, strategy)

        self.append_open_position(new_position)
        self._total_positions += 1

        return new_position