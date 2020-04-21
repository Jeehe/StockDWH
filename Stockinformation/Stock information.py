#from pandas_datareader library  import stock information

import pandas as pd
import pandas_datareader.data as web
import datetime
import pymysql
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:P@ssword@localhost:3306/test?charset=utf8')

'''第一个参数为股票代码，
苹果公司的代码为"AAPL",国内股市采用的输入方式“股票代码”+“对应股市”，上证后面加上“.SS”，深圳后面加上“.SZ”
DataReader可从多个金融网站获取到股票数据，如“Yahoo! Finance” 、“Google Finance”等，这里以Yahoo为例。
第三、四个参数为股票数据的起始时间断。返回的数据格式为DataFrame。'''

symbol=['000002.SZ']
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 2, 1)

# try to collect data
try:
    data = web.DataReader(symbol, 'yahoo', start, end)
    data = pd.DataFrame(data)
    data['symbol'] = symbol
    data['Volume'] = data['Volume'].astype(int)
    data['Execute'] = 1

except:
    #data = pd.DataFrame(columns=['symbol'])
    #data = data.append({'symbol': symbol}, ignore_index=True)
    data['Execute'] = 0
    #data['Adj Close(-1)'] = -99.0
    #data['Prediction (Adj Close)'] = -99.0
    #data['Percentage Increase'] = -99.0

#df.to_sql('stockinfor',engine,if_exists='append')#插入数据库
print(data)



