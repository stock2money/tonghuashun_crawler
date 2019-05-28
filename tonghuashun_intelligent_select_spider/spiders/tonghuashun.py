# -*- coding: utf-8 -*-
import scrapy
import time
import datetime
import chardet
import re
import json
import pandas as pd
from tonghuashun_intelligent_select_spider.items import TonghuashunItem, AllItem, Strategy

class TonghuashunSpider(scrapy.Spider):

    strategys = {
        "461357": "W&R短线超跌",
        "461358": "DMI短线超跌",
        "461359": "BIAS短线超跌",
        "461498": "尖三兵",
        "461500": "多方炮",
        "461506": "超级短线波段",
        "526841": "倒锤线",
        "526842": "曙光初现1",
        "526846": "红三兵",
        "526854": "涨停回马枪",
        "dtpl": "均线多头",
        "cxg": "创新高",
        "lxsz": "连续上涨"
    }

    operation = {
        "461357": "短线超跌",
        "461358": "中短线超跌",
        "461359": "",
        "461498": "中线或短线追涨",
        "461500": "",
        "461506": "短线强势",
        "526841": "",
        "526842": "中长线超跌",
        "526846": "中线或短线追涨",
        "526854": "",
        "dtpl": "中线趋势追涨",
        "cxg": "短线或中线追涨",
        "lxsz": "短线或中线追涨"
    }
    
    usage = {
        "461357": u'参数为6和10的两条威廉指标线的均值上穿90，且CCI指标开始上翘。',
        "461358": u'DI2线在50以上形成拐头向下的买入机会。',
        "461359": u'',
        "461498": u'股价上涨阶段连续3天形成长阳组合K线，其中必有一天为涨停板，今收盘价高于昨最高价，为中线或短线买入机会，并结合个股均线走势和前期高位压力分析。',
        "461500": u'',
        "461506": u'前一日出现中阳线，后2日缩量，且底部抬高的买入参考。均线多头且为小K线为佳。',
        "526841": u'',
        "526842": u'股价连续下跌，昨日出现中阴线，低开出现中阳线的买入机会。有前期支撑位为佳。',
        "526846": u'一般出现在阶段底部，连续3根小阳线，个股涨幅过高，请慎重。',
        "526854": u'',
        "dtpl": u'多头排列是指短期均线上穿中期均线，中期均线上穿长期均线，整个均线系统形成向上发散态势，显示多头的气势。',
        "cxg": u'创新高为股票创出一段时期最高价格，股票之所以能够创新高，说明股票看多力量强大。',
        "lxsz": u'选出连续上涨的个股 ，并根据涨幅进行排序。'
    }

    name = 'tonghuashun'
    allowed_domains = ['10jqka.com']
    start_urls = []
    base_url = "http://comment.10jqka.com.cn/znxg/formula_stocks_pc.json?_=%d"
    stocks = {}
               
    def __init__(self):
        timestamp = int(time.mktime(datetime.datetime.now().timetuple())) * 1000
        url = self.base_url % timestamp
        self.start_urls.append(url)

        info = pd.read_csv("data/stocks.csv", header=0, delimiter=",")
        for i in range(len(info["display_name"])):
            self.stocks[info["display_name"][i]] = info["code"][i]


    def parse(self, response):
        data = response.text
        data = data[data.index('{'): self.find_last(data, '}') + 1]
        jsobj = json.loads(data)
        
        obj = AllItem()
        obj["items"] = []
        obj["strategys"] = []

        for strategy in jsobj:
            if strategy in self.strategys.keys():
                s = Strategy()
                s["strategy"] = self.strategys[strategy]
                s["successRate"] = jsobj[strategy]["successRate"]
                s["operation"] = self.operation[strategy]
                s["usage"] = self.usage[strategy]
                obj["strategys"].append(s)
                for item in jsobj[strategy]["list"]:
                    if item["name"] in self.stocks.keys():
                        stock = TonghuashunItem()
                        stock["last_close"] = item["6"]
                        stock["today_open"] = item["7"]
                        stock["last_price"] = item["10"]
                        stock["change"] = item["264648"]
                        stock["change_rate"] = item["199112"]
                        stock["name"] = item["name"]
                        stock["code"] = self.stocks[stock["name"]]
                        stock["date"] = item["date"]
                        stock["strategy"] = self.strategys[strategy]
                        obj["items"].append(stock)
        return obj

    def find_last(self, string, str):
        last_position = -1
        while True:
            position = string.find(str, last_position+1)
            if position == -1:
                return last_position
            last_position = position
        return last_position
        
