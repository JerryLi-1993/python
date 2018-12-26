# -*- coding: utf-8 -*-
import scrapy
from get_news.items import GetWeiboTopic

class GetWeiboTopicSpider(scrapy.Spider):
    name = 'get_weibo_topic'
    allowed_domains = ['s.weibo.com']
    start_urls = ['https://s.weibo.com/top/summary?cate=topicband']

    def parse(self, response):
        item = GetWeiboTopic()
        topic_list = response.xpath("//section[@class='list']//li")
        for each in topic_list:
            item['url'] = "https://s.weibo.com" + each.xpath("./a/@href").extract_first()
            item['hot_sort'] = each.xpath("./a/div/em/text()").extract_first()
            item['topic'] = each.xpath("./a/article/h2/text()").extract_first()
            item['amount'] = each.xpath("./a/article/span/text()").extract_first()
            yield item
