# api输入文章content，
# 返回content，market，code

# coding=utf-8

import flask
import json
from flask import request
import dataSource

# flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
server = flask.Flask(__name__)


@server.route('/stockTagSearch', methods=['post'])
def stockTagSearch():
    # 获取到post的数据
    content = request.form.get('content')
    tittle = request.form.get('tittle')
    time = request.form.get('time')
    newsContentDict = {
        'content': content,
        'tittle': tittle,
        'time': time,
    }
    print(newsContentDict)

    # 统计股票 公司预警事件出现次数
    stockSearchWordLi = dataSource.stockSearchWordLi
    tagSearchWordLi = dataSource.tagSearchWordLi

    def strStockTagCount(strDict):
        titleStr = strDict['tittle']
        # 循环插入搜索关键词，如果有count，就放到dict里
        contentStockCountDictLi = []
        contentStockCountDict = {}
        for stockSearchWordDic in stockSearchWordLi:
            if titleStr.count(stockSearchWordDic['name']):
                print(stockSearchWordDic)
                # contentStockCountDict[stockSearchWordDic['name']] = titleStr.count(stockSearchWordDic['name'])
                contentStockCountDict = stockSearchWordDic
                contentStockCountDict['count'] = titleStr.count(stockSearchWordDic['name'])
                contentStockCountDictLi.append(contentStockCountDict)

        # 循环结束后排序
        contentStockCountDictLi.sort(key=lambda k: (k.get('count', 0)), reverse=True)
        print(contentStockCountDictLi)

        if len(contentStockCountDictLi):
            strDict['stockName'] = contentStockCountDictLi[0]['name']
            strDict['market'] = contentStockCountDictLi[0]['market']
            strDict['code'] = contentStockCountDictLi[0]['SecuCode']
        else:
            strDict['stockName'] = ""
            strDict['market'] = ""
            strDict['code'] = ""

        if len(contentStockCountDictLi):
            strDict['contentStockCountDictLi'] = contentStockCountDictLi

        # TagCount
        contentTagCountDictLi = []
        contentTagCountDict = {}
        for tagSearchWordDic in tagSearchWordLi:
            # print(tagSearchWordDic['name'])
            if titleStr.count(tagSearchWordDic['eventName']):
                print(tagSearchWordDic)
                # contentTagCountDict[tagSearchWordDic['name']] = titleStr.count(tagSearchWordDic['name'])
                contentTagCountDict = tagSearchWordDic
                contentTagCountDict['count'] = titleStr.count(tagSearchWordDic['eventName'])
                contentTagCountDictLi.append(contentTagCountDict)

        # 循环结束后排序
        contentTagCountDictLi.sort(key=lambda k: (k.get('count', 0)), reverse=True)
        print(contentTagCountDictLi)
        strDict['contentTagCountDictLi'] = contentTagCountDictLi
        if len(contentTagCountDictLi):
            strDict['contentTagCountDictLi'] = contentTagCountDictLi

        if len(contentTagCountDictLi):
            strDict['tagType'] = contentTagCountDictLi[0]['type']
        else:
            strDict['tagType'] = ""

        return strDict

    response = strStockTagCount(newsContentDict)
    return json.dumps(response, ensure_ascii=False)


if __name__ == '__main__':
    server.run(port=8891, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
