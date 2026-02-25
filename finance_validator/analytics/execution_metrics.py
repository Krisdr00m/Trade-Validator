from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict
from typing import Callable, Iterable, TypeVar, Dict, List
from trade_parser.models import Trade


T = TypeVar("T")
K = TypeVar("K")

def aggregate(
    items: Iterable[T],
    key_fn: Callable[[T], K],
    value_fn: Callable[[T], float],
    filter_fn: Callable[[T], bool] | None = None
) -> Dict[K, float]:
    """
    Generic grouping + aggregation engine.

    key_fn   → defines HOW we group
    value_fn → defines WHAT we accumulate
    filter_fn → optional row filtering
    """

    result = defaultdict(float)

    for item in items:
        if filter_fn and not filter_fn(item):
            continue

        key = key_fn(item)
        value = value_fn(item)

        result[key] += value

    return dict(result)


# =========================
# 3️⃣ Time Normalization Helper
# =========================

def minute_bucket(ts: datetime) -> datetime:
    """
    Normalize timestamp to the minute.
    Always rounds DOWN (industry standard).
    """
    return ts.replace(second=0, microsecond=0)


# =========================
# 4️⃣ Business Analytics Built on Top
# =========================

def volume_by_broker(trades: List[Trade]) -> Dict[str, int]:
    """
    Business Question:
    Which brokers handled the flow today?
    """
    return aggregate(
        trades,
        key_fn=lambda t: t.broker_id,
        value_fn=lambda t: t.quantity
    )


def buy_volume_by_symbol(trades: List[Trade]) -> Dict[str, int]:
    """
    How much BUY flow per symbol?
    """
    return aggregate(
        trades,
        key_fn=lambda t: t.symbol,
        value_fn=lambda t: t.quantity,
        filter_fn=lambda t: t.side == "BUY"
    )


def notional_by_symbol(trades: List[Trade]) -> Dict[str, float]:
    """
    Total dollar value traded per symbol.
    """
    return aggregate(
        trades,
        key_fn=lambda t: t.symbol,
        value_fn=lambda t: t.quantity * t.price
    )


def volume_per_minute(trades: List[Trade]) -> Dict[datetime, int]:
    """
    Trading intensity over time.
    """
    return aggregate(
        trades,
        key_fn=lambda t: minute_bucket(t.timestamp),
        value_fn=lambda t: t.quantity
    )


def broker_activity_over_time(trades: List[Trade]) -> Dict[tuple[str, datetime], int]:
    """
    Who traded WHEN (Broker + Minute bucket).
    """
    return aggregate(
        trades,
        key_fn=lambda t: (t.broker_id, minute_bucket(t.timestamp)),
        value_fn=lambda t: t.quantity
    )

    print(volume_by_broker(trades))
    print(buy_volume_by_symbol(trades))
    print(notional_by_symbol(trades))
    print(volume_per_minute(trades))