from surmount.base_class import Strategy, TargetAllocation
from surmount.data import InstitutionalOwnership, InsiderTrading

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize with a list of tickers to track.
        self.tickers = ["SPY", "QQQ", "AAPL", "GOOGL"]
        # Gathering data for institutional ownership and insider trading for each ticker.
        self.data_list = [InstitutionalOwnership(i) for i in self.tickers] + [InsiderTrading(i) for i in self.tickers]

    @property
    def interval(self):
        # Defines the data interval to be daily for this strategy.
        return "1day"

    @property
    def assets(self):
        # List of assets this strategy will consider trading.
        return self.tickers

    @property
    def data(self):
        # List of data sources needed for the strategy.
        return self.data_list

    def run(self, data):
        # Initialize allocation dictionary with equal weight for each ticker.
        allocation_dict = {ticker: 1/len(self.tickers) for ticker in self.tickers}
        
        for data_item in self.data_list:
            # Check if data item is related to insider trading.
            if isinstance(data_item, InsiderTrading):
                # Fetch the latest insider trading information for the ticker.
                recent_data = data.get(('insider_trading', data_item.ticker), [])
                # If there's recent data and the latest transaction was a sale, set allocation to 0.
                if recent_data and recent_data[-1]['transactionType'] == "Sale":
                    allocation_dict[data_item.ticker] = 0

        # Return the target allocation based on the strategy logic.
        return TargetAllocation(allocation_dict)