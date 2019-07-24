# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
from monitordatabase import MonitorRedis


class YoutubeRazerPipeline(object):
    def __init__(self, redis_url, temp_redis_url):
        self.redis_url = redis_url
        self.temp_redis_url = temp_redis_url

    def process_item(self, item, spider):
        url = item.get('url')
        ret = self.setr.sadd(item.collection, url)
        if ret:
            self.lr.rpush(item.collection, url)
        return item

    def open_spider(self, spider):
        self.setr = redis.from_url(self.temp_redis_url)
        self.lr = redis.from_url(self.redis_url)
        self.msc = MonitorRedis(self.setr, spider, 'youtuberazerdetail:start_urls')
        self.msc.start()

    def close_spider(self, spider):
        self.setr.delete('youtuberazerdetail:start_urls')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis_url=crawler.settings.get('REDIS_URL'),
            temp_redis_url=crawler.settings.get('TEMP_REDIS_URL')
        )
