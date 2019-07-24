# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from lxml import etree
from ..items import InstagramItem
from urllib.parse import urljoin
from scrapy.exceptions import DropItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    url = 'https://www.instagram.com/razer/'
    num = 1  # 乘数因子（用来叠加滚动距离）

    def start_requests(self):
        while True:
            scrollDistance = 'var h=document.documentElement.scrollTop=%d' % (self.num * 1000)
            self.num += 1
            yield Request(self.url, callback=self.parse, meta={'scrollDistance': scrollDistance},
                          dont_filter=True)

    def parse(self, response):
        try:
            if response.status == 200:
                html = etree.HTML(response.body)
                items = html.xpath('//article[@class="FyNDV"]//div[contains(@class, "Nnq7C")]')
                for item in items:
                    ites = item.xpath('.//div[contains(@class, "v1Nh3")]/a')
                    for ite in ites:
                        iui = InstagramItem()
                        iui['url'] = urljoin(self.url, ite.xpath('./@href')[0])
                        yield iui
        except:
            yield DropItem()
