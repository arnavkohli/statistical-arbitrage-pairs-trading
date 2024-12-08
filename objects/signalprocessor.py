class SignalProcessor:
    
    @staticmethod
    def overval_entry_signal(data_row, strategy):
        overval_entry_condition_z_value = abs(strategy.get_entry_condition_z_value())
        strategy_id = strategy.get_id()
        return (data_row[f'{strategy_id}_residual'] > overval_entry_condition_z_value) and \
                (data_row[f'{strategy_id}_prev_residual'] < overval_entry_condition_z_value)
    
    @staticmethod
    def overval_exit_signal(data_row, strategy):
        pass

    @staticmethod
    def underval_entry_signal(data_row, strategy):
        underval_entry_condition_z_value = -1 * abs(strategy.get_entry_condition_z_value())
        strategy_id = strategy.get_id()
        return (data_row[f'{strategy_id}_residual'] < underval_entry_condition_z_value) and \
                (data_row[f'{strategy_id}_prev_residual'] > underval_entry_condition_z_value)

    @staticmethod
    def underval_exit_signal(data_row, strategy):
        pass
    
    @staticmethod
    def exit_signal(data_row, position, strategy):
        return (
            SignalProcessor.stoploss_hit(data_row, position, strategy) or \
                SignalProcessor.target_hit(data_row, position, strategy) or \
                    SignalProcessor.exit_condition_hit(data_row, strategy)
            )

    @staticmethod
    def stoploss_hit(data_row, position, strategy):
        long_ticker = position.get_long_ticker()
        short_ticker = position.get_short_ticker()
        current_long_price = data_row[long_ticker]
        current_short_price = data_row[short_ticker]

        position_net_per = position.compute_net_perc(
            current_long_price=current_long_price,
            current_short_price=current_short_price
        )

        return position_net_per <= strategy.get_stoploss_perc()
    
    @staticmethod
    def target_hit(data_row, position, strategy):
        long_ticker = position.get_long_ticker()
        short_ticker = position.get_short_ticker()
        current_long_price = data_row[long_ticker]
        current_short_price = data_row[short_ticker]

        position_net_per = position.compute_net_perc(
            current_long_price=current_long_price,
            current_short_price=current_short_price
        )

        return position_net_per >= strategy.get_target_perc()

    @staticmethod
    def exit_condition_hit(data_row, strategy):
        exit_conditions = strategy.get_exit_conditions()
        return all([condition(data_row) for condition in exit_conditions])
