#from pandas_datareader library  import stock information
import pandas as pd
import pandas_datareader.data as web
import datetime
start = datetime.datetime(2019, 1, 1)
end = datetime.datetime(2020, 4, 1)
'''第一个参数为股票代码，
苹果公司的代码为"AAPL",国内股市采用的输入方式“股票代码”+“对应股市”，上证股票在股票代码后面加上“.SS”，深圳股票在股票代码后面加上“.SZ”
DataReader可从多个金融网站获取到股票数据，如“Yahoo! Finance” 、“Google Finance”等，这里以Yahoo为例。
第三、四个参数为股票数据的起始时间断。返回的数据格式为DataFrame。
'''
stock='000002.sz'
data = web.DataReader(stock, 'yahoo', start, end)
data=pd.DataFrame(data)
print(data)
