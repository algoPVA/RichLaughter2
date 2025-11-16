from wss.LWS.LWS1 import LWS1_FIRSTGRID,LWS1_AUTOGRID


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
        'ws': LWS1_AUTOGRID,
        'ws_params':{
            'start':2560,
            'end':2568,
            'amount_lvl': 3,
            'us_lvl': 2571,
            'ds_lvl': 2558,
            'grid_dir': -1,
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
            'lvls':(2527,2530,2534),
            'us_lvl': 2537,
            'ds_lvl': 2525,
            'grid_dir': -1 
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
        'ws': LWS1_AUTOGRID,
        'ws_params':{
            'start':11950,
            'end':12030,
            'amount_lvl': 4,
            'us_lvl': 12060,
            'ds_lvl': 11940,
            'grid_dir': 0,
        },
        'dts': [
            {
                'ss':('GZZ5',),
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