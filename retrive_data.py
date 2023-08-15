from smartapi import SmartConnect
from smartapi import smartExceptions
from config import *
import pandas as pd
import logging

def candle_param(token, formdate, todate):
    param ={
            "exchange": "NSE",
            "symboltoken": token,
            "interval": "FIFTEEN_MINUTE",
            "fromdate": formdate,
            "todate": todate,
            }
    return param


def candle_data(obj, param):
    try:
        candle = obj.getCandleData(param)
    except smartExceptions as e:
        print("Historic Api failed: {}".format(e.args))

        candle = []
    return candle


def order():
    api_key = API_KEY_MJ
    obj = SmartConnect(api_key=api_key,)
    print(obj)
    userid = USERID_MJ
    password = PASSWORD_MJ
    data = obj.generateSession(userid,password)
    refreshToken = data['data']['refreshToken']
    feedToken = obj.getfeedToken()
    userProfile = obj.getProfile(refreshToken)
    return obj


def equityParam(SYMBOL,TOKEN,PRICE,QUANTITY):
    param ={
        "variety": "STOPLOSS",
        "tradingsymbol": SYMBOL +"-EQ",
        "symboltoken": str(TOKEN),
        "transactiontype": "SELL",
        "exchange": "NSE",
        "ordertype": "STOPLOSS_MARKET",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "triggerprice": str(PRICE),
        "price": "0.0",
        "squareoff": "0.0",
        "stoploss": "0.0",
        "quantity": str(QUANTITY),
        }
    return param
    #


def give_param(TYPE,SYMBOL,TOKEN,PRICE,QUANTITY,ORDERTYPE,VARIETY,EXCHANGE):

    param ={
        "variety": VARIETY,
        "tradingsymbol": SYMBOL,
        "symboltoken": str(TOKEN),
        "transactiontype": TYPE,
        "exchange": EXCHANGE,
        "ordertype": ORDERTYPE,
        "producttype": "INTRADAY",
        "duration": "DAY",
        "triggerprice": str(PRICE),
        "price": "0.0",
        "squareoff": "0.0",
        "stoploss": "0.0",
        "quantity": str(QUANTITY),
        }
    return param


def equity_order(obj,param):
    orderid = 0
    try:
        orderId = obj.placeOrder(param)

        print("The order id is: {}".format(orderId))
        return orderId
    except BaseException as e:
        print("Order placement failed: {}".format(e.args))
        return None
    except smartExceptions as e:
        print("Order placement failed: {}".format(e.message))
        return None


def equity_modify(ORDERID,SYMBOL,TOKEN,QUANTITY,TYPE):
    param = {
        "variety": "NORMAL",
        "orderid": str(ORDERID),
        "ordertype": "MARKET",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "transactiontype": TYPE,
        "price": "0.0",
        "quantity": str(QUANTITY),
        "tradingsymbol": SYMBOL+"-EQ",
        "symboltoken": str(TOKEN),
        "exchange": "NSE"
    }
    return param


def stoploss_param(SYMBOL,TOKEN,QUANTITY,STOPLOSS,TYPE):
    param = {
        "variety": "STOPLOSS",
        "tradingsymbol": SYMBOL +"-EQ",
        "symboltoken": str(TOKEN),
        "transactiontype": TYPE,
        "exchange": "NSE",
        "ordertype": "STOPLOSS_MARKET",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "triggerprice": str(STOPLOSS-1),
        "price": "0.0",
        "squareoff": "0.0",
        "stoploss": "0.0",
        "quantity": str(QUANTITY),
        }
    return param


def get_data_trading_view(stock,tv,charttime =15):

    import time
    from tvDatafeed import Interval
    try:
        if charttime ==5:
            df = tv.get_hist(stock, 'NSE', interval=Interval.in_5_minute, n_bars=100)
        else:
            df = tv.get_hist(stock, 'NSE', interval=Interval.in_15_minute, n_bars=100)
    except:
        time.sleep(1)
        df = get_data_trading_view(stock,tv)
    return df


def trading_view():
    from tvDatafeed import TvDatafeed
    username = ''
    password = ''
    tv = TvDatafeed(username=username, password=password)
    return tv


def data_cleann(data):
    data = data.reset_index()

    data.columns = ["Date", "symbol", "Open", "High", "Low", "Close", "Volume"]
    # print(data)
    # data['Date'] = [datetime.datetime.strptime(data['Date'].iloc[x], "%Y-%m-%d %H:%M:%S")
    #                 for x in range(len(data))]

    data['Nine'] = [True if data['Date'].iloc[x].hour == 9 and data['Date'].iloc[x].minute == 0 else False
                    for x in range(len(data))]
    data.drop(data[data['Nine'] == True].index, inplace=True)
    data['Three'] = [True if data['Date'].iloc[x].hour == 15 and data['Date'].iloc[x].minute == 30 else False
                    for x in range(len(data))]
    data.drop(data[data['Three'] == True].index, inplace=True)
    data.drop('Three', inplace=True, axis=1)
    data.drop('Nine', inplace=True, axis=1)

    data.drop(data.tail(1).index, inplace=True)
    print(data.tail(1))
    return data


def data_clean(data):
    from datetime import datetime
    import pandas as pd


    data = data.reset_index()

    data.columns = ["Date", "symbol", "Open", "High", "Low", "Close", "Volume"]
    # print(data)
    # data['Date'] = [datetime.datetime.strptime(data['Date'].iloc[x], "%Y-%m-%d %H:%M:%S")
    #                 for x in range(len(data))]

    data['Nine'] = [True if data['Date'].iloc[x].hour == 9 and data['Date'].iloc[x].minute == 0 else False
                    for x in range(len(data))]
    data.drop(data[data['Nine'] == True].index, inplace=True)
    data['Three'] = [True if data['Date'].iloc[x].hour == 15 and data['Date'].iloc[x].minute == 30 else False
                    for x in range(len(data))]
    data.drop(data[data['Three'] == True].index, inplace=True)
    data.drop('Three', inplace=True, axis=1)
    data.drop('Nine', inplace=True, axis=1)
    min = datetime.now().minute
    hr = datetime.now().hour
    dates = data['Date'][-1:].values[0]
    dates = pd.to_datetime(dates)
    min1 = dates.minute
    hr1 = dates.hour
    if min== min1 and hr == hr1:
        data.drop(data.tail(1).index, inplace=True)
    return data

def strad_Token(expiry):
    import requests
    BASE_URL = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'

    data = requests.get(BASE_URL)
    df = data.json()
    strike = 30000
    EXPIRY = expiry
    symbol = []
    token = []


    for item in range(100):

        symbolce = 'BANKNIFTY' + EXPIRY + str(strike) + 'CE'
        symbolpe = 'BANKNIFTY' + EXPIRY + str(strike) + 'PE'
        for items in df:
            for key, value in items.items():
                if value == symbolce:
                    tokenc = items['token']
                    symbol.append(symbolce)
                    token.append(tokenc)
                if value == symbolpe:
                    tokenp = items['token']
                    symbol.append(symbolpe)
                    token.append(tokenp)




        strike += 100
    df1 = pd.DataFrame(symbol , columns = ['Symbol'])
    df2 = pd.DataFrame(token , columns = ['Token'])
    df1 = df1.join(df2)
    df1.to_csv('token.csv')

if __name__ == '__main__':
    strad_Token('30SEP21')