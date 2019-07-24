# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import AmazonItem
from lxml import etree
from urllib.parse import urljoin


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    url = 'https://www.amazon.com/'

    def start_requests(self):
        keywords = self.settings.get('KEYWORDS')
        for keyword in keywords:
            yield Request(url=self.url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        if response.status == 200:
            try:
                html = etree.HTML(response.body)
                items = html.xpath('//ul[@id="s-results-list-atf"]/li[contains(@id, "result")]')
                for item in items:
                    try:
                        ite = AmazonItem()
                        ite['url'] = item.xpath('./div/div/div/div[2]/div[1]/div[1]/a/@href')[0]
                        yield ite
                    except:
                        continue

                next = html.xpath('//a[@id="pagnNextLink"]/@href')[0]
                next_url = urljoin(self.url, next)
                yield Request(url=next_url, callback=self.parse, dont_filter=True)
            except:
                yield {}
    # def parse(self, response):
    #     if response.status == 200:
    #         try:
    #             html = etree.HTML(response.body)
    #             items = html.xpath(
    #                 '//div[@id="search"]/div[@class="sg-row"]//div[contains(@class, "s-result-list")]/div')
    #             for item in items:
    #                 try:
    #                     ite = AmazonItem()
    #                     try:
    #                         ite['url'] = urljoin(self.url, item.xpath(
    #                             './div/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h5/a/@href')[0])
    #                     except:
    #                         ite['url'] = urljoin(self.url, item.xpath(
    #                             './div/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h5/a/@href')[0])
    #                     yield ite
    #                 except:
    #                     print('=====================Parse Error=====================')
    #                     continue
    #
    #             next = html.xpath(
    #                 '//div[@id="search"]/div[1]/div[2]/div/span[7]/div/div/div/ul/li/a[contains(text(), "Next")]/@href')[0]
    #             next_url = urljoin(self.url, next)
    #             yield Request(url=next_url, callback=self.parse, dont_filter=True)
    #         except:
    #             yield {}
