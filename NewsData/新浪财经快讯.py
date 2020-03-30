#插入新浪国内财经新闻
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
import tqdm
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
        result['article'] = ' '.join([p.text.strip() for p in soup.select('.article p')[:-1]])  # 一行文 获取文章内容
        result['updatetime']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) #获取当前时间
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

newslisturl='http://feed.mix.sina.com.cn/api/roll/get?pageid=155&lid=1686&num=10&page={}&callback=feedCardJsonpCallback&_=1584521933053'

#产生分页连接
news_total=[]
for i in range(1,10):
    newsurl=newslisturl.format(i)
    newsary=parserlistlinks(newsurl)
    news_total.extend(newsary)
#print(news_total)

#truncate目标表数据
conn=pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='P@ssword',
    database='test',
    #charset='utf-8'
)
#获取一个光标
cursor=conn.cursor()
#定义执行语句
sql='truncate table sina_chinafinnews;'
#执行语句
cursor.execute(sql)
#提交
conn.commit()
#关闭光标和连接
cursor.close()
conn.close()

df=pandas.DataFrame(news_total)#pandas整理数据
df.to_sql('sina_chinafinnews',engine,if_exists='append')#插入数据库

'''
url='https://news.sina.com.cn/china/'#国内新闻
r=requests.get(url)
r.encoding='utf-8'
soup=BeautifulSoup(r.text,'html.parser')
news_all = soup.find("div", class_="left-content-1").find("div", attrs={"style": "display:none;"}).find_all("a")
news_list=[(i.text,i['href']) for i in news_all]
for n in news_list:
    print(n)
'''


#a_all = soup.find("div", class_="left-content-1").find("div", attrs={"style": "display:none;"}).find_all("a")