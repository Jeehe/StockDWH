#插入新浪国内新闻
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
import json
import pandas
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:P@ssword@localhost:3306/test?charset=utf8')
import pymysql
'''
c=url.split('/')[-1].rstrip('.shtml').lstrip('doc-i')#获取urlID
print(c)
res=requests.get(newslisturl)

scale=50
print("start".center(scale//2,"-"))
start=time.perf_counter()
for i in range(scale+1):
    a='*'* i
    b='.'* (scale-i)
    c=(i/scale)*100
    dur=time.perf_counter()-start
    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c,a,b,dur),end='')
    time.sleep(0.1)
print("\n"+"end".center(scale//2,'-'))
'''

def getnewsdetail(url):
    try:
        result={}
        r = requests.get(url,headers={'user-agent': 'Mozilla/5.0'})
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        result['title'] = soup.select('.main-title')[0].text  # 新闻标题
        if len(soup.select('.date-source a'))<1:#判断，个别网页标签不一致
            result['newssource']=soup.select('.date-source span')[1].text
        else:
            result['newssource']=soup.select('.date-source a')[0].text   # 新闻来源
        timesource = soup.select('.date-source')[0].contents[1].text  # 新闻时间&来源
        result['timesource'] = soup.select('.date-source')[0].contents[1].text  # 新闻时间
        result['dt']= datetime.strptime(timesource, '%Y年%m月%d日 %H:%M')  # 新闻时间转换为时间格式
        result['article'] = ' '.join([p.text.strip() for p in soup.select('#article p')[:-1]])  # 一行文 获取文章内容
        result['updatetime']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) #获取当前时间
        result['url'] = url
        return result
    except:
        return " "

#js里面抓取新闻列表来源连接
def parserlistlinks(newslisturl):
    newsdetails=[]
    res=requests.get(newslisturl,headers={'user-agent': 'Mozilla/5.0'})
    jd=json.loads(res.text.replace('try{feedCardJsonpCallback(','').replace(');}catch(e){};',''))
    for ent in jd['result']['data']:
       newsdetails.append(getnewsdetail(ent['url']))
    return newsdetails

newslisturl='https://feed.sina.com.cn/api/roll/get?pageid=121&lid=1356&num=20&versionNumber=1.2.4&page={}&encode=utf-8&callback=feedCardJsonpCallback&_=1584424192307'
#产生分页连接
news_total=[]
for i in range(1,10):
    newsurl=newslisturl.format(i)
    newsary=parserlistlinks(newsurl)
    news_total.extend(newsary)
#print(news_total)



df=pandas.DataFrame(news_total)#pandas整理数据
df.to_sql('sina_chinanews',engine,if_exists='append')#插入数据库s







