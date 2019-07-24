# -*- coding: utf-8 -*-
from lxml import etree
from ..items import YoutuberazerdetailItem
from scrapy_redis.spiders import RedisSpider
from razerdateresolution import parse_date_str
import datetime


class YoutuberazerdetailSpider(RedisSpider):
    name = 'youtuberazerdetail'
    allowed_domains = ['youtube.com']

    def parse(self, response):
        if response.status == 200:
            html = etree.HTML(response.body)
            try:
                items = html.xpath(
                    '//ytd-comments[@id="comments"]/ytd-item-section-renderer[@id="sections"]/div[@id="contents"]')
                for item in items:
                    ites = item.xpath('.//ytd-comment-thread-renderer')
                    for ite in ites:
                        try:
                            youtubeItem = YoutuberazerdetailItem()
                            strdate = ''.join(
                                ite.xpath('.//*[@id="header-author"]/yt-formatted-string/a/text()')).strip()
                            youtubeItem['DateofComplaint'], youtubeItem['ID'] = parse_date_str(strdate)
                            youtubeItem['FromUser'] = ''.join(ite.xpath('.//*[@id="author-text"]/span/text()')).strip()
                            youtubeItem['Source'] = response.url
                            youtubeItem['CustomerFeedback'] = ''.join(
                                ite.xpath('.//*[@id="content-text"]/text()')).strip()
                            youtubeItem['Remarks'] = ''
                            youtubeItem['Source'] = response.url
                            youtubeItem['DateofAdd'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            yield youtubeItem
                        except:
                            continue
            except:
                return {}
