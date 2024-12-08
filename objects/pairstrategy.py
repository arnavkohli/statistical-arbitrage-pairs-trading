class PairStrategy:
    def __init__(
        self,
        id,
        long_ticker,
        short_ticker,
        entry_conditions,
        exit_conditions,
        target_perc,
        stoploss_perc):

        self._long_ticker = long_ticker
        self._short_ticker = short_ticker

        self._entry_conditions = entry_conditions
        self._exit_conditions = exit_conditions

        self._target_perc = target_perc
        self._stoploss_perc = stoploss_perc
    
    def get_entry_conditions(self):
        return getattr(self, '_entry_conditions')
    def get_exit_conditions(self):
        return getattr(self, '_exit_conditions')
    
    def get_target_perc(self):
        return getattr(self, '_target_perc')
    def get_stoploss_perc(self):
        return getattr(self, '_stoploss_perc')
    
