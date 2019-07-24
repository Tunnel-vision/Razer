# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from lxml import etree
from ..items import ThevergeItem
from urllib.parse import urljoin
from razerdateresolution import parse_est_date_str
import datetime


class ThevergeSpider(scrapy.Spider):
    name = 'theverge'
    allowed_domains = ['theverge.com']
    url = 'https://www.theverge.com/'

    def start_requests(self):
        keywords = self.crawler.settings.get('KEYWORDS')
        for keyword in keywords:
            yield Request(url=self.url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        try:
            if response.status == 200:
                html = etree.HTML(response.body)
                items = html.xpath('//div[@id="activity"]/div')
                for item in items:
                    try:
                        ite = ThevergeItem()
                        ite['FromUser'] = item.xpath('./div/div[2]/a[1]/text()')[0]
                        strdate = item.xpath('./div/div[2]/a[2]/text()')[0]
                        id, ite['DateofComplaint'] = parse_est_date_str(strdate)
                        ite['ID'] = ''.join([id, ite['FromUser']])
                        comm_items = item.xpath('./div/div[1]/p/text()')
                        ite['CustomerFeedback'] = ''.join(comm_items)
                        ite['Remarks'] = ''
                        ite['Source'] = response.url
                        ite['DateofAdd'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        yield ite
                    except:
                        continue

                nextpage = html.xpath('//div[@class="c-pagination__wrap"]/a[contains(text(), "Next")]/@href')[0]
                next_url = urljoin(self.url, nextpage)
                yield Request(url=next_url, callback=self.parse)
        except:
            yield {}
