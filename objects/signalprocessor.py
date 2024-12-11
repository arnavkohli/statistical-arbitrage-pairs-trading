class SignalProcessor:
    
    @staticmethod
    def overval_entry_signal(data_row, strategy):
        overval_entry_condition_z_value = abs(strategy.get_entry_condition_z_value())
        strategy_id = strategy.get_id()
        return (data_row[f'{strategy_id}_residual'] > overval_entry_condition_z_value) and \
                (data_row[f'{strategy_id}_prev_residual'] < overval_entry_condition_z_value)

    @staticmethod
    def overval_target_signal(data_row, strategy):
        overval_target_condition_z_value = abs(strategy.get_target_condition_z_value())
        strategy_id = strategy.get_id()
        return data_row[f'{strategy_id}_residual'] < overval_target_condition_z_value

    @staticmethod
    def overval_stoploss_signal(data_row, strategy):
        overval_stoploss_condition_z_value = abs(strategy.get_stoploss_condition_z_value())
        strategy_id = strategy.get_id()
        return data_row[f'{strategy_id}_residual'] > overval_stoploss_condition_z_value
    
    @staticmethod
    def overval_exit_signal(data_row, position, strategy):
        return SignalProcessor.overval_stoploss_signal(data_row, strategy) or \
                SignalProcessor.overval_target_signal(data_row, strategy) or \
                SignalProcessor.stoploss_hit(position, strategy) or \
                SignalProcessor.target_hit(position, strategy) 

    @staticmethod
    def underval_entry_signal(data_row, strategy):
        underval_entry_condition_z_value = -1 * abs(strategy.get_entry_condition_z_value())
        strategy_id = strategy.get_id()
        return (data_row[f'{strategy_id}_residual'] < underval_entry_condition_z_value) and \
                (data_row[f'{strategy_id}_prev_residual'] > underval_entry_condition_z_value)
    
    @staticmethod
    def underval_target_signal(data_row, strategy):
        underval_target_condition_z_value = abs(strategy.get_target_condition_z_value())
        strategy_id = strategy.get_id()
        return data_row[f'{strategy_id}_residual'] > underval_target_condition_z_value
    
    @staticmethod
    def underval_stoploss_signal(data_row, strategy):
        underval_stoploss_condition_z_value = abs(strategy.get_stoploss_condition_z_value())
        strategy_id = strategy.get_id()
        return data_row[f'{strategy_id}_residual'] < underval_stoploss_condition_z_value

    @staticmethod
    def underval_exit_signal(data_row, position, strategy):
        return SignalProcessor.underval_stoploss_signal(data_row, strategy) or \
                SignalProcessor.underval_target_signal(data_row, strategy) or \
                SignalProcessor.stoploss_hit(position, strategy) or \
                SignalProcessor.target_hit(position, strategy) 

    @staticmethod
    def stoploss_hit(position, strategy):
        return position.get_net_perc() <= strategy.get_stoploss_perc()
    
    @staticmethod
    def target_hit(position, strategy):
        return  position.get_net_perc() <= strategy.get_stoploss_perc()