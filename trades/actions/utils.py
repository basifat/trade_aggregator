from typing import NamedTuple


class Trade(NamedTuple):
    correlation_id: int
    number_of_trades: int
    trade_limit: int
    trade_value: int


class TradeAggregate(NamedTuple):
    number_of_trades: int
    trade_limit: int
    trade_value: int
    trade_count: int
    state: str


class TradeState(NamedTuple):
    accepted: str
    pending: str
    rejected: str


def update_trade_state(
    number_of_trades=None, new_count=None, new_value=None, trade_limit=None
):
    states = TradeState("Accepted", "Pending", "Rejected")

    if (number_of_trades and new_count) and (number_of_trades > new_count):
        return states.pending
    elif (new_value and trade_limit) and (new_value < trade_limit):
        return states.accepted
    elif (new_value and trade_limit) and (new_value > trade_limit):
        return states.rejected


def aggregate(trade, existing):
    _, number_of_trades, trade_limit, trade_value = trade
    new_value = trade_value
    new_count = 1

    if existing:
        number_of_trades, trade_limit, trade_value, trade_count, state = existing
        new_count += trade_count
        new_value += trade_value

    state = update_trade_state(
        number_of_trades=number_of_trades,
        new_count=new_count,
        new_value=new_value,
        trade_limit=trade_limit,
    )

    return TradeAggregate(number_of_trades, trade_limit, new_value, new_count, state)


class AggregationException(Exception):
    """Exception class for handling aggregate calculations"""

    pass
