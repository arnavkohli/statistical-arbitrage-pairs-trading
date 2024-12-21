class PositionManager:
    
    @staticmethod
    def update_position_pnl(data_row, position):
        PositionManager.update_long_leg_pnl(data_row, position)
        PositionManager.update_short_leg_pnl(data_row, position)

        position.set_abs_net(position.get_long_net_abs() + position.get_short_net_abs())
        position.set_net_perc(
            position.get_long_net_perc()*position.get_long_ticker_wt() + \
            position.get_short_net_perc()*position.get_short_ticker_wt()
        )


    @staticmethod
    def update_long_leg_pnl(data_row, position):
        long_ticker = position.get_long_ticker()
        long_ticker_current_price = data_row[long_ticker]

        long_profit = long_ticker_current_price - position.get_long_entry_price()
        long_net_perc = long_profit / position.get_long_entry_price()

        long_net_abs = long_net_perc * position.get_capital_allocated() * position.get_long_ticker_wt()

        position.set_long_net_abs(long_net_abs)
        position.set_long_net_perc(long_net_perc)

    
    @staticmethod
    def update_short_leg_pnl(data_row, position):
        short_ticker = position.get_short_ticker()
        short_ticker_current_price = data_row[short_ticker]

        short_profit = position.get_short_entry_price() - short_ticker_current_price
        short_net_perc = short_profit / position.get_short_entry_price()

        short_net_abs = short_net_perc * position.get_capital_allocated() * position.get_short_ticker_wt()

        position.set_short_net_abs(short_net_abs)
        position.set_short_net_perc(short_net_perc)
    