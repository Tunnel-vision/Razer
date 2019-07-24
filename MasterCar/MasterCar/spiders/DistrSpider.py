# -*- coding: utf-8 -*-
import scrapy
from redis import Redis
from urllib import parse
from scrapy.http import Request
from multiprocessing import Pool
from MasterCar.Common.DBAccess import *
from MasterCar.Common.UrlEntiy import *
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
header = {'User-Agent': user_agent}

# 获得车型
def _getCarType(url):
    urla = url.split("?")
    res = parse.parse_qs(urla[1])
    return res.get('ctype')[0];

# 通过往HyperLogLog数据结构中添加元素值来去重
def _filter_url(redis, url, key="Cars:start_urls"):
    try:
        is_new_url = bool(redis.pfadd(key + "_filter", url))
        if is_new_url:
            redis.lpush(key, url)
    except Exception as e:
        raise e;
# Master
class MasterSpider(scrapy.Spider):
    name = "master";
    r = Redis()
    #r.flushall()
    def start_requests(self):  # 起始URL设置
        try:
            # 爱卡汽车
            for url in urlList1:
                yield Request(url=url, callback=self._aika, headers=header)
            # 太平洋汽车
            for url in urlList4:
                yield Request(url=url, callback=self._tai,headers=header)
            # 网易汽车
            for url in urlList5:
                yield Request(url=url, callback=self._wangyi,headers=header)
            # 盖世汽车网
            for url in urlList2:
                yield Request(url=url, callback=self._Gaishi,headers=header)
            # 新浪网汽车
            for url in urlList6:
                yield Request(url=url, callback=self._Sina,headers=header)
            # 搜狐网汽车
            for url in urlList3:
                yield Request(url=url, callback=self.souhu,headers=header)
            # 易车网汽车
            for url in urlList7:
                yield Request(url=url, callback=self._yiche,headers=header)
        except Exception as e:
            raise e;

    # 获取爱卡汽车的每个页面的url
    def _aika(self, response):
        try:
            count = response.xpath('//div[@class="unify_page mt20"]/a/text()').extract()[6]
            for i in range(1,int(count)):
                yield _filter_url(MasterSpider.r, response.url + '&r=reputation/reputation/GetAjaxKbList3&page=' + str(i))
        except Exception as e:
            raise e;

    # 获取太平洋汽车每个页面的url
    def _tai(self, response):
        try:
            CatType = _getCarType(response.url)
            next_link = response.xpath('//div[@class="main_nav_page"]/a[@class="next"]/@href')[0].extract()
            if next_link:
                yield _filter_url(MasterSpider.r, 'http:' + next_link + '?rnd=tai&ctype=' + CatType);
                yield Request('http:' + next_link+ '?ctype=' + CatType, callback=self._tai,headers=header)
        except Exception as e:
            raise e;

    # 获取网易汽车每个详情页面的URL
    def _wangyi(self, response):
        try:
            CatType = _getCarType(response.url)
            details_urls = response.xpath('//div[@id="main-article-list"]/div/a/@href').extract()
            for details_url in details_urls:
                yield _filter_url(MasterSpider.r, details_url + '?rnd=wangyi&ctype=' + CatType);
            texts = response.xpath('//div[@class="pager"]/table/tr/td/div/a/text()').extract()
            for i in range(len(texts)):  # 翻页功能，需要替换'下一页'
                if texts[i] == '>':
                    index = str(i + 1)
                    next_link = 'http://product.auto.163.com' \
                                + response.xpath('//div[@class="pager"]/table/tr/td/div/a[%s]/@href'%index).extract_first() \
                                +  '&ctype=' + CatType
                    if next_link != '#':
                        yield Request(next_link, callback=self._wangyi,headers=header)
        except Exception as e:
            raise e;

    # 获取Gaishi汽车每个详情页面的URL
    def _Gaishi(self, response):
        try:
            CatType = _getCarType(response.url)
            details_urls = response.xpath('//div[@class="listLeft"]/div[@class="content"]/h2/a/@href').extract()
            for details_url in details_urls:
                yield _filter_url(MasterSpider.r, 'http://auto.gasgoo.com' + details_url + '?rnd=gaisi&ctype=' + CatType);
            texts = response.xpath('//div[@id="ContentPlaceHolder1_pages"]/a/text()').extract()
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            header = {'User-Agent': user_agent}
            for i in range(len(texts) + 1):
                if texts[i] == '>>':
                    index = str(i + 1)
                    next_link = 'http://auto.gasgoo.com' + response.xpath(
                        '//div[@id="ContentPlaceHolder1_pages"]/a[%s]/@href' % index).extract_first() \
                                + '&ctype=' + CatType
                    yield Request(next_link, callback=self._Gaishi,headers=header)
        except Exception as e:
            raise e;

    # 获得新浪网汽车得每个详情页面得URL
    def _Sina(self, response):
        try:
            CatType = _getCarType(response.url)
            details_urls = response.xpath('//div[@class="wpkwp_ck"]/dl/dt/a/@href').extract()
            for details_url in details_urls:
                yield _filter_url(MasterSpider.r, details_url + '?rnd=sina&ctype=' + CatType);
            texts = response.xpath('//div[@class="morepage"]/a/text()').extract()
            for i in range(len(texts)):  # 翻页功能，需要替换'下一页'
                if texts[i] == '下一页':
                    index = str(i + 1)
                    next_link = response.xpath('//div[@class="morepage"]/a[%s]/@href' % index).extract_first() + '?ctype=' + CatType
                    yield Request(next_link, callback=self._Sina,headers=header)
        except Exception as e:
            raise e;

    # 获得搜狐汽车每个详情页的url
    def souhu(self,response):
        try:
            CatType = _getCarType(response.url)
            Urls= response.xpath(
                '//div[@class="koubeico"]/div[@class="koubei-tabcon  cur "]/ul/li/'
                'div[@class="comm-content"]/div[@class="serise-content"]/a[@class="serise-name"]/@href').extract() + response.xpath(
                '//div[@class="koubeico"]/div[@class="koubei-tabcon "]/ul/li/'
                'div[@class="comm-content"]/div[@class="serise-content"]/a[@class="serise-name"]/@href').extract()
            for url in Urls:
                yield _filter_url(MasterSpider.r, 'http://' + url + '?rnd=souhu&ctype=' + CatType);
        except Exception as e:
            raise e;

    # 获得易车网每个详情页得URL
    def _yiche(self, response):
        CatType = _getCarType(response.url)
        details_urls = response.xpath(
            '//html//div[@class="col-xs-9"]//div[@class="kb-list-box"]/div[2]/div[@class="main"]/p/a/@href').extract()
        for details_url in details_urls:
            yield _filter_url(MasterSpider.r, details_url + '?rnd=yiche&ctype=' + CatType);
        next_link = response.xpath('//div[@class="the_pages"]//div/a[@class="next_on"]/@href').extract_first() + '?ctype=' + CatType
        if next_link:
            yield Request(next_link, callback=self._yiche, headers=header)

# 清空数据库
SQLServer.ClearCarsInfo(SQLServer());

_Pool = Pool(4)
for i in range(5):
    _Pool.apply_async(MasterSpider.start_requests(MasterSpider()), args=(MasterSpider()))
_Pool.close()
_Pool.join()








