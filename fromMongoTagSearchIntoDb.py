# coding:utf-8

import pymongo
import pymysql
import requests
import json

#从mongo获取  爬取的新闻数据
myclient = pymongo.MongoClient("mongodb://47.106.75.82:27017/")
dblist = myclient.list_database_names()
mydb = myclient["fin_news"]
collist = mydb. list_collection_names()
mycol = mydb["warn_news"]
# 按新闻tag关键词，来使用
# newsResultList = mycol.find()
newsResultList = mycol.find({'tag':'高管变动'})
# ['经营业绩', '财务预警', '诉讼纠纷', '违法违规', '兼并收购', '高管变动', '金融监管处罚', '环保处罚', '失信被执行人',
#               '中介机构', '私募基金', '生产事故', '产品信息', '新股发行', '商业贸易','资产重组', '股价波动', '投融资', '生产停产', '债务逾期']
print(newsResultList[0])

#循环发请求，插入目标mysql数据库
host02 = '47.107.33.27'
port02: 3306
user02 = 'root'
password02 = 'kaisa!'
db_name02 = 'kgl_user_center'
charset02 = "utf8"

connection02 = pymysql.connect(
host=host02,
user=user02,
password=password02,
charset='utf8',
db=db_name02
)
cursor02 = connection02.cursor(cursor=pymysql.cursors.DictCursor)

#循环发form请求
def itemApiResIntoDb(newsResult):
    tittle = newsResult['title']
    content = newsResult['content']
    time = newsResult['publish_time']
    url = "http://localhost:8891/stockTagSearch"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    form_data = {
        "tittle": tittle,
        "content": content,
        "time": time,
    }

    response = requests.post(url, data=form_data, headers=headers).text
    print('response')
    response = json.loads(response)

    res_content=response['content']
    res_tittle=response['tittle']
    res_code=response['code']
    res_time=response['time']
    res_stockName=response['stockName']
    res_market=response['market']
    res_Type=response['tagType']
    res_stockLi=str(response['contentStockCountDictLi'])
    res_tagLi=str(response['contentTagCountDictLi'])

    print('res_Type')
    print(res_code)
    print(res_Type)
    print(res_stockLi)
    print('type')
    print(type(res_stockLi))
    print(res_tagLi)
    print('-----------------------')

    if(res_code):
        if(res_Type):
            sql = "INSERT INTO app_config_shares_news_event_tag (content,title,code,time,stockName,market,tagType) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (res_content,res_tittle,res_code,res_time,res_stockName,res_market,res_Type)
            cursor02.execute(sql)
            connection02.commit()

for newsResult in newsResultList:
    try:itemApiResIntoDb(newsResult)
    except:continue
