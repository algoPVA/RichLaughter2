from wss.LWS.LWS1 import LWS1_FIRSTGRID,LWS1_AUTOGRID,LWS2_SWIMGRID,LWS2_PSG


from traders.QuikTrader.QuikTrader import QuikTrader

bot_on_ticker = [
    {
        'ws': LWS1_AUTOGRID,
        'ws_params':{
            'start':11.440,
            'end':11.640,
            'amount_lvl': 10,
            'us_lvl': 11.740,
            'ds_lvl': 11.340,
            'grid_dir': 0,
        },
        'dts': [
            {
                'ss':('CRZ5',),
                'tfs':('M5',),
                'qs': (1,)
            }
        ]

    },
    {
        'ws': LWS1_AUTOGRID,
        'ws_params':{
            'start':11.360,
            'end':11.440,
            'amount_lvl': 5,
            'us_lvl': 11.540,
            'ds_lvl': 11.260,
            'grid_dir': 0,
        },
        'dts': [
            {
                'ss':('CNYRUBF',),
                'tfs':('M5',),
                'qs': (1,)
            }
        ]

    },
    # {
    #     'ws': LWS2_SWIMGRID,
    #     'ws_params':{
    #         'amount_lvl': 3,
    #         'per_step':0.2,
    #         'grid_dir': 1,
    #         'keep':False
    #     },
    #     'dts': [
    #         {
    #             'ss':('MMZ5',),
    #             'tfs':('M5',),
    #             'qs': (1,)
    #         }
    #     ]

    # },
    # {
    #     'ws': LWS1_FIRSTGRID,
    #     'ws_params':{
    #         'lvls':(2490,2505,2513),
    #         'us_lvl': 2520,
    #         'ds_lvl': None,
    #         'grid_dir': 1 
    #     },
    #     'dts': [
    #         {
    #             'ss':('IMOEXF',),
    #             'tfs':('M5',),
    #             'qs': (1,)
    #         }
    #     ]

    # },
    {
        'ws': LWS2_PSG,
        'ws_params':{
            'amount_lvl': 4,
            'per_step':0.05,
            'keep':False,
            'reset_n':2
        },
        'dts': [
            {
                'ss':('IMOEXF','MMZ5'),
                'tfs':('M5',),
                'qs': (1,1)
            }
        ]

    },
    {
        'ws': LWS2_SWIMGRID,
        'ws_params':{
            'amount_lvl': 3,
            'per_step':0.4,
            'grid_dir': 1,
            'keep':False
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