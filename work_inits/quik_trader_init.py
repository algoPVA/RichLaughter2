from wss.LWS.LWS1 import LWS1_FIRSTGRID


from traders.QuikTrader.QuikTrader import QuikTrader

bot_on_ticker = [
    {
        'ws': LWS1_FIRSTGRID,
        'ws_params':{
            'lvls':(11.52,11.53,11.54,11.55),
            'us_lvl': 11.57,
            'ds_lvl': 11.50,
            'grid_dir': 0 
        },
        'dts': [
            {
                'ss':('CRZ5',),
                'tfs':('M5',),
                'qs': (1,)
            }
        ]

    }
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