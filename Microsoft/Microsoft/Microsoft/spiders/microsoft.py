# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from ..items import MicrosoftItem
from razerdateresolution import parse_split_date_str
import datetime


class MicrosoftSpider(scrapy.Spider):
    name = 'microsoft'
    allowed_domains = ['microsoft.com']
    start_urls = ['https://www.microsoft.com/en-us/store/p/razer-synapse-for-xbox/9p3xv1vq92qc']

    def parse(self, response):
        try:
            if response.status == 200:
                results = str(response.body, 'utf-8').split('--*--*--')
                for result in results:
                    try:
                        html = etree.HTML(result)
                        items = html.xpath('//div[@id="ReviewsList"]//div[@class="review-cards-section"]/div[contains(@class, "review-card")]')
                        for item in items:
                            mi = MicrosoftItem()
                            mi['FromUser'] = item.xpath('./div/div[1]/h3/text()')[0]
                            try:
                                mi['Device'] = item.xpath('./div/div[1]/p/text()')[0]
                            except:
                                mi['Device'] = ''
                            strdate = item.xpath('./div/div[2]/div[2]/span[2]/text()')[0]
                            mi['IssueDescription'] = ''.join(item.xpath('./div/div[2]/h3/text()')).strip()
                            mi['CustomerFeedback'] = ''.join(item.xpath('./div/div[2]/p/text()')).strip()
                            id, mi['DateofComplaint'] = parse_split_date_str(strdate)
                            mi['ID'] = ''.join([id, mi['FromUser']])
                            mi['Remarks'] = ''
                            mi['Source'] = response.url
                            mi['DateofAdd'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            yield mi
                    except:
                        continue
        except:
            yield {}