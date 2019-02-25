import requests
import pandas as pd


def get_price(url):
    #get request
    res = requests.get(url)
    #compile json format get the data from ['stats']
    data_prices = res.json()['stats']
    #convert data_prices to dataframe
    df = pd.DataFrame(data_prices)
    #set columns name
    df.columns = ['datetime', 'twd']
    #convert datetime(ms) to datetime
    df['datetime'] = pd.to_datetime(df['datetime'], unit = 'ms')
    #set inedx
    df.index = df['datetime']
    return df


#=====================================================


# url = 'https://www.coingecko.com/price_charts/1/twd/90_days.json'
# bitcoin = get_price(url)
# #create a columns call 'ma'
# bitcoin['ma'] = bitcoin['twd'].rolling(window = 100).mean()
# bitcoin[['twd', 'ma']].plot(kind = 'line', figsize = [15, 5], xlim = ['2018-12-01', '2018-12-30'])
