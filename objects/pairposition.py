class PairPosition:
    def __init__(
        self,
        id,
        type,
        strategy_id,
        long_ticker,
        short_ticker,
        long_ticker_wt,
        short_ticker_wt,
        entry_date,
        long_entry_price,
        short_entry_price,
        capital_allocated):

        self._id = id
        self._type = type
        self._strategy_id = strategy_id

        self._long_ticker = long_ticker
        self._short_ticker = short_ticker

        self._long_ticker_wt = long_ticker_wt
        self._short_ticker_wt = short_ticker_wt

        self._entry_date = entry_date

        self._long_entry_price = long_entry_price
        self._short_entry_price = short_entry_price

        self._capital_allocated = capital_allocated

        self._exit_date = None

        self._long_exit_price = None
        self._short_exit_price = None

        self._long_net_perc = 0
        self._short_net_perc = 0

        self._long_net_abs = 0
        self._short_net_abs = 0

        self._abs_net = 0
        self._net_perc = 0
    
    def get_id(self):
        return getattr(self, '_id')

    def get_strategy_id(self):
        return getattr(self, '_strategy_id')
    
    def get_type(self):
        return getattr(self, '_type')

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
        return setattr(self, '_short_exit_price', short_exit_price)
    
    def get_long_net_abs(self):
        return getattr(self, '_long_net_abs')
    def set_long_net_abs(self, long_net_abs):
        return setattr(self, '_long_net_abs', long_net_abs)
    
    def get_short_net_abs(self):
        return getattr(self, '_short_net_abs')
    def set_short_net_abs(self, short_net_abs):
        return setattr(self, '_short_net_abs', short_net_abs)
    
    def get_abs_net(self):
        return getattr(self, '_abs_net')
    def set_abs_net(self, abs_net):
        return setattr(self, '_abs_net', abs_net)

    def get_long_net_perc(self):
        return getattr(self, '_long_net_perc')
    def set_long_net_perc(self, long_net_perc):
        return setattr(self, '_long_net_perc', long_net_perc)
    
    def get_short_net_perc(self):
        return getattr(self, '_short_net_perc')
    def set_short_net_perc(self, short_net_perc):
        return setattr(self, '_short_net_perc', short_net_perc)

    def get_net_perc(self):
        return getattr(self, '_net_perc')
    def set_net_perc(self, net_perc):
        return setattr(self, '_net_perc', net_perc)
    
    def get_capital_allocated(self):
        return getattr(self, '_capital_allocated')

    def info(self):
        return {
            'id': self.get_id(),
            'type': self.get_type(),
            'strategy_id': self.get_strategy_id(),
            'long_ticker': self.get_long_ticker(),
            'short_ticker': self.get_short_ticker(),
            'long_ticker_wt': self.get_long_ticker_wt(),
            'short_ticker_wt': self.get_short_ticker_wt(),
            'entry_date': self.get_entry_date(),
            'exit_date': self.get_exit_date(),
            'long_entry_price': self.get_long_entry_price(),
            'long_exit_price': self.get_long_exit_price(),
            'long_net_abs': self.get_long_net_abs(),
            'long_net_perc': self.get_long_net_perc(),
            'short_entry_price': self.get_short_entry_price(),
            'short_exit_price': self.get_short_exit_price(),
            'short_net_abs': self.get_short_net_abs(),
            'short_net_perc': self.get_short_net_perc(),
            'net_perc': self.get_net_perc(),
            'net_abs': self.get_abs_net()

        }
    
        

        