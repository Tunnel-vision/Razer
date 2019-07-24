# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from scrapy.http import Request
from ..items import NotebookreviewItem
from razerdateresolution import parse_at_date_str
import datetime


class NotebookreviewSpider(scrapy.Spider):
    name = 'notebookreview'
    allowed_domains = ['notebookreview.com']
    url = 'http://forum.notebookreview.com/razer/'

    def start_requests(self):
        for keyword in self.crawler.settings.get('KEYWORDS'):
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
                            ite = NotebookreviewItem()
                            ite['IssueDescription'] = item.xpath('./div[2]/div[1]/h3/a/text()')[0]
                            ite['CustomerFeedback'] = ''.join(item.xpath('./div[2]/blockquote/a/text()')).strip()
                            ite['FromUser'] = ''.join(item.xpath('./div[2]/div[2]/a[1]/text()')).strip()
                            ite['Device'] = ''.join(item.xpath('./div[2]/div[2]/a[2]/text()')).strip()
                            strdate = ''.join(item.xpath('./div[2]/div[2]/span/@title')).strip()
                            id, ite['DateofComplaint'] = parse_at_date_str(strdate)
                            ite['ID'] = ''.join([id, ite['FromUser']])
                            ite['Remarks'] = ''
                            ite['Source'] = response.url
                            ite['DateofAdd'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            yield ite
                        except:
                            continue
        except:
            yield {}
