# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from lxml import etree
from ..items import FacebookItem
from razerdateresolution import parse_date_week_str
import datetime


class FacebookteamrazerSpider(scrapy.Spider):
    name = 'facebookteamrazer'
    allowed_domains = ['facebook.com']
    url = 'https://www.facebook.com/teamrazer/'
    num = 0

    def start_requests(self):
        while True:
            scrollDistance = 'var h=document.documentElement.scrollTop=%d' % (self.num * 1000)
            self.num += 1
            yield Request(self.url, callback=self.parse, meta={'scrollDistance': scrollDistance},
                          dont_filter=True)

    def parse(self, response):
        try:
            if response.status == 200:
                html = etree.HTML(response.body)
                ufilist = html.xpath('//div[@class="UFIList"]')
                for ufi in ufilist:
                    commenteles = ufi.xpath('./div[contains(@class, "_3b-9")]/div/div[@id]')
                    for commentele in commenteles:
                        try:
                            commitem = FacebookItem()
                            strdate = ''.join(
                                commentele.xpath(
                                    './div/div/div/div[2]/div/div/div/div[2]/span[4]/a/abbr/@title')).strip()
                            id, commitem['DateofComplaint'] = parse_date_week_str(strdate)
                            commitem['FromUser'] = ''.join(commentele.xpath(
                                './div/div/div/div[2]/div/div/div/div[1]/div[1]/div/span/div/span[1]/a/text()')).strip()
                            commitem['CustomerFeedback'] = ''.join(commentele.xpath(
                                './div/div/div/div[2]/div/div/div/div[1]/div[1]/div/span/div/span[2]/span/span/span/span/text()')).strip()
                            commitem['Remarks'] = ''
                            commitem['Source'] = self.url
                            commitem['ID'] = ''.join([id, commitem['FromUser']])
                            commitem['DateofAdd'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            yield commitem
                        except:
                            continue
        except:
            yield {}