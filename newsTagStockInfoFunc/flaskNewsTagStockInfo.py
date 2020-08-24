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
    tdxMarketCode = request.form.get('tdxMarketCode')
    print('tdxMarketCode' + ':' + tdxMarketCode)

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
    # HK、HS、US股票数据分开，或合并
    if (tdxMarketCode == '131'):
        stockSearchWordLi = dataSource.hsStockSearchWordLi
    if (tdxMarketCode == '132'):
        stockSearchWordLi = dataSource.hkStockSearchWordLi

    tagSearchWordLi = dataSource.tagSearchWordLi

    def strStockTagCount(responseDict):
        # 先分析标题，有必要再分析正文
        titleStr = responseDict['tittle']
        contentStr = responseDict['content']
        # 循环插入搜索关键词，如果有count，就放到dict里
        contentStockCountDictLi = []
        contentStockCountDict = {}
        for stockSearchWordDic in stockSearchWordLi:
            if titleStr.count(stockSearchWordDic['name']):
                print(stockSearchWordDic)
                contentStockCountDict = stockSearchWordDic
                contentStockCountDict['count'] = titleStr.count(stockSearchWordDic['name'])
                contentStockCountDictLi.append(contentStockCountDict)
        # title循环结束后排序
        contentStockCountDictLi.sort(key=lambda k: (k.get('count', 0)), reverse=True)
        print(contentStockCountDictLi)
        # 判断标题中是否有 和count最大相等的第二个，如果有去内容中判断
        if len(contentStockCountDictLi) > 1:
            if (contentStockCountDictLi[0]['count'] == contentStockCountDictLi[1]['count']):
                contentStockCountDictLi = []
                contentStockCountDict = {}
                for stockSearchWordDic in stockSearchWordLi:
                    if contentStr.count(stockSearchWordDic['name']):
                        print(stockSearchWordDic)
                        contentStockCountDict = stockSearchWordDic
                        contentStockCountDict['count'] = contentStr.count(stockSearchWordDic['name'])
                        contentStockCountDictLi.append(contentStockCountDict)

                # content循环结束后排序
                contentStockCountDictLi.sort(key=lambda k: (k.get('count', 0)), reverse=True)
                print(contentStockCountDictLi)

        if len(contentStockCountDictLi):
            responseDict['stockName'] = contentStockCountDictLi[0]['name']
            responseDict['market'] = contentStockCountDictLi[0]['market']
            responseDict['code'] = contentStockCountDictLi[0]['SecuCode']
        else:
            responseDict['stockName'] = ""
            responseDict['market'] = ""
            responseDict['code'] = ""

        if len(contentStockCountDictLi):
            responseDict['contentStockCountDictLi'] = contentStockCountDictLi

        # TagCount
        contentTagCountDictLi = []
        contentTagCountDict = {}
        for tagSearchWordDic in tagSearchWordLi:
            if titleStr.count(tagSearchWordDic['eventName']):
                print(tagSearchWordDic)
                contentTagCountDict = tagSearchWordDic
                contentTagCountDict['count'] = titleStr.count(tagSearchWordDic['eventName'])
                contentTagCountDictLi.append(contentTagCountDict)

        # title循环结束后排序
        contentTagCountDictLi.sort(key=lambda k: (k.get('count', 0)), reverse=True)
        print(contentTagCountDictLi)
        # 判断标题中是否有和count最大相等的第二个，如果有去内容中判断
        if len(contentTagCountDictLi) > 1:
            if (contentTagCountDictLi[0]['count'] == contentTagCountDictLi[1]['count']):
                contentTagCountDictLi = []
                contentTagCountDict = {}
                for tagSearchWordDic in tagSearchWordLi:
                    if contentStr.count(tagSearchWordDic['eventName']):
                        print(tagSearchWordDic)
                        contentTagCountDict = tagSearchWordDic
                        contentTagCountDict['count'] = contentStr.count(tagSearchWordDic['eventName'])
                        contentTagCountDictLi.append(contentTagCountDict)

                # content循环结束后排序
                contentTagCountDictLi.sort(key=lambda k: (k.get('count', 0)), reverse=True)
                print('contentTagCountDictLi')
                print(contentTagCountDictLi)

        responseDict['contentTagCountDictLi'] = contentTagCountDictLi
        if len(contentTagCountDictLi):
            responseDict['contentTagCountDictLi'] = contentTagCountDictLi
        if len(contentTagCountDictLi):
            responseDict['tagType'] = contentTagCountDictLi[0]['type']
        else:
            responseDict['tagType'] = ""
        return responseDict

    response = strStockTagCount(newsContentDict)
    return json.dumps(response, ensure_ascii=False)


if __name__ == '__main__':
    server.run(port=8891, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
