# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import datetime
from ..items import InstagramItem
from lxml import etree
from razerdateresolution import parse_date_tz


class InstagramdetailSpider(RedisSpider):
    name = 'instagramdetail'
    allowed_domains = ['instagram.com']

    def parse(self, response):
        try:
            html = etree.HTML(response.body)
            items = html.xpath('//div[contains(@class, "KlCQn")]/ul//li')
            dateofcmplaint = html.xpath('//div[contains(@class, "k_Q0X")]//time/@datetime')[0]
            for item in items:
                try:
                    ii = InstagramItem()
                    ii['FromUser'] = item.xpath('.//a[contains(@class, "FPmhX")]/text()')[0]
                    ii['CustomerFeedback'] = ''.join(item.xpath('.//div[@class="C4VMK"]/span/text()'))
                    ii['Source'] = response.url
                    ii['Remarks'] = ''
                    id, ii['DateofComplaint'] = parse_date_tz(dateofcmplaint)
                    ii['ID'] = ''.join([id, ii['FromUser']])
                    ii['Source'] = response.url
                    ii['DateofAdd'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    yield ii
                except:
                    continue
        except:
            yield {}