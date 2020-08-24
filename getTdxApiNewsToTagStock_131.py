# 获取通达信7*24， 标出股票
import pymysql
import requests
import json
import uuid
from time import gmtime, strftime

tdxMarketCode = '131'


def getTdxStockMarketNews(marketIndex):
    url = 'http://8.129.11.22:7619/TQLEX?Entry=CWServ.mzx_yw'
    postJson = json.dumps({"Params": [marketIndex, "", "1", "999"]})
    tdxResponse = requests.post(url, data=postJson).text
    tdxResponse = json.loads(tdxResponse)
    return tdxResponse


tdxResponseData = getTdxStockMarketNews(tdxMarketCode)

tdxNewsLi = tdxResponseData['ResultSets'][0]['Content']
tdxNewsDictLi = []
tdxNewsDict = {}
for tdxNewsItem in tdxNewsLi:
    tdxNewsDict = {}
    try:
        tdxNewsDict['title'] = tdxNewsItem[0]
        tdxNewsDict['content'] = tdxNewsItem[2]
        tdxNewsDict['publish_time'] = tdxNewsItem[1]
        tdxNewsDictLi.append(tdxNewsDict)
    except:
        continue

# tdxNewsDictLi调接口标出股票

# 循环发请求，插入目标mysql数据库
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


# 循环发form请求
def itemApiResIntoDb(newsResult, tdxMarketCode):
    # 需区分tdxMarketCode
    tittle = newsResult['title']
    content = newsResult['content']
    time = newsResult['publish_time']
    url = "http://localhost:8891/stockTagSearch"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    form_data = {
        "tdxMarketCode": tdxMarketCode,
        "tittle": tittle,
        "content": content,
        "time": time,
    }

    response = requests.post(url, data=form_data, headers=headers).text
    print('response')
    response = json.loads(response)
    res_content = response['content']
    res_tittle = response['tittle']
    res_code = response['code']
    res_time = response['time']
    res_stockName = response['stockName']
    res_market = response['market']
    res_Type = response['tagType']
    created_by = 'kaisa.xp06'
    last_modified_by = 'kaisa.xp06'
    gmt_create = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    gmt_modified = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    id = str(uuid.uuid4()).replace("-", "")[:18]

    print('res_Type')
    print(res_code)
    print(res_Type)
    print('type')
    print('-----------------------')

    if (res_code):
        # if(res_Type):
        sql = "INSERT INTO app_config_shares_news_info (id,content,title,code,time,stockName,market,created_by,last_modified_by,gmt_create,gmt_modified) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') ON duplicate KEY UPDATE title = title " % (
            id, res_content, res_tittle, res_code, res_time, res_stockName, res_market, created_by, last_modified_by,
            gmt_create, gmt_modified)
        cursor02.execute(sql)
        connection02.commit()


for newsResult in tdxNewsDictLi:
    try:
        itemApiResIntoDb(newsResult, tdxMarketCode)
    except:
        continue
