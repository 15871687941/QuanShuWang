# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuanshuwangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    bookUrl = scrapy.Field()
    author = scrapy.Field()
    introduction = scrapy.Field()
    status = scrapy.Field()
    chapter_info = scrapy.Field()

