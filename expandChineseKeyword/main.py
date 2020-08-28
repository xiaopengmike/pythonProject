# 发请求，传关键词，返回解析出同义词list
# coding:utf-8
from lxml import etree
import requests
import pymysql

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


#关键词字典列表
keywordDictLi = [
{
      "eventName": "受贿",
      "tagEvent": "贿赂  ",
      "type": "管理预警"
    },
    {
      "eventName": "贪污 ",
      "tagEvent": "贿赂  ",
      "type": "管理预警"
    },
    {
      "eventName": "行贿 ",
      "tagEvent": "贿赂  ",
      "type": "管理预警"
    },
    {
      "eventName": "贿赂  ",
      "tagEvent": "贿赂  ",
      "type": "管理预警"
    },
]

tagEvent=keywordDictLi[0]['tagEvent']
type=keywordDictLi[0]['type']


# keywordLi = ['欠税款','欠款']

#找关键词，并插入数据库，去重
def keywordGetSimilarWord(keyword):
    url = 'https://kmcha.com/similar/' + keyword
    html = requests.get(url).text

    # print(html)
    dom = etree.HTML(html)
    goalXpathResultLi = dom.xpath('//html/body/div[1]/div[2]/div[2]/p/text()')

    itemLi = []
    for item in goalXpathResultLi:
        itemParseLi = item.strip().split('\xa0\n')
        for itemParse in itemParseLi:
            if itemParse.strip()!='':
                if len(itemParse.strip())<6:
                    itemLi.append(itemParse.strip())
    print(itemLi)
    print('parseDone')
    cursor02 = connection02.cursor(cursor=pymysql.cursors.DictCursor)

    for itemPhrase in itemLi:
        print('短语：' + itemPhrase)
        try:
            sql = "INSERT INTO app_config_shares_com_event_ori_tags_expand (eventName,tagEvent,type) VALUES ('%s','%s','%s')" % (itemPhrase,tagEvent,type)
            cursor02.execute(sql)
            connection02.commit()
        except:continue

for keywordDict in keywordDictLi:
    keywordGetSimilarWord(keywordDict['eventName'])
