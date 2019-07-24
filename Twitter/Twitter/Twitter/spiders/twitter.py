# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib.parse import urlencode
from lxml import etree
from ..items import TwitterItem
import datetime
from razerdateresolution import parse_date_id


class TwitterSpider(scrapy.Spider):
    name = 'twitter'
    allowed_domains = ['twitter.com']
    base_url = 'https://twitter.com/search?'
    scroll = "var q=document.documentElement.scrollTop=%d"
    bKeywordFlag = False
    page_source = ''

    def start_requests(self):
        keywords = self.settings.get('KEYWORDS')
        for keyword in keywords:
            data = {
                "f": "tweets",
                "q": keyword,
                "src": "typd"
            }
            url = self.base_url + urlencode(data)
            self.bKeywordFlag = False
            num = 0
            while True:
                if self.bKeywordFlag:
                    break
                scrollDistance = self.scroll % (num * 800)
                num += 1
                yield Request(url, callback=self.parse, meta={'scrollDistance': scrollDistance}, dont_filter=True)

    def parse(self, response):
        try:
            if response.status == 200:
                if self.page_source != response.body:
                    self.page_source = response.body
                else:
                    self.bKeywordFlag = True

                html = etree.HTML(response.body)
                items = html.xpath('//div[@class="stream"]/ol/li')
                for item in items:
                    try:
                        ite = TwitterItem()
                        ite['FromUser'] = ''.join(item.xpath('./div/div[2]/div[1]/a/span[1]/strong/text()'))
                        reply_time = item.xpath('./div/div[2]/div[1]/small/a/@data-original-title')
                        datefield = ''
                        if reply_time:
                            datefield = reply_time[0]
                        else:
                            datefield = item.xpath('./div/div[2]/div[1]/small/a/@title')[0]
                        ite['DateofComplaint'] = parse_date_id(datefield)
                        ite['ID'] = ''.join(item.xpath('./div/div[2]/div[1]/small/a/span/@data-time-ms')).strip()
                        ite['CustomerFeedback'] = ''.join(item.xpath('./div/div[2]/div[3]/p/text()')).strip()
                        ite['Remarks'] = ''
                        ite['Source'] = response.url
                        ite['DateofAdd'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        yield ite
                    except:
                        continue
        except:
            yield {}
