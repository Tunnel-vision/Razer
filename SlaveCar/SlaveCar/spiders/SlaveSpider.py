# -*- coding: utf-8 -*-
import re
import scrapy
from redis import Redis
from urllib import parse
from scrapy.http import Request
from SlaveCar.Common import Analysis
from scrapy.selector import Selector
from SlaveCar.Common import EnumUrlType
from SlaveCar.items import SlavecarItem
from scrapy_redis.spiders import RedisSpider
identity='slave'
# slave

def _getUrlType(url):
    urla = url.split("?")
    res = parse.parse_qs(urla[1])
    return res.get('rnd')[0];

class CarsSpider(RedisSpider):
    # 爬虫名
    name = 'slave'
    # slave从redis队列中爬取的url的key
    redis_key = 'Cars:start_urls'

    # request请求的回掉函数
    # response作为request请求的返回值
    def parse(self, response):
        try:
            print("*************************************爬虫开始*************************************");
            urlType = _getUrlType(response.url);
            yield from Analysis.CommonFun(response,urlType);
        except Exception as e:
             print(e);





