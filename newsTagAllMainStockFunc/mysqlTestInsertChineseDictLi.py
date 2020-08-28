# 获取通达信7*24， 标出股票
import pymysql
import requests
import json
import uuid
from time import gmtime, strftime
import config

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
all_stock_dict_li = [
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
]

# all_stock_dict_li='中文编码测试'

all_stock_dict_li=json.dumps(all_stock_dict_li,ensure_ascii=False)




sql = "INSERT INTO app_config_shares_news_info_get_all_shares (all_stock_dict_li) VALUES ('%s')" % (
 all_stock_dict_li)

cursor02.execute(sql)
connection02.commit()