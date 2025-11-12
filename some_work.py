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
    charts=charts,
    close_on_time=True
)

# tt1.check_fast_old()
# # Печать статистики
# tt1.print_statistics('IMOEXF')
# tt1.print_statistics('MMZ5')

# tt1.reload_data()
tt1.check_fast()
# Печать статистики
tt1.print_statistics('IMOEXF')
tt1.print_statistics('MMZ5')

# tt1.reload_data()
# tt1.check_fast_vectorized()
# # Печать статистики
# tt1.print_statistics('IMOEXF')
# tt1.print_statistics('MMZ5')

# tt1.reload_data()
# tt1.check_fast_cached()
# # Печать статистики
# tt1.print_statistics('IMOEXF')
# tt1.print_statistics('MMZ5')
# print(tt1.trade_data)

# # Визуализация для конкретного символа
# tt1.visualize_results('IMOEXF')


# # Сравнение всех символов
# trader.compare_all_symbols()

# # Сохранение графика
# trader.visualize_results('ETHUSDT', save_path='eth_results.png')

