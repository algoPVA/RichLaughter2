import os
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from wss.WSBase import WSBase

class TraderBase:
    def __init__(self, symbols:List[str],timeframes:List[str|int],quantity:List[int],ws:WSBase = (WSBase,tuple()),sufix_debug='TB',need_debug=False):
        self.symbols = symbols
        self.timeframes = timeframes
        self.quantity_map = dict(zip(self.symbols, quantity))
        poss = self._check_position()
        pos = {k: v['pos'] for k, v in poss.items()}
        mp = {k: v['mp'] for k, v in poss.items()}
        self.ws:WSBase = ws[0](self.symbols,self.timeframes,pos,mp,ws[1])

        self.need_debug = need_debug
        if need_debug:
            self._debug_folder_create(sufix_debug)
        folder_error = 'logs/error_logs' + sufix_debug
        if not os.path.exists(folder_error):
            os.makedirs(folder_error)
        self.error_log = { symbol:
            os.path.join(folder_error,sufix_debug + '_' + symbol + '.txt')
            for symbol in self.symbols}

    def _debug_folder_create(self,sufix_debug):
        folder_debug = 'logs/debug_logs' + sufix_debug
        if not os.path.exists(folder_debug):
            os.makedirs(folder_debug)
        self.debug_log = { symbol:
            os.path.join(folder_debug,sufix_debug + '_' + symbol + '.txt')
            for symbol in self.symbols}


    def start_info(self):
        print('TraderBase')

    def _get_balance(self):
        pass
    
    def _check_risk(self):
        pass

    def _check_time(self):
        pass

    def _check_position(self) -> Dict:
        return {symbol: {
            'pos':0,
            'mp':0
        } for symbol in self.symbols}

    def _check_req(self):
        pass

    def _send_open(self,direction,quantity):
        pass

    def _send_close(self,direction,quantity):
        pass

    def _reverse_pos(self,direction):
        pass
    
    def _close_all_pos(self):
        pass

    def _reset_req(self):
        pass

    def _get_df(self,symbol,timeframe) -> pd.DataFrame:
        df = pd.DataFrame()
        return df

    def _get_dfs(self) -> Dict:
        dfs = {
            tf: {symbol: self._get_df(symbol,tf) for symbol in self.symbols}
            for tf in self.timeframes
        }
        return dfs
    
    def _debug_log(self,content):
        now = datetime.now()
        with open(self.debug_log,'a',encoding="utf-8") as f:
            f.write('vvvvvvvvvvvvv__' + str(now) + '__vvvvvvvvvvvvv' + '\n')
            f.write(content)

    
    def _get_need_pos(self):
        dfs = self._get_dfs()
        poss = self._check_position()
        self.ws.preprocessing(dfs,poss)
        need_pos = self.ws()
        return need_pos
    
    def _work_ws(self,need_pos,cur_pos):
        pass
    
    def run(self):
        pass