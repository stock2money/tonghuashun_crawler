# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TonghuashunItem(scrapy.Item):
    # 昨收
    last_close = scrapy.Field()
    # 今开
    today_open = scrapy.Field()
    # 最新价
    last_price = scrapy.Field()
    # 变动
    change = scrapy.Field()
    # 变动比例 %
    change_rate = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    # 日期
    date = scrapy.Field()
    # 股票名称
    name = scrapy.Field()
    # 策略名称
    strategy = scrapy.Field()

class Strategy(scrapy.Item):
    # 策略名称
    strategy = scrapy.Field()
    # 综合成功率
    successRate = scrapy.Field()
    # 操作类型
    operation = scrapy.Field()
    # 核心用法
    usage = scrapy.Field()

class AllItem(scrapy.Item):
    items = scrapy.Field()
    strategys = scrapy.Field()
