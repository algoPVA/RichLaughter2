from loaders.api_moex_loader.api_moex_loader import ApiMoexLoader
from datetime import date,timedelta

today = date.today()
start_date = str(today - timedelta(days=5))
# # start_date = '2025-02-01'

loader = ApiMoexLoader('IMOEXF','RFUD','forts','futures')

loader.save_df(start_date,timeframe=1,sformat='csv')
loader.save_df(start_date,timeframe=10,sformat='csv')

loader = ApiMoexLoader('MMZ5','RFUD','forts','futures')
loader.save_df(start_date,timeframe=1,sformat='csv')
loader.save_df(start_date,timeframe=10,sformat='csv')