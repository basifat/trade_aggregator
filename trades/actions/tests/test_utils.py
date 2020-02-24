from unittest import mock
from trades.actions.utils import update_trade_state, aggregate, Trade, TradeAggregate
from trades.settings import project_root


def test_update_trade_state_for_pending():
    actual = update_trade_state(number_of_trades=10, new_count=5)
    expected = "Pending"
    assert actual == expected


def test_update_trade_state_accepted():
    actual = update_trade_state(new_value=2, trade_limit=8)
    expected = "Accepted"
    assert actual == expected


def test_update_trade_state_rejected():
    actual = update_trade_state(new_value=7, trade_limit=3)
    expected = "Rejected"
    assert actual == expected


def test_aggregate_first_time():
    trade = Trade(correlation_id=3, number_of_trades=2, trade_limit=100, trade_value=1)
    actual = aggregate(trade, False)
    expected = TradeAggregate(
        number_of_trades=2,
        trade_limit=100,
        trade_value=1,
        trade_count=1,
        state="Pending",
    )
    assert actual == expected


def test_aggregate_existing_trade():
    trade = Trade(correlation_id=2, number_of_trades=2, trade_limit=100, trade_value=1)
    existing_trade = TradeAggregate(
        number_of_trades=2,
        trade_limit=100,
        trade_value=75,
        trade_count=1,
        state="Pending",
    )
    actual = aggregate(trade, existing_trade)
    expected = TradeAggregate(
        number_of_trades=2,
        trade_limit=100,
        trade_value=76,
        trade_count=2,
        state="Accepted",
    )
    assert actual == expected
