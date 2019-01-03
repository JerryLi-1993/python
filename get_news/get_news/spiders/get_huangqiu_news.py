# -*- coding: utf-8 -*-
import scrapy
from get_news.items import GetHuanQiuNew

class GetHuangqiuNewsSpider(scrapy.Spider):
    name = 'get_huangqiu_news'
    allowed_domains = ['www.huanqiu.com']
    start_urls = ['http://www.huanqiu.com']

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=headers)

    def parse(self, response):
        item = GetHuanQiuNew()
        # 抓取首页右边的宣传新闻
        news_list = response.xpath("//div[@class='rightFir']//a")
        for each in news_list:
            item['news_type'] = '宣传'
            item['news'] = each.xpath("./text()").extract_first()
            item['url'] = each.xpath("./@href").extract_first()
            yield item
        # 抓取要闻
        news_list = response.xpath("//div[@class='secNewsBlock']//a")
        for each in news_list:
            item['news_type'] = '要闻'
            item['news'] = each.xpath("./text()").extract_first()
            item['url'] = each.xpath("./@href").extract_first()
            yield item
        # 抓取各类新闻
        news_list = response.xpath("//div[@class='conThr clear']")
        for each in news_list:
            item['news_type'] = each.xpath(".//div[@class='indexBTitle']/strong/text()").extract_first()
            for news in each.xpath(".//div[@class='centerThr']//a"):
                item['news'] = news.xpath("./text()").extract_first()
                item['url'] = news.xpath("./@href").extract_first()
                yield item
