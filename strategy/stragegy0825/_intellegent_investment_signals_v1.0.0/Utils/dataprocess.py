# from Utils.MySQLConn import MySQLConn
# import  pandas as pd
#
# command = '''
#     select codetable.SecuCode,t.BeginDate,t.EndDate,t.FinancialYear,t.DividendRatio
#     from HK_MainIndex t left join HK_SecuCodeTable codetable on t.CompanyCode = codetable.InnerCode
#     where (codetable.SecuCategory = "港股" or codetable.SecuCategory = "H股")  and codetable.SecuCode="{company_code}"
#     '''.format(company_code='00008')
#
# dfdata, nlines = MySQLConn.read(command)
# columns = "SecuCode,BeginDate,EndDate,FinancialYear,DividendRatio"
# columns_list = columns.split(",")
# dfdata = pd.DataFrame(data=dfdata, columns=columns_list)
# print(dfdata)
#
#
#
# host = 'rm-wz9s90lao15s6j4v2ro.mysql.rds.aliyuncs.com'
# port: 3306
# user = 'jydb'
# password = 'G2W9iPwpAqF4R#202'
# db_name = 'jydb'
# charset = "utf8"
#
# connection = pymysql.connect(
# host=host,
# user=user,
# password=password,
# charset='utf8',
# db=db_name
# )
#
# cursor = connection.cursor(cursor=pymysql.cursors.DictCursor)
# sql='select CompanyCode,BasicEPS from HK_MainIndex'
#
# cursor.execute(sql)
# newsResultList=cursor.fetchall()
# print(newsResultList)
#
# engine_template = "mysql+pymysql://{usr}:{pwd}@{host}:{port}/{db}?charset={charset}"
# engine_str = engine_template.format(usr="fsi_check", pwd="fsi_check@", host="172.28.249.24", port="13358",
#                                     db="hk_finance", charset="utf8mb4")
#
# hk_mian_index_stmt = text("""select * from HK_MainIndex where CompanyCode='{company_code}' and BeginDate >= '{search_start_time}' and
#                     EndDate <= Date('{search_end_time}') and (
#                     PeriodMark=12 or PeriodMark=3 or PeriodMark=6 or PeriodMark=9) order by EndDate;""".format(
#     company_code=00007, \
#     search_start_time=search_start_time, search_end_time=search_end_time))
#
# hk_mian_index_result = pd.read_sql(hk_mian_index_stmt, engine)
# "