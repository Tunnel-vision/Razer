# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.exceptions import DropItem
from lxml import etree
from ..items import SocialmentionItem


class SocialmentionSpider(scrapy.Spider):
    name = 'socialmention'
    allowed_domains = ['socialmention.com']
    url = 'http://socialmention.com/'

    def start_requests(self):
        for keyword in self.crawler.settings.get('KEYWORDS'):
            yield Request(url=self.url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        try:
            if response.status == 200:
                results = str(response.body, 'utf-8').split('--*--*--')
                for result in results:
                    try:
                        html = etree.HTML(result)
                        items = html.xpath('//div[@id="results"]/div[contains(@class, "result")]')
                        for item in items:
                            ite = SocialmentionItem()
                            ite['url'] = item.xpath('./div[2]/div[2]/p/a[1]/@href')[0]
                            yield ite
                    except:
                        continue
        except:
            yield DropItem()
