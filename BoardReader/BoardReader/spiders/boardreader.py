# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from lxml import etree
from ..items import BoardreaderItem
import datetime
from urllib.parse import urljoin
from razerdateresolution import parse_at_date_str


class BoardreaderSpider(scrapy.Spider):
    name = 'boardreader'
    allowed_domains = ['boardreader.com']
    url = 'http://boardreader.com/'

    def start_requests(self):
        for keyword in self.crawler.settings.get('KEYWORDS'):
            yield Request(url=self.url, callback=self.parse, meta={'keyword': keyword}, dont_filter=True)

    def parse(self, response):
        try:
            if response.status == 200:
                results = str(response.body, 'utf-8').split('--*--*--')
                for result in results:
                    try:
                        html = etree.HTML(result)
                        items = html.xpath('//ul[@class="mdl-list"]/li')
                        for item in items:
                            issuedescription = ''.join(item.xpath('.//p[@class="title"]/a/text()'))
                            detail_url = item.xpath('.//p[@class="title"]/a/@href')[0]
                            source = item.xpath('.//p[@class="last-info"]/span[1]/a/text()')[0]
                            forum = ''.join(item.xpath('.//p[@class="last-info"]/span[2]/a/span/text()'))
                            source_url = item.xpath('.//p[@class="last-info"]/span[1]/a/@href')[0]
                            params = {
                                'issuedescription': issuedescription,
                                'url': detail_url,
                                'source': source,
                                'forum': forum,
                                'source_url': source_url
                            }
                            yield Request(url=detail_url, callback=self.parse_item,
                                          meta={'issuedescription': issuedescription,
                                                # 'url': detail_url,
                                                'source': source,
                                                'forum': forum,
                                                'source_url': source_url}, dont_filter=True)
                    except:
                        continue
        except:
            yield {}

    def parse_item(self, response):
        if response.status == 200:
            html = etree.HTML(response.body)
            try:
                items = html.xpath('//ol[@id="messageList"]/li')
                for item in items:
                    try:
                        ite = BoardreaderItem()
                        ite['FromUser'] = item.xpath('./div[1]/div/h3/a/text()')[0]
                        ite['IssueDescription'] = response.headers.get('issuedescription')
                        ite['Source'] = response.headers.get('source')
                        ite['Forum'] = response.headers.get('forum')
                        ite['CustomerFeedback'] = ''.join(
                            item.xpath('./div[2]/div[1]/article/blockquote/text()')).strip()
                        strdate = item.xpath('./div[2]/div[2]/div[1]/span/a/abbr/@title')[0]
                        id, ite['DateofComplaint'] = parse_at_date_str(strdate)
                        ite['ID'] = ''.join([item.xpath('./div[2]/div[2]/div[1]/span/a/abbr/@data-time')[0],
                                             item.xpath('./div[2]/div[2]/div[1]/span/a/abbr/@data-diff')[0]])
                        ite['Remarks'] = ''
                        ite['Source'] = response.url
                        ite['DateofAdd'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        yield ite
                    except:
                        continue

                source_url = response.headers.get('source_url')
                nexts = html.xpath(
                    '//div[@id="content"]//a[contains(text(), "Next")]/@href')
                next_url = urljoin('http://forum.notebookreview.com/', nexts[0])
                yield Request(url=next_url, callback=self.parse_item, meta={'issuedescription': ite['IssueDescription'],
                                                                            # 'url': detail_url,
                                                                            'source': ite['Source'],
                                                                            'forum': ite['Forum'],
                                                                            'source_url': source_url}, dont_filter=True)
            except:
                yield {}
