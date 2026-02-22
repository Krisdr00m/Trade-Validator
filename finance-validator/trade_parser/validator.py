from models import Trade
from datetime import datetime
import re

TRADE_ID_PATTERN = re.compile(r"^T\d+$")
BROKER_PATTERN = re.compile(r"^BRK\d+$")

RULES = [
    ("trade_id missing", lambda t: t.trade_id != ""),
    ("trade_id format", lambda t: TRADE_ID_PATTERN.search(t.trade_id) is not None),

    ("price <= 0", lambda t: t.price > 0),
    ("quantity <= 0", lambda t: t.quantity > 0),

    ("invalid side", lambda t: t.side in ("BUY", "SELL")),

    ("invalid exchange", lambda t: t.exchange in ("NASDAQ", "NYSE")),
    ("exchange not uppercase", lambda t: t.exchange.isupper()),

    ("symbol empty", lambda t: t.symbol.strip() != ""),
    ("symbol not uppercase", lambda t: t.symbol.isupper()),

    ("invalid broker_id", lambda t: BROKER_PATTERN.search(t.broker_id) is not None),
]

def check_data(trade_data: list[list[str]], invalid_rows):
    next_step_data = []
    for row in trade_data:
        
        if len(row) != 8:
            invalid_rows.append((row, "Wrong column count"))
            continue
    
        try:
            new_trade = Trade(
                trade_id= row[0], 
                symbol= row[1],
                price= float(row[2]),
                quantity=int(row[3]),
                timestamp= datetime.fromisoformat(row[4]),
                exchange=row[5],
                side=row[6],
                broker_id=row[7]
                )

            next_step_data.append(new_trade)
        except (ValueError, TypeError) as e:
            invalid_rows.append((row, str(e)))
                

    return (next_step_data)

def clean_data(trade_data_objects, invalid_rows):
    
    valid_trades = []
    seen_trade_ids = set()

    for trade in trade_data_objects:

        if trade.trade_id in seen_trade_ids:
            invalid_rows.append((trade, "duplicate trade_id"))
            continue

        seen_trade_ids.add(trade.trade_id)

        failed_reason = None
        for reason, rule in RULES:
            if not rule(trade):
                failed_reason = reason
                break

        if failed_reason:
            invalid_rows.append((trade, failed_reason))
        else:
            valid_trades.append(trade)

    return valid_trades