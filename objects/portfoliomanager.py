from objects.pairposition import PairPosition

class PortfolioManager:

    @staticmethod
    def enter_pair_position(portfolio, strategy, data_row, pair_position_type):
        capital_required = strategy.get_capital_allocated()
        if portfolio.get_total_capital() < capital_required:
            print ('not enough capital')
            return 
        
        entry_date = data_row['date']
        strategy_id = strategy.get_id()
        capital_allocated = strategy.get_capital_allocated()

        if pair_position_type == 'underval':
            long_ticker=strategy.get_ticker2()
            short_ticker=strategy.get_ticker1()
            long_ticker_wt=strategy.get_ticker2_wt()
            short_ticker_wt=strategy.get_ticker1_wt()
            long_entry_price=data_row[f'{strategy.get_ticker2()}']
            short_entry_price=data_row[f'{strategy.get_ticker1()}']
        elif pair_position_type == 'overval':
            long_ticker=strategy.get_ticker1()
            short_ticker=strategy.get_ticker2()
            long_ticker_wt=strategy.get_ticker1_wt()
            short_ticker_wt=strategy.get_ticker2_wt()
            long_entry_price=data_row[f'{strategy.get_ticker1()}']
            short_entry_price=data_row[f'{strategy.get_ticker2()}']
        
        portfolio.append_open_position(PairPosition(
            id=1, # fix this
            entry_date=entry_date,
            type=pair_position_type,
            strategy_id=strategy_id,
            long_ticker=long_ticker,
            short_ticker=short_ticker,
            long_ticker_wt=long_ticker_wt,
            short_ticker_wt=short_ticker_wt,
            long_entry_price=long_entry_price,
            short_entry_price=short_entry_price,
            capital_allocated=capital_allocated
        ))
        portfolio.deduct_from_total_capital(strategy.get_capital_allocated())

    
    @staticmethod
    def exit_pair_position(portfolio, position, data_row):
        portfolio.remove_open_position(position)

        long_ticker = position.get_long_ticker()
        short_ticker = position.get_short_ticker()

        long_exit_price = data_row[long_ticker]
        short_exit_price = data_row[short_ticker]

        position.set_exit_date(data_row['date'])
        position.set_long_exit_price(long_exit_price)
        position.set_short_exit_price(short_exit_price)
        position.set_duration()

        portfolio.add_to_total_capital((1 + position.get_net_perc()) * position.get_capital_allocated())

        portfolio.append_closed_position(position)