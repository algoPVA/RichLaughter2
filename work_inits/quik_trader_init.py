from wss.LWS.LWS1 import LWS1_FIRSTGRID


from traders.QuikTrader.QuikTrader import QuikTrader

bot_on_ticker = [
    # {
    #     'ws': LWS1_FIRSTGRID,
    #     'ws_params':{
    #         'lvls':(11.52,11.53,11.54,11.55),
    #         'us_lvl': 11.57,
    #         'ds_lvl': 11.50,
    #         'grid_dir': 0 
    #     },
    #     'dts': [
    #         {
    #             'ss':('CRZ5',),
    #             'tfs':('M5',),
    #             'qs': (1,)
    #         }
    #     ]

    # },
    {
        'ws': LWS1_FIRSTGRID,
        'ws_params':{
            'lvls':(2569,2560,2552),
            'us_lvl': 2574,
            'ds_lvl': 2540,
            'grid_dir': 1 
        },
        'dts': [
            {
                'ss':('MMZ5',),
                'tfs':('M5',),
                'qs': (1,)
            }
        ]

    },
    {
        'ws': LWS1_FIRSTGRID,
        'ws_params':{
            'lvls':(2530,2533,2537,2540),
            'us_lvl': 2545,
            'ds_lvl': 2523,
            'grid_dir': 0 
        },
        'dts': [
            {
                'ss':('IMOEXF',),
                'tfs':('M5',),
                'qs': (1,)
            }
        ]

    },
    {
        'ws': LWS1_FIRSTGRID,
        'ws_params':{
            'lvls':(993.5,995),
            'us_lvl': 996,
            'ds_lvl': 991.5,
            'grid_dir': -1 
        },
        'dts': [
            {
                'ss':('RMZ5',),
                'tfs':('M5',),
                'qs': (1,)
            }
        ]

    },
]

def init_trader() -> list[QuikTrader]:
    bots = []
    for conf_ws in bot_on_ticker:
        ws = (conf_ws['ws'],conf_ws['ws_params'])
        for dt in conf_ws['dts']:
            print(dt['ss'],dt['tfs'],ws)
            bot = QuikTrader(dt['ss'],dt['tfs'],dt['qs'],ws,need_debug=True)
            bots.append(bot)
    return bots