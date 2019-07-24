# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from lxml import etree
from urllib.parse import urljoin
import time
from ..items import YoutuberazerItem
from scrapy.exceptions import DropItem


class YoutuberazerSpider(scrapy.Spider):
    name = 'youtuberazer'
    allowed_domains = ['youtube.com']
    start_url = 'https://www.youtube.com/user/cultofrazer/videos?flow=grid&view=0&sort=dd'
    num = 1  # 乘数因子（用来叠加滚动距离）

    def start_requests(self):
        while True:
            scrollDistance = 'var h=document.documentElement.scrollTop=%d' % (self.num * 800)
            self.num += 1
            time.sleep(1)
            yield Request(self.start_url, callback=self.parse, meta={'scrollDistance': scrollDistance},
                          dont_filter=True)

    def parse(self, response):
        try:
            if response.status == 200:
                html = etree.HTML(response.body)
                items = html.xpath('//*[@id="items"]')
                for item in items:
                    ites = item.xpath('./ytd-grid-video-renderer')
                    for ite in ites:
                        youtubeitem = YoutuberazerItem()
                        youtubeitem['url'] = urljoin(self.start_url, ite.xpath('.//a[@id="thumbnail"]/@href')[0])
                        yield youtubeitem
        except:
            yield DropItem()

    @staticmethod
    def close(spider, reason):
        pass