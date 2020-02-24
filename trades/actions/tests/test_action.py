from unittest import mock
from trades.actions.action import get_aggregated_data
from trades.actions.utils import Trade, TradeAggregate
from trades.settings import project_root

test_input_file = "mock input file"


@mock.patch("trades.actions.action.pre_transform_data")
def test_aggregation_single_trade_pending_state(mock_pre_transform_data):
    mock_pre_transform_data.return_value = [
        Trade(correlation_id=234, number_of_trades=3, trade_limit=1000, trade_value=100)
    ]

    actual = get_aggregated_data(test_input_file)
    expected = {
        234: TradeAggregate(
            number_of_trades=3,
            trade_limit=1000,
            trade_value=100,
            trade_count=1,
            state="Pending",
        )
    }
    assert actual == expected


@mock.patch("trades.actions.action.pre_transform_data")
def test_accepted_single_trade_accepted_state(mock_pre_transform_data):
    mock_pre_transform_data.return_value = [
        Trade(correlation_id=234, number_of_trades=1, trade_limit=1000, trade_value=100)
    ]

    actual = get_aggregated_data(test_input_file)
    expected = {
        234: TradeAggregate(
            number_of_trades=1,
            trade_limit=1000,
            trade_value=100,
            trade_count=1,
            state="Accepted",
        )
    }
    assert actual == expected


@mock.patch("trades.actions.action.pre_transform_data")
def test_accepted_single_trade_rejected_state(mock_pre_transform_data):
    mock_pre_transform_data.return_value = [
        Trade(correlation_id=234, number_of_trades=1, trade_limit=50, trade_value=100)
    ]

    actual = get_aggregated_data(test_input_file)
    expected = {
        234: TradeAggregate(
            number_of_trades=1,
            trade_limit=50,
            trade_value=100,
            trade_count=1,
            state="Rejected",
        )
    }
    assert actual == expected


@mock.patch("trades.actions.action.pre_transform_data")
def test_aggregation_for_multiple_trades_pending_state(mock_pre_transform_data):
    mock_pre_transform_data.return_value = [
        Trade(
            correlation_id=234, number_of_trades=3, trade_limit=1000, trade_value=100
        ),
        Trade(
            correlation_id=234, number_of_trades=3, trade_limit=1000, trade_value=100
        ),
    ]

    actual = get_aggregated_data(test_input_file)
    expected = {
        234: TradeAggregate(
            number_of_trades=3,
            trade_limit=1000,
            trade_value=200,
            trade_count=2,
            state="Pending",
        )
    }
    assert actual == expected


@mock.patch("trades.actions.action.pre_transform_data")
def test_aggregation_for_multiple_trades_accepted_state(mock_pre_transform_data):
    mock_pre_transform_data.return_value = [
        Trade(
            correlation_id=234, number_of_trades=3, trade_limit=1000, trade_value=100
        ),
        Trade(
            correlation_id=234, number_of_trades=3, trade_limit=1000, trade_value=100
        ),
        Trade(
            correlation_id=234, number_of_trades=3, trade_limit=1000, trade_value=100
        ),
    ]

    actual = get_aggregated_data(test_input_file)
    expected = {
        234: TradeAggregate(
            number_of_trades=3,
            trade_limit=1000,
            trade_value=300,
            trade_count=3,
            state="Accepted",
        )
    }
    assert actual == expected


@mock.patch("trades.actions.action.pre_transform_data")
def test_aggregation_for_multiple_trades_rejected_state(mock_pre_transform_data):
    mock_pre_transform_data.return_value = [
        Trade(
            correlation_id=234, number_of_trades=3, trade_limit=1000, trade_value=100
        ),
        Trade(
            correlation_id=234, number_of_trades=3, trade_limit=1000, trade_value=600
        ),
        Trade(
            correlation_id=234, number_of_trades=3, trade_limit=1000, trade_value=500
        ),
    ]

    actual = get_aggregated_data(test_input_file)
    expected = {
        234: TradeAggregate(
            number_of_trades=3,
            trade_limit=1000,
            trade_value=1200,
            trade_count=3,
            state="Rejected",
        )
    }
    assert actual == expected


@mock.patch("trades.actions.action.pre_transform_data")
def test_aggregation_for_multiple_trades_all_three_states(mock_pre_transform_data):
    mock_pre_transform_data.return_value = [
        Trade(
            correlation_id=234, number_of_trades=3, trade_limit=1000, trade_value=100
        ),
        Trade(
            correlation_id=234, number_of_trades=3, trade_limit=1000, trade_value=200
        ),
        Trade(
            correlation_id=234, number_of_trades=3, trade_limit=1000, trade_value=200
        ),
        Trade(correlation_id=222, number_of_trades=1, trade_limit=500, trade_value=600),
        Trade(
            correlation_id=200, number_of_trades=2, trade_limit=2000, trade_value=1000
        ),
    ]

    actual = get_aggregated_data(test_input_file)
    expected = {
        234: TradeAggregate(
            number_of_trades=3,
            trade_limit=1000,
            trade_value=500,
            trade_count=3,
            state="Accepted",
        ),
        222: TradeAggregate(
            number_of_trades=1,
            trade_limit=500,
            trade_value=600,
            trade_count=1,
            state="Rejected",
        ),
        200: TradeAggregate(
            number_of_trades=2,
            trade_limit=2000,
            trade_value=1000,
            trade_count=1,
            state="Pending",
        ),
    }
    assert actual == expected


@mock.patch("trades.actions.utils.aggregate")
@mock.patch("trades.actions.action.pre_transform_data")
def test_aggregation_for_multiple_trades_mock_aggregated_state(
    mock_pre_transform_data, mock_aggregate
):
    mock_pre_transform_data.return_value = [
        Trade(
            correlation_id=234, number_of_trades=2, trade_limit=1000, trade_value=100
        ),
        Trade(
            correlation_id=234, number_of_trades=2, trade_limit=1000, trade_value=200
        ),
    ]

    mock_aggregate.return_value = TradeAggregate(
        number_of_trades=2,
        trade_limit=1000,
        trade_value=300,
        trade_count=2,
        state="Accepted",
    )

    actual = get_aggregated_data(test_input_file)
    expected = {
        234: TradeAggregate(
            number_of_trades=2,
            trade_limit=1000,
            trade_value=300,
            trade_count=2,
            state="Accepted",
        ),
    }
    assert actual == expected

