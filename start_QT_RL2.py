from time import sleep
from work_inits.quik_trader_init import init_trader

bots = init_trader()
for bot in bots:
    print(bot.symbols)
print('Start trading...')
work = True
while work:
    for bot in bots:
        bot.run()
    sleep(15)