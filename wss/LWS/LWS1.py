import pandas as pd
from wss.WSBase import WSBase

class LWS1_FIRSTGRID(WSBase):
    """грид-бот"""
    def __init__(self, symbols, timeframes, positions, middle_price, parameters):
        """
        parameters = {
            'lvls':(200,300,400,500),
            'us_lvl': None,
            'ds_lvl': 100,
            'grid_dir': 1
        }
        """
        super().__init__(symbols, timeframes, positions, middle_price, parameters)
        self.lvls = parameters['lvls']
        self.us_lvl = parameters['us_lvl']
        self.ds_lvl = parameters['ds_lvl']
        self.grid_dir = parameters['grid_dir']
        self.middle_lvl = sum(self.lvls) / len(self.lvls)
        self.in_work = True
        if self.grid_dir == 1: #long
            self.grid_func = self.long_grid
        elif self.grid_dir == -1:
            self.grid_func = self.short_grid
        else:
            self.grid_func = self.neutral_grid
    
    def long_grid(self,row,s):
        if self.ds_lvl:
            if row['close'] < self.ds_lvl:
                self.in_work = False
                return False    
        if self.us_lvl:
            if row['close'] > self.us_lvl:
                self.need_pos[s] = 0
                return True
        new_pos = 0
        for lvl in self.lvls:
            if row['close'] <= lvl:
                new_pos += 1
        self.need_pos[s] = new_pos
        return True
    
    def short_grid(self,row,s):
        if self.us_lvl:
            if row['close'] > self.us_lvl:
                self.in_work = False
                return False    
        if self.ds_lvl:
            if row['close'] < self.ds_lvl:
                self.need_pos[s] = 0
                return True
        new_pos = 0
        for lvl in self.lvls:
            if row['close'] >= lvl:
                new_pos -= 1
        self.need_pos[s] = new_pos
        return True
    
    def neutral_grid(self,row,s):
        if self.us_lvl:
            if row['close'] > self.us_lvl:
                self.in_work = False
                return False    
        if self.ds_lvl:
            if row['close'] < self.ds_lvl:
                self.in_work = False
                return False 
        new_pos = 0
        for lvl in self.lvls:
            if row['close'] <= lvl < self.middle_lvl: #long
                new_pos += 1
            if row['close'] >= lvl > self.middle_lvl: #short
                new_pos -= 1
        self.need_pos[s] = new_pos
        return True
    
    def __call__(self, *args, **kwds):
        if self.in_work:
            tf1 = self.timeframes[0]
            for s in self.last_dfs[tf1]:
                row = self.last_dfs[tf1][s].iloc[-1]
                if not self.grid_func(row,s):
                    break
        else:
            self.need_pos = {s: 0 for s in self.symbols}
        return self.need_pos


        
