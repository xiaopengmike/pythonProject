import pymysql

# 连接数据库
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
sql='SELECT * FROM `lc_news` LIMIT 3'
cursor.execute(sql)
resultList=cursor.fetchall()
print(resultList)
#test插入数据库

#进行匹配