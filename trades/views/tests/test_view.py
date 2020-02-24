from trades.views.view import write_files
from unittest import mock
from trades.settings import (
    project_root,
    dev_file_input,
    dev_file_output,
    dev_server_log,
)
import sys, os
from trades.actions.utils import TradeAggregate

test_input_file = f"{project_root}/views/tests/{dev_file_input}"
test_output_file = f"{project_root}/views/tests/{dev_file_output}"
test_server_file_log = f"{project_root}/views/tests/{dev_server_log}"


@mock.patch("trades.views.view.get_aggregated_data")
def test_write_data_to_csv_and_server_log(mock_get_aggregated_data):
    mock_get_aggregated_data.return_value = {
        234: TradeAggregate(3, 1000, 1200, 3, "Rejected"),
        101: TradeAggregate(2, 500, 900, 3, "Accepted"),
        212: TradeAggregate(2, 500, 900, 3, "Accepted"),
    }

    write_files(
        input_file=test_input_file,
        output_file=test_output_file,
        log_file=test_server_file_log,
    )
    actual = open(test_output_file).readlines()

    expected = [
        "CorrelationID\tNumberOfTrades\tState\n",
        "101\t2\tAccepted\n",
        "212\t2\tAccepted\n",
        "234\t3\tRejected\n",
    ]

    assert expected == actual[:4]
