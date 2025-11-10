import pandas as pd
from typing import Dict, List, Any, Optional, Union
from traders.TraderBase import TraderBase
from wss.WSBase import WSBase

class TestTrader(TraderBase):
    def __init__(self, 
                symbols:List[str],
                timeframes:List[str|int],
                quantity:List[int],
                ws:WSBase = (WSBase,dict()),
                sufix_debug='Test1', 
                need_debug=False, 
                charts:Dict[str,str]=dict(), 
                fee=0.0002,
                close_on_time=False,
                close_map=((23,30),(23,30),(23,30),(23,30),(23,30),(17,50),(17,50),)):
        """
        charts = {
        'tf1': {
            's1':'./df1.csv',
            's2':'./df2.csv'
            }
        }
        Важно!!! Таймфреймы передаются от меньшего к большему!
        (1,5,60) ✔
        (60,5,1) ❌
        """
        super().__init__(symbols, timeframes, quantity, ws, sufix_debug, need_debug)
        self.charts = charts
        self.read_dfs()
        self.get_total_time_range()
        self.trade_data = {
            symbol : {
                'total':0,
                'count':0,
                'fees': 0,
                'total_wfees_per':0,
                'equity':[0],
                'equity_fee':[0],
                'pos':0,
                'mp':0,
                'o_longs':[],
                'o_shorts':[],
                'c_longs':[],
                'c_shorts':[]
            } for symbol in self.symbols
        }
        self.fee_one_p = (fee / 2) * 100
        self.open_fee = {symbol:0 for symbol in self.symbols}
        self.close_on_time = close_on_time
        self.close_map = close_map

    def read_dfs(self):
        for t in self.charts:
            for s in self.charts[t]:
                path_df = self.charts[t][s]
                if path_df.endswith('.parquet'):
                    df = pd.read_parquet(path_df)
                else:
                    df = pd.read_csv(path_df)
                self.charts[t][s] = df
    
    def get_total_time_range(self):
        tf1 = self.timeframes[0]
        start_time = None
        end_time = None
        
        # Находим самое позднее время начала и самое раннее время окончания
        for s in self.charts[tf1]:
            df = self.charts[tf1][s]
            
            # Преобразуем столбец ms в datetime, если еще не сделано
            if not pd.api.types.is_datetime64_any_dtype(df['ms']):
                df['ms'] = pd.to_datetime(df['ms'], format='%Y-%m-%d %H:%M:%S')
            
            # Находим минимальное и максимальное время для текущего символа
            current_start = df['ms'].min()
            current_end = df['ms'].max()
            
            # Обновляем общее время начала (берем самое позднее)
            if start_time is None or current_start > start_time:
                start_time = current_start
            
            # Обновляем общее время окончания (берем самое раннее)
            if end_time is None or current_end < end_time:
                end_time = current_end
        self.start_time = start_time
        self.end_time = end_time
        # Теперь нужно проверить все таймфреймы, а не только первый
        if len(self.timeframes) > 1:
            for tf in self.timeframes[1:]:  # начинаем со второго таймфрейма
                for s in self.charts[tf]:
                    df = self.charts[tf][s]
                    
                    if not pd.api.types.is_datetime64_any_dtype(df['ms']):
                        df['ms'] = pd.to_datetime(df['ms'], format='%Y-%m-%d %H:%M:%S')
                    
                    current_start = df['ms'].min()
                    current_end = df['ms'].max()
                    
                    # Обновляем общее время начала
                    if current_start > start_time:
                        start_time = current_start
                    
                    # Обновляем общее время окончания
                    if current_end < end_time:
                        end_time = current_end
        self.all_start_time = start_time
        self.all_end_time = end_time
    
    def get_deep_copy_last_dfs(self):
        # Глубокое копирование всей структуры
        dfs = {}
        for tf in self.ws.last_dfs:
            dfs[tf] = {}
            for s in self.ws.last_dfs[tf]:
                dfs[tf][s] = self.ws.last_dfs[tf][s].copy(deep=True)
        return dfs

    def check_fast(self):
        poss = self._check_position()
        self.ws.preprocessing(self.charts,poss)
        dfs = self.get_deep_copy_last_dfs()
        tf1 = self.timeframes[0]
        dates_df1 = dfs[tf1][self.symbols[0]]['ms'].to_list()
        for d in dates_df1:
            for tf in dfs:
                for s in dfs[tf]:
                    df = dfs[tf][s].copy()
                    filtered_df = df[df['ms'] <= d]
                    # Обновляем датафрейм в основном хранилище
                    self.ws.last_dfs[tf][s] = filtered_df
            need_pos = self.ws()
            if self.close_on_time:
                last_row = self.ws.last_dfs[tf1][self.symbols[0]].iloc[-1]
                time_close = self.close_map[last_row['weekday']]
                if last_row['ms'].dt.hour >= time_close[0] and last_row['ms'].dt.minute >= time_close[0]:
                    for s in need_pos:
                        need_pos[s] = 0
            print(d,s,need_pos)
            # for tf in self.ws.last_dfs:
            #     for s in self.ws.last_dfs[tf]:
            #         print(tf,s)
            #         self.ws.last_dfs[tf][s].info()



    
    def check_window(self,window_size=150):
        ...
    
    def check_child(self,timeframe='5min'):
        ...
