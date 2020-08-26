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
      "eventName": "欠税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "拖欠税款",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "欠缴税款",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "补缴税款",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "补交税款",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "欠税款",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "追缴税款",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "所欠税款",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "清缴欠税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "欠税金额",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "追缴欠税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "企业欠税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "逃漏税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "逃税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "漏税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "偷税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "逃税漏税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "偷税漏税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "偷漏税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "税务欺诈 ",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "避税 ",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "偷逃税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "逃税避税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "偷逃税款",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "隐瞒收入",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "逃避税收",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "非法避税                       ",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "税务问题",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "涉嫌偷税漏税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "转移资产",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "逃避纳税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "偷税逃税",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "做假账",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },
    {
      "eventName": "税务罚款",
      "tagEvent": "税务问题",
      "type": "信用预警"
    },]

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
