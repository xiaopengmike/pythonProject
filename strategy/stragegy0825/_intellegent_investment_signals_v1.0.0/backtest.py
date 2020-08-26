from Core.GildataRem import GildataDb
import  pandas as pd
import  pymysql
from Utils.PyTime import PyDating
pd.set_option('display.max_columns',30) #给最大列设置为10列
pd.set_option('display.max_rows',3000)#设置最大可见100行

def get_quater_factordata(target,date):
    Basedata=GildataDb()
    df1=Basedata.read_financeindex_data(target,date)###
    df3=Basedata.read_HK_MainIndex_data(target,'20201220')
    df4=pd.merge(df1,df3,on=['PeriodMark','FinancialYear'])
    return df4

def  get_daily_factordata(target,date):
    Basedata = GildataDb()
    df5=Basedata.read_QT_HKDailyQuoteIndex_data(target,date)
    return df5

#初始化
holdingstockdata=pd.DataFrame(columns=['开仓日期','开仓标的','开仓价格','平仓日期','平仓价格'])
aus=0

#获取交易日期
traderdays=pd.read_csv('hsindex.csv')

for j in range(61,len(traderdays)-1):
    date = traderdays.iloc[j,0].replace('/','').lstrip(' ') #字符串'2010/01/30'
    date2 = traderdays.iloc[j+1,0].replace('/','').lstrip(' ') #字符串'2010/01/30'
    print(j,date)
    #获取该交易日的候选标的
    constituent_intervel=['20091231','20100630','20101231','20110630','20111231','20120630','20121231','20130630','20131231','20140630','20141231','20150630','20151231','20160630','20161231','20170630','20171231','20180630','20181231','20190630','20191231','20200630','20201231']
    for m in range(1,len(constituent_intervel)):
        if constituent_intervel[m-1]<=date and date<=constituent_intervel[m]:
            alltarget=pd.read_csv(constituent_intervel[m-1]+'.csv',encoding='gb18030').iloc[:,0]

    #提取该交易日所有候选标的的因子值，并排序
    targetdata = pd.DataFrame(columns=['日期','标的','股息率TTM'])

    for i in range(len(alltarget)):
        dfa = get_daily_factordata(alltarget[i][:5], date)
        if dfa.empty:
            continue
        else:
            targetdata.loc[i, '标的'] = alltarget[i][:5]
            targetdata.loc[i, '日期'] = date
            targetdata.loc[i, '股息率TTM'] =dfa['DividendRatioRW'].tolist()[-1]
    #选出标的并建仓
    targetdata=targetdata[targetdata['股息率TTM']>5].sort_values(by='股息率TTM').tail(10)

    for k in range(len(targetdata)):
        stock=targetdata['标的'].tolist()[k]
        Basedata = GildataDb()
        adsf=Basedata.read_QT_HKBefRehDQuote_data(stock,date)
        adsfadf = Basedata.read_QT_HKBefRehDQuote_data(stock, date2)
        holdingstockdata.loc[aus, '开仓日期'] = date
        holdingstockdata.loc[aus, '开仓标的'] = stock
        holdingstockdata.loc[aus, '开仓价格'] = adsf['OpenPrice'].tolist()[-1]
        holdingstockdata.loc[aus, '平仓日期'] = date2
        holdingstockdata.loc[aus, '平仓价格'] = adsfadf['OpenPrice'].tolist()[-1]
        aus+=1
    if j%30==0:
        holdingstockdata.to_csv('guxilvTTM'+str(j)+'.csv')


holdingstockdata.to_csv('guxilvTTM.csv')