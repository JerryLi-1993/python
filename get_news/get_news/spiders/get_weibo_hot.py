# -*- coding: utf-8 -*-
import scrapy
from get_news.items import GetNewsItem


class GetWeiboHotSpider(scrapy.Spider):
    name = 'get_weibo_hot'
    allowed_domains = ['s.weibo.com']
    start_urls = ['https://s.weibo.com/top/summary?cate=realtimehot']

    def parse(self, response):
        item = GetNewsItem()
        hot_list = response.xpath("//section/ul[@class='list_a']/li/a")
        for each in hot_list:
            item['hot_sort'] = each.xpath("./strong[@class='hot']/text()").extract_first()
            item['title'] = each.xpath("./span/text()").extract_first()
            item['amount'] = each.xpath("./span/em/text()").extract_first()
            item['url'] = "https://s.weibo.com" + each.xpath("./@href").extract_first()
            yield item
