#coding=utf-8
import flask, json
# from gevent import pywsgi
from flask import request
# '''
# flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
# 创建一个服务，把当前这个python文件当做一个服务
server = flask.Flask(__name__)
@server.route('/stockSearch', methods=['post'])
def stockSearch():
    content = request.form.get('content')
    contentDict = {'content':content}
    print(contentDict)
    # 获取到post的数据，统计股票出现次数
    # stockSearchWordLi = ['ChiNameAbbr', '平安银行','畅联股份', '万科', '金田实业']

    stockSearchWordLi = [
        {
            "market": "1",
            "name": "福纺控股",
            "SecuCode": "08506"
        },
        {
            "market": "1",
            "name": "海通恒信",
            "SecuCode": "01905"
        }
    ]

    def strStockCount(strDict):
        str = strDict['content']
        # 循环插入搜索股票关键词，如果有count，就放到dict里
        contentStockCountDict = {}
        for stockSearchWord in stockSearchWordLi:
            print(stockSearchWord['name'])
            if (str.count(stockSearchWord['name'])):
                contentStockCountDict[stockSearchWord['name']] = str.count(stockSearchWord['name'])
                # contentStockCountDict[stockSearchWord] = 'TRUE  '
        # sub='苏宁'
        print(contentStockCountDict)
        stockCountList = sorted(contentStockCountDict.keys())
        if(len(stockCountList)):
            strDict['stock'] = stockCountList[0]
        else:strDict['stock'] = ""
        strDict['contentStockCountDict'] = contentStockCountDict
        return strDict

    response = strStockCount(contentDict)
    return json.dumps(response,ensure_ascii=False)


if __name__ == '__main__':
    server.run(port=8891, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问