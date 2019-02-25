import requests
import bitcoin_module as m
import pandas as pd


def strategy(df, total, ma_num, stop_earn):
    #以制定的ma大小計算均線
    df['ma'] = df['twd'].rolling(window = ma_num).mean()
    #去掉一開始window大小不夠的none值
    df = df[ma_num-1:]
    #進場點
    entry_price = 0
    #最高點
    max_price = 0
    #最低點
    min_price = 0
    #狀態default: wait_long 等待做多
    state = 'wait_long'
    for i in range(len(df)):
        #等待作多
        if state == 'wait_long':
            #當price（twd） > ma時將進場點與最高點設為現價並轉移狀態為：entry_long進場作多
            if df['twd'][i] > df['ma'][i]:
                max_price = df['twd'][i]
                #存一下進場價格
                entry_price = df['twd'][i]
                #轉移狀態為entry_long
                state = 'entry_long'
        #等待做空
        elif state == 'wait_short':
            #當twd < ma時將entry_price與min_price設為現價並轉移state為entry_short
            if df['twd'][i] < df['ma'][i]:
                min_price = df['twd'][i]
                entry_price = df['twd'][i]
                state = 'entry_short'
        #進場做多
        elif state == 'entry_long':
            if df['twd'][i] > max_price:
                max_price = df['twd'][i]
            if df['twd'][i] < max_price:
                total += df['twd'][i] - entry_price
                state = 'wait_short'
            elif df['twd'][i] - entry_price > stop_earn and stop_earn != 0:
                total += df['twd'][i] - entry_price
                #出場並等待做空
                state = 'wait_short'
        #進場做空
        elif state == 'entry_short':
            if df['twd'][i] < min_price:
                min_price - df['twd'][i]
            if df['twd'][i] < min_price:
                total += entry_price - df['twd'][i]
                #出場並等待作多
                state = 'wait_long'
            elif entry_price - df['twd'][i] > stop_earn and stop_earn != 0:
                total +=entry_price - df['twd'][i]
                state = 'wait_long'

    return total

url = 'https://www.coingecko.com/price_charts/1/twd/90_days.json'
bitcoin = m.get_price(url)
total = strategy(bitcoin, 100000, 200, 1000)
print(total)














