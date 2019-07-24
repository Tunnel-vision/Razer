# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from lxml import etree
from ..items import InsiderItem
import datetime


class InsiderSpider(scrapy.Spider):
    name = 'insider'
    allowed_domains = ['insider.razer.com']
    url = 'http://insider.razer.com/'

    def start_requests(self):
        keywords = self.crawler.settings.get('KEYWORDS')
        for keyword in keywords:
            yield Request(url=self.url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        try:
            if response.status == 200:
                results = str(response.body, 'utf-8').split('--*--*--')
                for result in results:
                    html = etree.HTML(result)
                    items = html.xpath('//ol[@class="searchResultsList"]/li')
                    for item in items:
                        try:
                            ite = InsiderItem()
                            ite['IssueDescription'] = ''.join(item.xpath('./div[2]/div[1]/h3/a/text()')).strip()
                            ite['CustomerFeedback'] = ''.join(item.xpath('./div[2]/blockquote/a/text()')).strip()
                            ite['FromUser'] = item.xpath('./div[2]/div[2]/a[1]/text()')[0]
                            ite['Device'] = item.xpath('./div[2]/div[2]/a[2]/text()')[0]
                            ite['DateofComplaint'] = item.xpath('./div[2]/div[2]/abbr/@title')[0]
                            ite['ID'] = ''.join([item.xpath('./div[2]/div[2]/abbr/@data-time')[0], ite['FromUser']])
                            ite['Remarks'] = ''
                            ite['Source'] = response.url
                            ite['DateofAdd'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            yield ite
                        except:
                            continue
        except:
            yield {}
