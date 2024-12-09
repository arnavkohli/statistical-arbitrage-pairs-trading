class PairStrategy:
    def __init__(
        self,
        id,
        ticker1,
        ticker2,
        ticker1_wt,
        ticker2_wt,
        entry_condition_z_value,
        target_condition_z_value,
        stoploss_condition_z_value,
        target_perc,
        stoploss_perc):

        self._id = id

        self._ticker1 = ticker1
        self._ticker2 = ticker2

        self._ticker1_wt = ticker1_wt
        self._ticker2_wt = ticker2_wt

        self._entry_condition_z_value = entry_condition_z_value
        self._target_condition_z_value = target_condition_z_value
        self._stoploss_condition_z_value = stoploss_condition_z_value

        self._target_perc = target_perc
        self._stoploss_perc = stoploss_perc
    
    def get_id(self):
        return getattr(self, '_id')

    def get_ticker1(self):
        return getattr(self, '_ticker1')
    def get_ticker2(self):
        return getattr(self, '_ticker2')

    def get_ticker1_wt(self):
        return getattr(self, '_ticker1_wt')
    def get_ticker2_wt(self):
        return getattr(self, '_ticker2_wt')

    def get_entry_condition_z_value(self):
        return getattr(self, '_entry_condition_z_value')
    def get_target_condition_z_value(self):
        return getattr(self, '_target_condition_z_value')
    def get_stoploss_condition_z_value(self):
        return getattr(self, '_stoploss_condition_z_value')
    
    def get_target_perc(self):
        return getattr(self, '_target_perc')
    def get_stoploss_perc(self):
        return getattr(self, '_stoploss_perc')
    
