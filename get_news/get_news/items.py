# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GetNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    hot_sort = scrapy.Field()
    title = scrapy.Field()
    amount = scrapy.Field()
    url = scrapy.Field()


class GetWeiboTopic(scrapy.Item):
    hot_sort = scrapy.Field()
    topic = scrapy.Field()
    amount = scrapy.Field()
    url = scrapy.Field()
