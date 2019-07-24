# -*- coding: utf-8 -*-
from lxml import etree
from ..items import TwitterdetailItem
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider
from razerdateresolution import parse_date_id
import datetime


class TwitterdetailSpider(RedisSpider):
    name = 'twitterdetail'
    allowed_domains = ['twitter.com']
    scroll = 'var q=document.getElementById("permalink-overlay").scrollTop=%d'

    def parse(self, response):
        try:
            if response.status == 200:
                html = etree.HTML(response.body)
                # 判断评论数是否大于0
                replyNumNode = html.xpath(
                    '//div[contains(@class, "tweet")]/div[contains(@class, "stream-item-footer")]/div[contains(@class, "ProfileTweet-actionCountList")]/span[1]/span[1]/@data-tweet-stat-count')
                if replyNumNode:
                    replyNum = int(replyNumNode[0])
                    for i in range(1, int(replyNum / 3)):
                        value = i * 800
                        scrollDistance = self.scroll % value
                        yield Request(url=response.url, callback=self.parse_scroll, meta={'scrollDistance': scrollDistance},
                                      dont_filter=True)

                items = html.xpath('//div[@class="stream"]/ol//li/ol//li')
                for item in items:
                    try:
                        ti = TwitterdetailItem()
                        username = item.xpath('./div/div[2]/div[1]/a/span[1]/strong/text()')
                        if not username:
                            continue
                        ti['FromUser'] = username[0]
                        ti['ID'] = item.xpath('./div/div[2]/div[1]/small/a/span/@data-time-ms')[0]
                        replyTime = item.xpath('./div/div[2]/div[1]/small/a/@data-original-title')
                        datefield = ''
                        if replyTime:
                            datefield = replyTime[0]
                        else:
                            datefield = item.xpath('./div/div[2]/div[1]/small/a/@title')[0]
                        ti['DateofComplaint'] = parse_date_id(datefield)

                        content = item.xpath('./div/div[2]/div[3]/p/text()')
                        if content:
                            ti['CustomerFeedback'] = ''.join(content)
                        else:
                            ti['CustomerFeedback'] = ''
                        ti['Remarks'] = ''
                        ti['Source'] = response.url
                        ti['DateofAdd'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        yield ti
                    except:
                        continue
        except:
            yield {}

    def parse_scroll(self, response):
        try:
            if response.status == 200:
                html = etree.HTML(response.body)
                items = html.xpath('//div[@class="stream"]/ol//li/ol//li')
                for item in items:
                    try:
                        ti = TwitterdetailItem()
                        username = item.xpath('./div/div[2]/div[1]/a/span[1]/strong/text()')
                        if not username:
                            continue
                        ti['FromUser'] = username[0]
                        ti['ID'] = item.xpath('./div/div[2]/div[1]/small/a/span/@data-time-ms')[0]
                        replyTime = item.xpath('./div/div[2]/div[1]/small/a/@data-original-title')
                        datefield = ''
                        if replyTime:
                            datefield = replyTime[0]
                        else:
                            datefield = item.xpath('./div/div[2]/div[1]/small/a/@title')[0]
                        ti['DateofComplaint'] = parse_date_id(datefield)

                        content = item.xpath('./div/div[2]/div[3]/p/text()')
                        if content:
                            ti['CustomerFeedback'] = ''.join(content)
                        else:
                            ti['CustomerFeedback'] = ''
                        ti['Remarks'] = ''
                        ti['Source'] = response.url
                        ti['DateofAdd'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        yield ti
                    except:
                        continue
        except:
            yield {}
