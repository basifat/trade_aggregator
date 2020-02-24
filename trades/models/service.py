import re
from trades.actions.utils import Trade


def load_data(file_name):
    line_generator = (line for line in open(file_name))
    # skips the first tag of the xml document i.e <Trades>
    next(line_generator)
    # skips the last tag of the xml document i.e </Trades>
    *rest, _ = line_generator

    return rest


def extract(row):
    pattern = "[\\s|<|>|/|\t]"
    row = re.split(pattern, row)

    return (prepare(item) for item in row if item and item != "Trade")


def prepare(item):
    first, *second = item.replace('"', "").split("=")
    if second:
        return int(*second)
    else:
        return int(first)


def pre_transform_data(file_name):
    entire_lines = load_data(file_name)
    row_data = map(extract, entire_lines)
    extra = []
    for item in row_data:
        *rest, _, trade_value = list(item)
        extra.append(Trade(*rest, trade_value))
    return extra
