import os
from traders.TestTrader.TestTrader import TestTrader
# from wss.LWS.LWS1 import LWS2_SWIMIGSON as WSS
# from wss.LWS.LWS1 import LWS2_SWIMGRID as WSS
# from wss.LWS.LWS1 import LWS2_PSG as WSS
# from wss.LWS.LWS1 import LWS2_PSGSON as WSS
from wss.LWS.LWS1 import LWS3_b as WSS
# from wss.PWS.PWS1 import PWS1_GRIDC as WSS
#     {
#     'period':50,
#     'amount_lvl': 2,
#     'grid_dir': 0,
#     'per_limit': 0.1,
#     'keep': True
# }
            # 'amount_lvl': 4,
            # 'per_step':0.05,
            # 'grid_dir': 0,
            # 'keep':False,
            # 'reset_n': 3

folder_charts = 'data_for_tests\data_from_moex5'
charts_list = os.listdir(folder_charts)
symbols = ('IMOEXF','MMZ5')
charts = {s: None for s in symbols}
for chart in charts_list:
    for s in symbols:
        if s in chart:
            charts[s] = os.path.join(folder_charts,chart)
tt1 = TestTrader(
    symbols,
    ('5min',),
    (1,1),
    (
        WSS,    
        {
            'period_rsi':14,
            'lvls':(10,30,70,90),
            'buff':10,
    }
    ),
    charts={'5min':charts},
    # charts={'5min':{
    #     'IMOEXF':'data_for_tests\data_from_moex5\_5IMOEXF_1_1763404348.parquet',
    #     'MMZ5':'data_for_tests\data_from_moex5\_5MMZ5_1_1763404355.parquet'
    #     }},

    close_on_time=True

)
# tt1 = TestTrader(
#     ('IMOEXF',),
#     ('5min',),
#     (1,),
#     (
#         WSS,    
#         {
#             'amount_lvl': 4,
#             'per_step':0.05,
#             'grid_dir': 0,
#             'keep':False,
#             'reset_n':3
#     }
#     ),
#     charts={'5min':{
#         'IMOEXF':'data_for_tests\data_from_moex5\_5IMOEXF_1_1763392706.csv',
#         # 'MMZ5':'data_for_tests\data_from_moex5\_5MMZ5_1_1763392708.csv'
#         }},
#     # charts={'1min':{
#     #     'IMOEXF':'data_for_tests\data_from_moex\IMOEXF_1_1762793370.csv',
#     #     'MMZ5':'data_for_tests\data_from_moex\MMZ5_1_1762793372.csv'
#     #     }},
#     close_on_time=True

# )
# # tt1.check_fast_old()
# # # Печать статистики
# # tt1.print_statistics('IMOEXF')
# # tt1.print_statistics('MMZ5')

# # tt1.reload_data()
tt1.check_fast()
# # Печать статистики
tt1.print_statistics('CNYRUBF')
tt1.print_statistics('CRZ5')
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


# from traders.QuikTrader.help_funcs import *

# symbol = 'IMOEXF'
# # pos = get_pos_futures(symbol)
# # print(pos)
# # cur_price = get_current_price(symbol)
# # print(cur_price)
# debug_futures_holdings(symbol)