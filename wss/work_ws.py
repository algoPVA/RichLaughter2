import pandas as pd
from wss.WSBase import WSBase


class WorkWS(WSBase):
    """period_dc"""
    def __init__(self, symbols, timeframes, positions, middle_price, parameters):
        super().__init__(symbols, timeframes, positions, middle_price, parameters)
        """period_dc"""
        self.period_dc = parameters['period_dc']

    def preprocessing(self, dfs, poss):
        self.update_poss_mps(poss)
        for t in dfs:
            for s in dfs[t]:
                df:pd.DataFrame = dfs[t][s]
                df[['up_dc','down_dc']] = df['close'].rolling(self.period_dc).agg(['max','min'])
                df['m_dc'] = (df['up_dc'] + df['down_dc']) / 2
                self.last_dfs[t][s] = df
                # df['up_dc'] = roll.max()
                # df['down_dc'] = roll.min()
        return self.last_dfs
    
    def __call__(self, *args, **kwds):
        tf1 = self.timeframes[0]
        tf2 = self.timeframes[1]
        symbol = self.symbols[0]
        symbol_r = self.symbols[1]
        row_tf1 = self.last_dfs[tf1][symbol].iloc[-1]
        row_tf2 = self.last_dfs[tf2][symbol].iloc[-1]
        if row_tf1['high'] == row_tf1['up_dc'] and row_tf2['close'] < row_tf2['m_dc']:
            self.need_pos[symbol] = -1
        if row_tf2['high'] == row_tf2['up_dc']:
            self.need_pos[symbol] = -2
            self.need_pos[symbol_r] = 1
        if row_tf1['low'] == row_tf1['down_dc'] and row_tf2['close'] > row_tf2['m_dc']:
            self.need_pos[symbol] = 1
        if row_tf2['low'] == row_tf2['down_dc']:
            self.need_pos[symbol] = 2
            self.need_pos[symbol_r] = -1
        return self.need_pos