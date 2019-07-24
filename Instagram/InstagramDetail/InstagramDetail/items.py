# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class InstagramItem(Item):
    table = 'instagram'
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
