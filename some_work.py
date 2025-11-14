from traders.TestTrader.TestTrader import TestTrader
# from wss.work_ws import WorkWS

# charts = {
#     '1min': {
#         'IMOEXF':'data_for_tests\data_from_moex\IMOEXF_1_1762793370.csv',
#         'MMZ5':'data_for_tests\data_from_moex\MMZ5_1_1762793372.csv'
#         },
#     '10min': {
#         'IMOEXF':'data_for_tests\data_from_moex\IMOEXF_10_1762793370.csv',
#         'MMZ5':'data_for_tests\data_from_moex\MMZ5_10_1762793372.csv'
#         },
# }

# tt1 = TestTrader(
#     ('IMOEXF','MMZ5'),
#     ('1min','10min'),
#     (1,1),
#     (WorkWS,{'period_dc':20}),
#     charts=charts,
#     close_on_time=True
# )
from wss.LWS.LWS1 import LWS1_FIRSTGRID
tt1 = TestTrader(
    ('IMOEXF',),
    ('1min',),
    (1,),
    (
        LWS1_FIRSTGRID,    
     {
        'lvls':(2530,2540,2550,2560,),
        'us_lvl': None,
        'ds_lvl': None,
        'grid_dir': 0 
    }
    ),
    charts={'1min':{'IMOEXF':'data_for_tests\data_from_moex\IMOEXF_1_1762793370.csv'}},
    close_on_time=True

)
# # tt1.check_fast_old()
# # # Печать статистики
# # tt1.print_statistics('IMOEXF')
# # tt1.print_statistics('MMZ5')

# # tt1.reload_data()
tt1.check_fast()
# # Печать статистики
tt1.print_statistics('IMOEXF')
# tt1.print_statistics('MMZ5')

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


# from traders.QuikTrader.help_funcs import *

# symbol = 'IMOEXF'
# # pos = get_pos_futures(symbol)
# # print(pos)
# # cur_price = get_current_price(symbol)
# # print(cur_price)
# debug_futures_holdings(symbol)