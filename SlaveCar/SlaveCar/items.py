# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SlavecarItem(scrapy.Item):
    Url = scrapy.Field()
    Post_Time = scrapy.Field()
    Car_Type = scrapy.Field()
    Car_Type_Title = scrapy.Field()
    youdian = scrapy.Field()
    quedian = scrapy.Field()
    waiguan = scrapy.Field()
    neishi = scrapy.Field()
    kongjian = scrapy.Field()
    peizhi = scrapy.Field()
    dongli = scrapy.Field()
    chaokong = scrapy.Field()
    youhao = scrapy.Field()
    shushi = scrapy.Field()
    comments = scrapy.Field()
    SenW = scrapy.Field()
    SenN = scrapy.Field()
    SenK = scrapy.Field()
    SenP = scrapy.Field()
    SenD = scrapy.Field()
    SenC = scrapy.Field()
    SenY = scrapy.Field()
    SenS = scrapy.Field()



