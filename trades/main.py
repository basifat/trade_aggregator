import os
import sys
import logging
from pprint import pprint

from trades.settings import prod_file_input, prod_file_output, prod_server_log
from trades.views.view import write_files

if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = prod_file_input


def run():
    pprint("Writing aggregates to disk ... ")
    write_files(
        input_file=file_name, output_file=prod_file_output, log_file=prod_server_log
    )
    pprint("Completed writing aggregates to disk.")
