from datetime import datetime
from trades.actions.action import get_aggregated_data
from trades.actions.utils import AggregationException
import csv
import os


def write_output_csv(output_file, data):
    file_exists = os.path.isfile(output_file)
    csvfile = open(output_file, "a")
    headers = ["CorrelationID", "NumberOfTrades", "State"]
    writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=headers)
    if not file_exists:
        writer.writeheader()
    for key, trade in data:
        writer.writerow(
            {
                "CorrelationID": key,
                "NumberOfTrades": trade.number_of_trades,
                "State": trade.state,
            }
        )


def write_server_log(log_file, total=None, error_message=None):
    server_csv = open(log_file, "a")
    text = error_message or f"Updated {total} trades at {str(datetime.now())}"
    server_csv.write(text)
    server_csv.write("\n")


def write_files(input_file=None, output_file=None, log_file=None):
    data = None

    try:
        data = get_aggregated_data(input_file)
        data = sorted(data.items(), key=lambda k: k)
        write_output_csv(output_file, data)
        write_server_log(log_file, total=len(data))

    except AggregationException as e:
        """TODO"""
        # Add more defensive error handling throught the application
        error_message = f"{str(e)} on {str(datetime.now())}"
        write_server_log(log_file, error_message=error_message)
    except Exception as e:
        error_message = f"{str(e)} {str(datetime.now())}"
        write_server_log(log_file, error_message=error_message)
        raise
