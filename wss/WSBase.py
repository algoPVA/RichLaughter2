from typing import Dict, List, Any, Optional, Union
import pandas as pd



class WSBase:
    def __init__(self,symbols:List[str],timeframes:List[str|int],positions:Dict[str,int],middle_price:Dict[str,float],parameters:Dict[str,Any]):
        """
        symbols = ['IMOEXF','MMZ5'],
        timeframes = ['5m','1H'],
        positions = {
            'IMOEXF':1,
            'MMZ5':-1,
        },
        middle_price = {
            'IMOEXF':2565.0,
            'MMZ5':2612.0,
        },
        parameters = {
            'period_bb':20,
            'mult_bb':2,
            'kind_bb':'close'
        }
        """
        self.symbols = symbols
        self.timeframes = timeframes
        self.positions = positions.copy()
        self.middle_price = middle_price
        # self.parameters = parameters
        self.need_pos = positions.copy()
        self.last_dfs = {
            timeframe:{symbol: pd.DataFrame() for symbol in symbols}
                for timeframe in timeframes
            }
    def update_poss_mps(self,poss):
        """
        poss = {
            's1':{
                'pos':2,
                'mp':105.5
            },
            's2':{
                'pos':-1,
                'mp':103.5
            }
        }
        """
        for s in poss:
            self.positions[s] = poss[s]['pos']
            self.middle_price[s] = poss[s]['mp']

    def preprocessing(self,dfs:Dict,poss:Dict):
        """
        Получаем такие данные:
        dfs = {
            'tf1': {
                's1':df_s1,
                's2':df_s2
            },
            'tf2': {
                's1':df_s1,
                's2':df_s2
            }
        }
        poss = {
            's1':{
                'pos':2,
                'mp':105.5
            },
            's2':{
                'pos':-1,
                'mp':103.5
            }
        }
        Здесь необходимо произвести обработку в соответсвии со стратегией
        self.update_poss_mps(poss) #если необходимо
        for s in dfs['tf1']:
            df = dfs['tf1'][s]
            df = add_bollinger(df,**parameters)
            self.last_dfs['tf1'][s] = df
        """
        self.last_dfs = dfs.copy()
        return self.last_dfs

    def __call__(self, *args, **kwds):
        """
        Метод должен обновить требуемые позиции, если это необходимо.
        Здесь прописывается логика по которой обновляются позиции.
        Пример:
        row_imoexf5 = self.last_dfs['5m']['IMOEXF'].iloc[-1]
        row_imoexf60 = self.last_dfs['1H']['IMOEXF'].iloc[-1]
        if row_imoexf60['close'] < row_imoexf60['bbd'] and row_imoexf5['close'] < row_imoexf5['bbd']:
            self.need_pos['IMOEXF'] = 1
        """
        return self.need_pos
    
