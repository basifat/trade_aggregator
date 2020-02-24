from collections import defaultdict
from trades.models.service import pre_transform_data
from trades.actions.utils import aggregate, AggregationException


def get_aggregated_data(file_name):
    dico = defaultdict(tuple)

    try:
        trades = pre_transform_data(file_name)
        for trade in trades:
            correlation_id, *_ = trade
            existing = dico[correlation_id]
            dico[correlation_id] = aggregate(trade, existing)
    except Exception:
        raise AggregationException("Failure to aggregate trades")

    return dico
