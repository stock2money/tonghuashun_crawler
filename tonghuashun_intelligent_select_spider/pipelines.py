# coding=utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class TonghuashunIntelligentSelectSpiderPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host="127.0.0.1",
            db="mydb",
            user="root",
            passwd="password",
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, items, spider):
        item_sql = "INSERT INTO recommend(last_close, today_open, last_price, `change`, change_rate, `code`, `date`, `name`, strategy) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute('truncate table recommend')
        for item in items["items"]:
            try:
                self.cursor.execute(item_sql, (item['last_close'], item['today_open'], item['last_price'], item['change'], item['change_rate'], item['code'], item['date'], item['name'], item['strategy']))
                self.cursor.connection.commit()
            except BaseException as e:
                print(e)
                self.connect.rollback()
        
        strategy_sql = "INSERT INTO strategy(strategy, successRate, operation, `usage`) VALUES(%s,%s,%s,%s)"
        self.cursor.execute('truncate table strategy')
        for strategy in items["strategys"]:
            try:
                self.cursor.execute(strategy_sql, (strategy['strategy'], strategy['successRate'], strategy['operation'], strategy['usage']))
                self.cursor.connection.commit()
            except BaseException as e:
                print(e)
                self.connect.rollback()
        return items
