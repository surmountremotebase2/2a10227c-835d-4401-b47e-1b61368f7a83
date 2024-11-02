from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import BB, ATR
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Symbol of the asset to trade
        self.ticker = "SPY"
        # Historical data window (days) to calculate indicators
        self.lookback_period = 20
        self.atr_multiplier = 2
    
    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        # Initialize allocation with 0 (not taking any position by default)
        allocation = {self.ticker: 0}
        
        # Calculate Bollinger Bands and Average True Range
        bollinger_bands = BB(self.ticker, data["ohlcv"], self.lookback_period, 2)
        atr = ATR(self.ticker, data["ohlcv"], self.lookback_period)
        
        if bollinger_bands and atr:
            # Calculate the width of Bollinger Bands
            bb_width = bollinger_bands['upper'][-1] - bollinger_bands['lower'][-1]
            
            # Determine if market is in a low volatility regime by checking if the BB width is less than ATR times a multiplier
            if bb_width < (atr[-1] * self.atr_multiplier):
                log("Market in low volatility regime. Considering position.")
                # Consider taking a position. Here, allocation logic can be more elaborate.
                # This is a placeholder indicating a willingness to engage the market under low volatility.
                # Allocation value can be dynamically determined based on additional indicators or risk management rules.
                allocation[self.ticker] = 0.5  # Example allocation

        return TargetAllocation(allocation)