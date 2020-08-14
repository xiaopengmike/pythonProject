import pymysql
import requests
import json

#数据库拿出数据
host = 'rm-wz9s90lao15s6j4v2ro.mysql.rds.aliyuncs.com'
port: 3306
user = 'jydb'
password = 'G2W9iPwpAqF4R#202'
db_name = 'jydb'
charset = "utf8"

connection = pymysql.connect(
host=host,
user=user,
password=password,
charset='utf8',
db=db_name
)

cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
# effect_row = cursor.execute('SELECT * FROM `lc_news` LIMIT 100')
sql='SELECT * FROM `lc_news` LIMIT 10'
cursor.execute(sql)
newsResultList=cursor.fetchall()
print(newsResultList)

#插入目标数据库
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
# sql02='SELECT * FROM `app_config_stock_news` LIMIT 2'
# cursor02.execute(sql02)
# newsResultList02=cursor02.fetchall()
# print(newsResultList02)
# id = newsResultList02[0]['id']
# print(id)

# cursor03 = connection02.cursor()
# cursor03.execute("insert into app_config_stock_news code(%s) %code")
# sql = "INSERT INTO `app_config_stock_news`(`id`) VALUES ('3')"

#循环发form请求
def itemApiResIntoDb(newsResult):
    tittle = newsResult['InfoTitle']
    content = newsResult['Content']
    time = newsResult['InfoPublDate']

    url = "http://localhost:8891/stockSearch"
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
    print(response)
    response = json.loads(response)

    res_content=response['content']
    res_tittle=response['tittle']
    res_code=response['code']
    res_time=response['time']
    res_stockName=response['stockName']
    res_market=response['market']


    # code = 'test12'
    sql = "INSERT INTO app_config_stock_news_info (content,tittle,code,time,stockName,market) VALUES ('%s','%s','%s','%s','%s','%s')" % (res_content,res_tittle,res_code,res_time,res_stockName,res_market)

    cursor02.execute(sql)
    connection02.commit()

    # res_content=response['content']
    # res_tittle=response['tittle']
    # res_time=response['time']
    # res_stockName=response['stockName']
    # res_market=response['market']
    # res_code=response['code']
    #
    # code = 'test10'
    # tittle = 'test10'
    # # sql = "INSERT INTO app_config_stock_news_info (content,tittle,time,stockName,market,code) VALUES ('%s','%s','%s','%s','%s','%s')" % (res_content,res_tittle,res_time,res_stockName,res_market,res_code)

    # response[‘time’]

for newsResult in newsResultList:
    itemApiResIntoDb(newsResult)


#test插入数据库


# id = '10'




