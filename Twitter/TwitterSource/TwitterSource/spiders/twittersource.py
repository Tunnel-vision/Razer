# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from lxml import etree
from urllib.parse import urljoin
from ..items import TwitterItem


class TwittersourceSpider(scrapy.Spider):
    name = 'twittersource'
    allowed_domains = ['twitter.com']
    url = 'https://twitter.com/Razer/'
    scroll = "var q=document.documentElement.scrollTop=%d"

    def start_requests(self):
        index = 0
        while True:
            value = index * 1000
            index += 1
            scrollDistance = self.scroll % value
            yield Request(url=self.url, callback=self.parse, meta={'scrollDistance': scrollDistance}, dont_filter=True)

    def parse(self, response):
        if response.status == 200:
            html = etree.HTML(response.body)
            items = html.xpath('//div[@class="stream"]/ol//li')
            for item in items:
                ui = TwitterItem()
                replies = item.xpath('.//a[contains(@class, "tweet-timestamp")]/@href')
                if replies:
                    reply = urljoin('https://twitter.com/Razer/with_replies', replies[0])
                    ui['url'] = reply
                    yield ui
