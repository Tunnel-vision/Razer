# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.exceptions import DropItem


class KeywordFilterPipeline(object):
    def __init__(self, keywords):
        self.keywords = keywords

    def process_item(self, item, spider):
        for keyword in self.keywords:
            if item['CustomerFeedback'].lower().find(keyword.lower()) != -1:
                return item
        return DropItem()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            keywords=crawler.settings.get('KEYWORDS')
        )


class MysqlPipeline(object):
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()
        sql = 'select max(ID) from twitter'
        self.cursor.execute(sql)
        self.maxid = self.cursor.fetchone()[0]
        if self.maxid is None:
            self.maxid = '0'

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        try:
            if item['ID'] <= self.maxid or isinstance(item, DropItem):
                return DropItem()

            data = dict(item)
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = 'insert ignore into %s (%s) values (%s)' % (item.table, keys, values)
            self.db.ping(reconnect=True)
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()
            return item
        except:
            return DropItem()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT')
        )
