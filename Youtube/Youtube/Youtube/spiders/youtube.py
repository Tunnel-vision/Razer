# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import YoutubeItem
from scrapy.exceptions import DropItem
from lxml import etree
from urllib.parse import urljoin


class YoutubeSpider(scrapy.Spider):
    name = 'youtube'
    allowed_domains = ['youtube.com']
    url = 'https://youtube.com/'

    def start_requests(self):
        for keyword in self.crawler.settings.get('KEYWORDS'):
            yield Request(url=self.url, meta={'keyword': keyword}, callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            if response.status == 200:
                html = etree.HTML(response.body)
                items = html.xpath('//ytd-video-renderer[contains(@class, "ytd-item-section-renderer")]')
                for item in items:
                    youtubeitem = YoutubeItem()
                    youtubeitem['url'] = urljoin(self.url, item.xpath('.//a[@id="thumbnail"]/@href')[0])
                    yield youtubeitem

        except:
            yield DropItem()
