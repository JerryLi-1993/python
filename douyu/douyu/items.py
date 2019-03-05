# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 分类名称
    classify_name = scrapy.Field()
    # 频道名称
    channel_name = scrapy.Field()
    # 直播间ID
    room_id = scrapy.Field()
    # 直播间url
    room_url = scrapy.Field()
    # 直播间名称
    room_name = scrapy.Field()
    # 直播间主播
    room_user = scrapy.Field()
    # 直播间热度
    room_hot = scrapy.Field()
