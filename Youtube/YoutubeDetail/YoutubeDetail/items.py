# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class YoutubedetailItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table = 'youtube'
    ID = Field()
    DateofComplaint = Field()
    IssueDescription = Field()
    CustomerFeedback = Field()
    Device = Field()
    FromUser = Field()
    Source = Field()
    IsIssueRelatedWith1MarProductionUpload = Field()
    Remarks = Field()
    DateofAdd = Field()