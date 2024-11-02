from surmount.base_class import Strategy, TargetAllocation
from surmount.data import ImpliedVolatility, UpcomingEvents, StockNews, StockPrice
from datetime import datetime, timedelta
import numpy as np

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "TSLA"
        self.target_profit_percentage = 0.25  # Target profit percentage (25%)
        self.stop_loss_percentage = 0.30  # Stop loss percentage (30%)
        self.weekly_exp = self.get_next_friday()
        self.start_of_week = self.get_monday()

        # Data requirements
        self.data_list = [
            StockPrice(self.ticker),
            ImpliedVolatility(self.ticker, self.weekly_exp),
            UpcomingEvents(self.ticker),
            StockNews(self.ticker)
        ]

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"

    def get_next_friday(self):
        today = datetime.today()
        next_friday = today + timedelta((4-today.weekday()) % 7)
        return next_friday

    def get_monday(self):
        today = datetime.today()
        monday = today - timedelta(days=today.weekday())
        return monday

    def run(self, data):
        # Placeholder for managing allocations, not directly applicable but included for concept
        allocation_dict = {}

        # Check if today is Monday and at market open; if not, do nothing
        if datetime.now().date() != self.start_of_week.date() or datetime.now().time() > datetime.strptime("09:30", "%H:%M").time():
            return TargetAllocation(allocation_dict)

        # Calculate IV, Check news impact and upcoming events
        iv = data[("implied_volatility", self.ticker, self.weekly_exp)]
        events = data[("upcoming_events", self.ticker)]
        news = data[("stock_news", self.ticker)]

        # Checking the implied volatility and market conditions
        if iv > 0.5:  # High volatility might indicate a larger price movement.
            width_between_strikes = 10
        else:
            width_between_strikes = 5

        # Strategy placeholder, as actual execution details like selecting strikes are not implementable here
        # This section should determine the out-of-money call and put strike prices based on current stock price,
        # implied volatility, and preferential width between strikes.

        # Plan for profit target and stop loss based on option pricing mechanics (unimplementable directly in Surmount)
        # Similarly, adjustment strategies and early closeouts would depend on real-time option pricing and stock movement
        
        # Log a message or send a signal for initiating trade (conceptual)
        print("Initiate long iron condor position for TSLA with expiry on", self.weekly_exp, "with target profit", self.target_profit_percentage, "and stop loss", self.stop_loss_percentage)

        return TargetAllocation(allocation_dict)

    def log_event_info(self, events, news):
        for event in events:
            print(f"Upcoming event for {self.ticker}: {event['description']}")
        for article in news:
            print(f"News impact for {self.ticker}: {article['headline']}")