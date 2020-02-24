import os

project_root = os.path.dirname(os.path.dirname(__file__))
project_root = os.path.join(project_root, "trades")

prod_file_input = "input.xml"
prod_file_output = "results.csv"
prod_server_log = "server.log"

dev_file_input = "test_input.xml"
dev_file_output = "test_results.csv"
dev_server_log = "test_server.log"

