import pandas as pd
import traceback
from time import sleep
from datetime import datetime
from typing import Dict, List
from traders.TraderBase import TraderBase
from traders.QuikTrader.help_funcs import get_bars,get_best_glass,get_pos_futures,close_active_order,send_transaction,get_code_orders,smart_close_active_order,get_order_by_trans_id
from wss.WSBase import WSBase

class QuikTrader(TraderBase):
    def __init__(self, 
                symbols:List[str],
                timeframes:List[str|int],
                quantity:List[int],
                ws:WSBase = (WSBase,dict()),
                sufix_debug='QT', 
                need_debug=False,
                amount_bars=200,
                class_codes:str|List[str]='SPBFUT',
                close_on_time=True,
                close_map=((22,30),(22,30),(22,30),(22,30),(22,30),(17,30),(17,30),)):
        super().__init__(symbols, timeframes, quantity, ws, sufix_debug, need_debug)
        self.amount_bars = amount_bars
        if isinstance(class_codes,str):
            self.class_codes = [class_codes for s in self.symbols]
        else:
            self.class_codes = class_codes

        self.start_pos = self._check_position()
        self.close_on_time = close_on_time
        now = datetime.now()
        cwd = now.weekday()
        self.close_time = close_map[cwd]
        self.start_time = {
            'day': now.day,
            'hour': now.hour,
            'min': now.minute,
            'month': now.month,
            'sec': now.second,
            'year': now.year
        }
        self.last_order_id = {s: None for s in self.symbols}
        self.last_kill_order_id = {s: None for s in self.symbols}
        self.orders_start = {s: False for s in self.symbols}
        self.symbol_range = range(len(self.symbols))


    def start_info(self):
        print('QuikTrader')

    def _get_balance(self):
        pass
    
    def _check_risk(self):
        pass

    def _check_time(self):
        now = datetime.now()
        chour = now.hour
        cminute = now.minute
        if chour > 8:
            if chour >= self.close_time[0] - 1:
                if cminute > self.close_time[1]:
                    if chour == self.close_time[0]:
                        return -1
                    else:
                        return -2
                elif chour == self.close_time[0]:
                    return -2
            return 1
        return 0
    
    def _check_today(self,order):
        date_order = order['datetime']
        if date_order['year'] != self.start_time['year']:
            return False
        if date_order['month'] != self.start_time['month']:
            return False
        if date_order['day'] != self.start_time['day']:
            return False
        if date_order['hour'] > self.start_time['hour']:
            return True
        if date_order['hour'] < self.start_time['hour']:
            return False
        if date_order['hour'] == self.start_time['hour']:
            if date_order['min'] < self.start_time['min']:
                return False
            if date_order['min'] == self.start_time['min'] and date_order['sec'] < self.start_time['sec']:
                return False
        return True
    
    def _check_position(self):
        poss = {}
        for s in self.symbols:
            pos = get_pos_futures(s)
            mp = 0 #заменим потом методом
            poss[s] = {
               'pos':pos,
               'mp':mp 
            }
        return poss
    
    def _check_position_on_order(self):
        """ON ORDER"""
        poss = {}
        for s in self.symbols:
            orders = get_code_orders(s)
            pos = self.start_pos[s]['pos']
            for order in orders:
                flags = bin(order['flags'])
                if flags[-1] == '0' and flags[-2] == '0':
                    delta = order['qty']
                else:
                    delta = order['qty'] - order['balance']
                if self._check_today(order):
                    if flags[-3] == '1':
                        pos -= delta
                    else:
                        pos += delta
            mp = 0 #заменим потом методом
            poss[s] = {
               'pos':int(pos),
               'mp':mp 
            }
        return poss
    
    def _check_last_order(self):
        for s in self.symbols:
            if self.orders_start[s]:
                last_order_id = self.last_order_id[s]
                last_order = get_order_by_trans_id(last_order_id)
                if not last_order:
                    print(datetime.now(),s, 'not see last order:', last_order_id)
                    return False
        return True


    def _check_req(self):
        pass

    def _send_open(self,direction,quantity,index):
        symbol = self.symbols[index]
        class_code = self.class_codes[index]
        bbid,bask = get_best_glass(symbol,class_code)
        price = bbid if direction == 'B' else bask
        self.last_kill_order_id[symbol], skip_close = smart_close_active_order(symbol,price)
        if skip_close == 0:
            self.last_order_id[symbol] = send_transaction(symbol,price,direction,quantity,class_code)
        if not self.orders_start[symbol]:
            self.orders_start[symbol] = True

    def _send_close(self,direction,quantity,index):
        rev_direction = 'B' if direction == 'S' else 'S'
        self._send_open(rev_direction,quantity,index)

    def _reverse_pos(self,direction):
        pass
    
    def _close_all_pos(self):
        pass

    def _reset_req(self,symbol):
        self.last_kill_order_id[symbol] = close_active_order(symbol)

    def _get_dfs(self) -> Dict[str,Dict[str,pd.DataFrame]]:
        dfs = {}
        for tf in self.timeframes:
            dfs[tf] = {}
            for i,s in enumerate(self.symbols):
                df = get_bars(s,tf,self.amount_bars,self.class_codes[i])
                dfs[tf][s] = df
        return dfs
    
    def _debug_log(self,symbol,pos,need_pos):
        now = datetime.now()
        with open(self.debug_log[symbol],'a',encoding="utf-8") as f:
            f.write('vvvvvvvvvvvvv__' + str(now) + '__vvvvvvvvvvvvv' + '\n')
            f.write('pos: '+ str(pos) + '\n')
            f.write('need_pos: '+ str(need_pos) + '\n')

    def _action_debug_log(self,symbol,pos,need_pos):
        if self.need_debug:
            self._debug_log(symbol,pos,need_pos)

    def _work_ws(self,symbol,npos,pos,index):
        if npos != pos:
            delta_pos = npos - pos
            q = self.quantity_map[symbol] * delta_pos
            if delta_pos > 0: #long
                self._send_open('B',q,index)
                self._action_debug_log(symbol,pos,npos)
            else: #short
                self._send_open('S',q,index)
                self._action_debug_log(symbol,pos,npos)
        else:
            self._reset_req(symbol)     

    def run(self):
        try:
            time_mode = self._check_time()
            if time_mode == 0:
                sleep(60*5)
                return
            else:
                if not self._check_last_order():
                    return
                dfs = self._get_dfs()
                poss = self._check_position_on_order()
                self.ws.preprocessing(dfs,poss)
                need_pos = self.ws()
                if time_mode == -1:
                    need_pos = {s: 0 for s in self.symbols}
                for i in self.symbol_range:
                    symbol = self.symbols[i]
                    npos = need_pos[symbol]
                    pos = poss[symbol]['pos']
                    self._work_ws(symbol,npos,pos,i)
        except Exception as err:
            print(datetime.now(),self.symbols,f"!!!! {type(err).__name__}: {err} !!!!")
            with open(self.error_log['main'],'a',encoding="utf-8") as f:
                f.write(str(datetime.now()) + "\n")
                f.write('\n')
                f.write(traceback.format_exc() + "\n")

