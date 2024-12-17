import pandas as pd

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

        self._total_capital = total_capital_allocated
        self._capital_investment = total_capital_allocated

        self._current_date = None
    
    def get_portfolio_equity_curve(self):
        realised_net_percs = pd.DataFrame(self._total_net_percs).set_index('date')
        notional_net_percs = pd.DataFrame(self._notional_net_percs).set_index('date')
        merged = pd.merge(
            left=realised_net_percs,
            left_index=True,
            right=notional_net_percs,
            right_index=True,
            how='outer'
        ).ffill().fillna(0)
        return merged['net_perc'] + merged['notional_net_perc'] + self._capital_investment
    
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
        return [open_position.get_strategy_id() for open_position in self.get_open_positions()]

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

    
    def get_total_capital(self):
        return getattr(self, '_total_capital')
    def get_capital_investment(self):
        return getattr(self, '_capital_investment')
    
    def deduct_from_total_capital(self, deduction):
        current_capital = self.get_total_capital()
        print (f'POSITION OPENED: CAPITAL DEDUCTED: - {round(deduction, 2)}; CAPITAL AVAILABLE: {round(current_capital - deduction, 2)}')
        return setattr(self, '_total_capital', current_capital - deduction)
    
    def add_to_total_capital(self, addition):
        current_capital = self.get_total_capital()
        print (f'POSITION CLOSED:    CAPITAL ADDED: + {round(addition, 2)}; CAPITAL AVAILABLE: {round(current_capital + addition, 2)}')
        return setattr(self, '_total_capital', current_capital + addition)