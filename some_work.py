from traders.TestTrader.TestTrader import TestTrader
from wss.work_ws import WorkWS

charts = {
    '1min': {
        'IMOEXF':'data_for_tests\data_from_moex\IMOEXF_1_1762793370.csv',
        'MMZ5':'data_for_tests\data_from_moex\MMZ5_1_1762793372.csv'
        },
    '10min': {
        'IMOEXF':'data_for_tests\data_from_moex\IMOEXF_10_1762793370.csv',
        'MMZ5':'data_for_tests\data_from_moex\MMZ5_10_1762793372.csv'
        },
}

tt1 = TestTrader(
    ('IMOEXF','MMZ5'),
    ('1min','10min'),
    (1,1),
    (WorkWS,{'period_dc':20}),
    charts=charts
)

tt1.check_fast()