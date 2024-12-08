class PairPosition:
    def __init__(
        self,
        id,
        strategy_id,
        long_ticker,
        short_ticker,
        long_ticker_wt,
        short_ticker_wt,
        entry_date,
        long_entry_price,
        short_entry_price):
        # capital_allocated_as_a_perc_of_total_capital

        self._id = id
        self._strategy_id = strategy_id

        self._long_ticker = long_ticker
        self._short_ticker = short_ticker

        self._long_ticker_wt = long_ticker_wt
        self._short_ticker_wt = short_ticker_wt

        self._entry_date = entry_date

        self._long_entry_price = long_entry_price
        self._short_entry_price = short_entry_price

        # self._capital_allocated_as_a_perc_of_total_capital = capital_allocated_as_a_perc_of_total_capital

        self._exit_date = None

        self._long_exit_price = None
        self._short_exit_price = None

        self._abs_net = 0
        self._net_perc = 0
    
    def get_strategy_id(self):
        return getattr(self, '_strategy_id')

    def get_long_ticker(self):
        return getattr(self, '_long_ticker')
    def get_short_ticker(self):
        return getattr(self, '_short_ticker')

    def get_long_ticker_wt(self):
        return getattr(self, '_long_ticker_wt')
    def get_short_ticker_wt(self):
        return getattr(self, '_short_ticker_wt')

    def get_entry_date(self):
        return getattr(self, '_entry_date')
    
    def get_long_entry_price(self):
        return getattr(self, '_long_entry_price')
    def get_short_entry_price(self):
        return getattr(self, '_short_entry_price')
    
    def get_exit_date(self):
        return getattr(self, '_exit_date')
    def set_exit_date(self, exit_date):
        return setattr(self, '_exit_date', exit_date)
    
    def get_long_exit_price(self):
        return getattr(self, '_long_exit_price')
    def set_long_exit_price(self, long_exit_price):
        return setattr(self, '_long_exit_price', long_exit_price)
    
    def get_short_exit_price(self):
        return getattr(self, '_short_exit_price')
    def set_short_exit_price(self, short_exit_price):
        return setattr(self, '_long_exit_price', short_exit_price)
    
    def get_abs_net(self):
        return getattr(self, '_abs_net')
    def set_abs_net(self, abs_net):
        return setattr(self, '_abs_net', abs_net)

    def get_net_perc(self):
        return getattr(self, '_net_perc')
    def set_net_perc(self, net_perc):
        return setattr(self, '_net_perc', net_perc)
    
    def compute_long_perc(self, current_long_price):
        entry_price = self.get_long_entry_price()
        return (current_long_price - entry_price) / entry_price
    
    def compute_short_perc(self, current_short_price):
        entry_price = self.get_short_entry_price()
        return (entry_price - current_short_price) / entry_price
    
    def compute_net_perc(self, current_long_price, current_short_price):
        long_perc = self.compute_long_perc(current_long_price)
        long_wt = self.get_long_ticker_wt()
        short_perc = self.compute_short_perc(current_short_price)
        short_wt = self.get_short_ticker_wt()
        return long_perc*long_wt + short_perc*short_wt
    
        

        