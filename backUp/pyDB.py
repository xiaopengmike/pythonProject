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

cursor02 = connection02.cursor(cursor=pymysql.cursors.DictCursor)

sql02='SELECT * FROM `app_config_stock_news` LIMIT 2'
cursor02.execute(sql02)
newsResultList02=cursor02.fetchall()
print(newsResultList02)
id = newsResultList02[0]['id']
print(id)

# cursor03 = connection02.cursor()
# cursor03.execute("insert into app_config_stock_news code(%s) %code")
# sql = "INSERT INTO `app_config_stock_news`(`id`) VALUES ('3')"
code = 'test05'
sql = "INSERT INTO a_test02 (code) VALUES ('%s')" %(code)

cursor02.execute(sql)
connection02.commit()


# sql = 'INSERT INTO {table}({keys}) VALUES ({values})'
# insertSql = "
# INSERT INTO table_name ( code )
#                        VALUES
#                        ( %code );"

