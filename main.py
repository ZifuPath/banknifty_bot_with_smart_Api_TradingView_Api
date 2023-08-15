import datetime

import pandas as pd
from smartapi import smartExceptions
from retrive_data import *
import datetime as dt
import time
import logging

logging.basicConfig(filename='log.log',encoding='utf-8', level=logging.INFO,format='%(asctime)s %(message)s')
tv = trading_view()
def bot_kakad(obj,tv,expiry):

    buy_order = False
    sell_order = False
    data = pd.read_csv('token.csv')
    token ={data['Symbol'].iloc[x] : data['Token'].iloc[x] for x in data.index}
    # print(token)
    while dt.time(9,30) > dt.datetime.now().time():
        time.sleep(1)
    df = get_data_trading_view('BANKNIFTY',tv)
    df = data_clean(df)
    print(df.tail(2))
    for item in df.index:
        # print(df['Date'].iloc[item])
        if df['Date'].iloc[item].day == datetime.datetime.now().day and df['Date'].iloc[item].hour== 9 and df['Date'].iloc[item].minute == 15:
            open_value = df['Open'].iloc[item]
            print(open_value)
            if df['Open'].iloc[item] < df['Close'].iloc[item]:
                condition = 'SELL'
                logging.info(f'SELL condition with {open_value}')
            else:
                condition = 'BUY'
                logging.info(f'BUY condition with {open_value}')
            break
    time.sleep(100)
    # condition = 'BUY'
    # open_value = 34747
    while condition == 'BUY':
        try:
            val = dt.datetime.now().minute
            condition_any = [val == 0, val == 5, val == 10, val == 15,
                             val == 20, val == 25, val == 30, val == 35,
                             val == 40, val == 45, val == 50, val == 55]
            if condition_any:
                df = get_data_trading_view(stock='BANKNIFTY', tv=tv,charttime=5)
                df = data_clean(df)
                if open_value < df['Close'][-1:].values[0]<open_value+50:
                    target = df['Close'][-1:].values[0] + 300
                    strike = round((df['Close'][-1:].values[0])/100 ) * 100

                    buy1 = 'BANKNIFTY'+expiry+str(strike)+'PE'
                    sell1 = 'BANKNIFTY'+expiry+str(strike-500)+'PE'
                    buy_order = True

                    param1 = give_param(TYPE="SELL", SYMBOL=buy1, TOKEN=token.get(buy1), PRICE=0,
                               QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                    param2 = give_param(TYPE="BUY", SYMBOL=sell1, TOKEN=token.get(buy1), PRICE=0,
                               QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                    b1 = equity_order(obj,param2)
                    time.sleep(1)
                    s1 = equity_order(obj, param1)
                    time.sleep(60)
                    logging.info(f'ENTERED TRADE - {buy1} is Bought and {sell1} is sold')
                    break
                time.sleep(60)
            if dt.time(15, 1) < dt.datetime.now().time():
                break

        except smartExceptions as e:
                logging.error(msg = e.msg)
                time.sleep(2)

        except smartExceptions as e:
                logging.error(msg = e.msg)
                time.sleep(2)

    while condition == 'SELL':
        try:
            val = dt.datetime.now().minute
            condition_any = [val == 0, val == 5, val == 10, val == 15,
                             val == 20, val == 25, val == 30, val == 35,
                             val == 40, val == 45, val == 50, val == 55]
            if any(condition_any):
                df = get_data_trading_view(stock='BANKNIFTY', tv=tv, charttime=5)
                df = data_clean(df)
                if open_value > df['Close'][-1:].values[0]> open_value-50:
                    target = df['Close'][-1:].values[0] - 250
                    strike = round((df['Close'][-1:].values[0]) / 100 )*100

                    buy1 = 'BANKNIFTY' + expiry + str(strike) + 'CE'
                    sell1 = 'BANKNIFTY' + expiry + str(strike + 500) + 'CE'
                    sell_order = True

                    param1 = give_param(TYPE="SELL", SYMBOL=buy1, TOKEN=token.get(buy1), PRICE=0,
                                        QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                    param2 = give_param(TYPE="BUY", SYMBOL=sell1, TOKEN=token.get(buy1), PRICE=0,
                                        QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                    b1 = equity_order(obj, param2)
                    time.sleep(1)
                    s1 = equity_order(obj, param1)
                    time.sleep(60)
                    logging.info(f'ENTERED TRADE - {buy1} is Bought and {sell1} is sold')
                    break
                time.sleep(60)
            if dt.time(15, 1) < dt.datetime.now().time():
                break
        except smartExceptions as e:
            logging.error(msg=e.msg)
            time.sleep(2)

        except smartExceptions as e:
            logging.error(msg=e.msg)
            time.sleep(2)

    while buy_order:
        time.sleep(60)
        try:
            val = dt.datetime.now().minute
            condition_any = [val == 0, val == 15, val == 30, val == 45]
            if any(condition_any):
                df = get_data_trading_view(stock='BANKNIFTY', tv=tv)
                df = data_clean(df)
                stop_loss = open_value-50
                if stop_loss > df['Close'][-1:].values[0]:
                    param2 = give_param(TYPE="BUY", SYMBOL=buy1, TOKEN=token.get(buy1), PRICE=0,
                                        QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                    param1 = give_param(TYPE="SELL", SYMBOL=sell1, TOKEN=token.get(buy1), PRICE=0,
                                        QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                    b1 = equity_order(obj, param1)
                    time.sleep(1)
                    s1 = equity_order(obj, param2)
                    time.sleep(60)
                    logging.info(f'Exited TRADE - {buy1} is Sold and {sell1} is Bought')
                    break
                if target < df['Close'][-1:].values[0]:
                    param2 = give_param(TYPE="BUY", SYMBOL=buy1, TOKEN=token.get(buy1), PRICE=0,
                                        QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                    param1 = give_param(TYPE="SELL", SYMBOL=sell1, TOKEN=token.get(sell1), PRICE=0,
                                        QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                    b1 = equity_order(obj, param1)
                    time.sleep(1)
                    s1 = equity_order(obj, param2)
                    time.sleep(60)
                    logging.info(f'Exited TRADE - {buy1} is Sold and {sell1} is Bought')
                    break

            if dt.time(15, 14) < dt.datetime.now().time():
                param2 = give_param(TYPE="BUY", SYMBOL=buy1, TOKEN=token.get(buy1), PRICE=0,
                                    QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                param1 = give_param(TYPE="SELL", SYMBOL=sell1, TOKEN=token.get(sell1), PRICE=0,
                                    QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                b1 = equity_order(obj, param1)
                time.sleep(1)
                s1 = equity_order(obj, param2)
                time.sleep(60)
                logging.info(f'Exited TRADE - {buy1} is Sold and {sell1} is Bought')
                break
        except smartExceptions as e:
            logging.error(msg=e.msg)
            time.sleep(2)

        except smartExceptions as e:
            logging.error(msg=e.msg)
            time.sleep(2)

    while sell_order:
        time.sleep(60)
        try:
            val = dt.datetime.now().minute
            condition_any = [val == 0, val == 15, val == 30, val == 45]
            if any(condition_any):
                df = get_data_trading_view(stock='BANKNIFTY', tv=tv)
                df = data_clean(df)
                stop_loss = open_value+50
                if stop_loss > df['Close'][-1:].values[0]:
                    param2 = give_param(TYPE="BUY", SYMBOL=buy1, TOKEN=token.get(buy1), PRICE=0,
                                        QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                    param1 = give_param(TYPE="SELL", SYMBOL=sell1, TOKEN=token.get(sell1), PRICE=0,
                                        QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                    b1 = equity_order(obj, param1)
                    time.sleep(1)
                    s1 = equity_order(obj, param2)
                    time.sleep(60)
                    logging.info(f'Exited TRADE - {buy1} is Sold and {sell1} is Bought')
                    break
                if target < df['Close'][-1:].values[0]:
                    param2 = give_param(TYPE="BUY", SYMBOL=buy1, TOKEN=token.get(buy1), PRICE=0,
                                        QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                    param1 = give_param(TYPE="SELL", SYMBOL=sell1, TOKEN=token.get(sell1), PRICE=0,
                                        QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                    b1 = equity_order(obj, param1)
                    time.sleep(1)
                    s1 = equity_order(obj, param2)
                    time.sleep(60)
                    logging.info(f'Exited TRADE - {buy1} is Sold and {sell1} is Bought')
                    break
            if dt.time(15, 14) < dt.datetime.now().time():
                param2 = give_param(TYPE="BUY", SYMBOL=buy1, TOKEN=token.get(buy1), PRICE=0,
                                    QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                param1 = give_param(TYPE="SELL", SYMBOL=sell1, TOKEN=token.get(sell1), PRICE=0,
                                    QUANTITY=25, ORDERTYPE='MARKET', VARIETY='NORMAL', EXCHANGE="NFO")
                b1 = equity_order(obj, param1)
                time.sleep(1)
                s1 = equity_order(obj, param2)
                time.sleep(60)
                logging.info(f'Exited TRADE - {buy1} is Sold and {sell1} is Bought')
                break
        except smartExceptions as e:
            logging.error(msg=e.msg)
            time.sleep(2)

        except smartExceptions as e:
            logging.error(msg=e.msg)
            time.sleep(2)
if __name__ == '__main__':
    obj = order()
    tv = trading_view()
    expiry = '30SEP23'
    bot_kakad(obj,tv,expiry)
