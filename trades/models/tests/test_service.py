from trades.models.service import load_data, extract, pre_transform_data, prepare
from trades.actions.utils import Trade, TradeAggregate
from unittest import mock
from trades.settings import project_root

test_input_file = project_root + '/models/tests/test_input.xml'

def test_load_data():
    actual = load_data(test_input_file)
    expected = 5
    assert expected == len(actual)

def test_extract_row_data():
    line =  ' <Trade CorrelationId="200" NumberOfTrades="2" Limit="1000" TradeID="645">1000</Trade> '
    expected = [200, 2, 1000, 645, 1000]
    actual = extract(line)
    assert expected == list(actual)
    
@mock.patch('trades.models.service.load_data')
def test_pre_transform_row_data(mock_load_data):
    mock_load_data.return_value = [
                                       '\t<Trade CorrelationId="234" NumberOfTrades="3" Limit="1000" TradeID="654">100</Trade>\n',
                                    ]
    expected = Trade(correlation_id=234, number_of_trades=3, trade_limit=1000, trade_value=100)
    actual = pre_transform_data('')
    
    assert expected == actual[0]

@mock.patch('trades.models.service.load_data')
def test_pre_transform_multiple_row_data(mock_load_data):
    mock_load_data.return_value = [
                                       '\t<Trade CorrelationId="234" NumberOfTrades="3" Limit="1000" TradeID="654">100</Trade>\n',
                                        '\t<Trade CorrelationId="255" NumberOfTrades="6" Limit="1000" TradeID="444">300</Trade>\n'
                                    ]
    expected = [
            Trade(correlation_id=234, number_of_trades=3, trade_limit=1000, trade_value=100), 
            Trade(correlation_id=255, number_of_trades=6, trade_limit=1000, trade_value=300)
    ] 
    actual = pre_transform_data('')
    assert expected == actual

def test_prepare_can_split_multiple_data():
    data = 'CorrelationId="234"'
    actual = prepare(data)
    assert actual == 234

def test_prepare_can_split_single_data():
    data = '100'
    actual = prepare(data)
    assert actual == 100