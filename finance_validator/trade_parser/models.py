from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
    trade_id: str
    symbol: str
    price: float
    quantity: int
    timestamp: datetime
    exchange: str
    side: str
    broker_id: str
