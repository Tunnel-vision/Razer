# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from lxml import etree
from urllib.parse import urljoin
from scrapy.http import Request
from ..items import AmazondetailItem
from razerdateresolution import parse_fullmonth_date_str
import datetime


class AmazondetailSpider(RedisSpider):
    name = 'amazondetail'
    allowed_domains = ['amazon.com']

    # def parse(self, response):
    #     if response.status == 200:
    #         try:
    #             html = etree.HTML(response.body)
    #             items = html.xpath('//div[@id="cm-cr-dp-review-list"]/div[contains(@class, "review")]')
    #             for item in items:
    #                 try:
    #                     ite = AmazondetailItem()
    #                     ite['FromUser'] = item.xpath('./div/div[1]/a/div[2]/span/text()')[0]
    #                     ite['DateofComplaint'] = item.xpath('./div/span[contains(@class, "review-date")]/text()')[0]
    #                     ite['CustomerFeedback'] = ''.join(item.xpath('./div/div[4]/span/text()'))
    #                     ite['Remarks'] = ''
    #                     # ite['ID'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')
    #                     ite['ID'] = ''.join([parse_fullmonth_date_str(ite['DateofComplaint']), ite['FromUser']])
    #                     ite['IssueDescription'] = item.xpath('./div/div[2]/a[2]/text()')[0]
    #                     ite['Source'] = response.url
    #                     ite['DateofAdd'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #                     yield ite
    #                 except:
    #                     continue
    #
    #             next = html.xpath('//div[@id="cm_cr-pagination_bar"]/ul//a[contains(text(), "Next")]/@href')[0]
    #             next_url = urljoin('https://www.amazon.com/', next)
    #             yield Request(url=next_url, callback=self.parse, meta={'NEXT': 'NEXT'}, dont_filter=True)
    #         except:
    #             yield {}
    def parse(self, response):
        if response.status == 200:
            try:
                html = etree.HTML(response.body)
                items = html.xpath('//div[@id="cm_cr-review_list"]/div[contains(@class, "review")]')
                for item in items:
                    try:
                        ite = AmazondetailItem()
                        ite['FromUser'] = \
                        item.xpath('.//div[contains(@id, "customer_review-")]/div[1]/a/div[2]/span/text()')[0]
                        strdate = item.xpath('.//div[contains(@id, "customer_review-")]/span/text()')[0]
                        ite['CustomerFeedback'] = ''.join(item.xpath('./div/div/div[4]/span/text()'))
                        ite['Remarks'] = ''
                        id, ite['DateofComplaint'] = parse_fullmonth_date_str(strdate)
                        ite['ID'] = ''.join([id, ite['FromUser']])
                        ite['IssueDescription'] = \
                        item.xpath('.//div[contains(@id, "customer_review-")]/div[2]/a[2]/text()')[0]
                        ite['Source'] = response.url
                        ite['DateofAdd'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        yield ite
                    except:
                        continue

                next = html.xpath('//div[@id="cm_cr-pagination_bar"]/ul//a[contains(text(), "Next")]/@href')[0]
                next_url = urljoin('https://www.amazon.com/', next)
                yield Request(url=next_url, callback=self.parse, meta={'NEXT': 'NEXT'}, dont_filter=True)
            except:
                yield {}
