# -*- coding: utf-8 -*-
import scrapy
import re
import json
from douyu.items import DouyuItem


"""
描述：获取斗鱼各频道下的各个直播间的相关信息，包括
参数：无
修改：jr 2018-02-27
"""
class DouyuSpiderSpider(scrapy.Spider):
    name = 'douyu_spider'
    allowed_domains = ['www.douyu.com']
    # start_urls = ['http://www.douyu.com/']

    def start_requests(self):
        # 斗鱼直播分类（分类名称：url）
        classify_dict = {
            '网游竞技': 'https://www.douyu.com/directory?shortName=PCgame',
            '单机热游': 'https://www.douyu.com/directory?shortName=djry',
            '手游休闲': 'https://www.douyu.com/directory?shortName=syxx',
            '娱乐天地': 'https://www.douyu.com/directory?shortName=yl',
            '科技教育': 'https://www.douyu.com/directory?shortName=kjjy',
            '语音直播': 'https://www.douyu.com/directory?shortName=voice',
            '正能量':   'https://www.douyu.com/directory?shortName=znl'
        }
        for key,value in classify_dict.items():
            yield scrapy.Request(url=value, meta={'classify_name':key}, callback=self.parse)

    def parse(self, response):
        # 频道名称
        channel_list = response.xpath("//ul[@class='layout-Classify-list']/li[@class='layout-Classify-item']/a")
        for each in channel_list:
            # 频道名称
            channel_name = each.xpath(".//strong/text()").extract_first()
            # 频道链接
            channel_url = "https://www.douyu.com%s" % each.xpath("./@href").extract_first()
            meta = {
                # 分类名称
                'classify_name': response.meta['classify_name'],
                # 频道名称
                'channel_name': channel_name
            }
            yield scrapy.Request(url=channel_url, meta=meta, callback=self.get_tag_path)

    # 获取直播间列表
    def get_tag_path(self, response):
        # 获取监本内容
        data = response.xpath("//script[contains(text(),'tabTagPath')]/text()").extract_first()
        # 获取列表数据页数
        page_count = re.search('"pageCount":(.+?),"', data, flags=re.I).group(1)
        # 获取列表数据请求接口地址
        tag_path =  re.search('"tabTagPath":"(.+?)"', data, flags=re.I).group(1)
        for page in range(1, int(page_count)+1):
            # 拼接请求接口链接，接口形式类似于https://www.douyu.com/gapi/rkc/directory/2_1/5
            tag_url = "https://www.douyu.com%s" % tag_path.replace("/c_tag", "").replace("list", str(page))
            meta = {
                # 分类名称
                'classify_name': response.meta['classify_name'],
                # 频道名称
                'channel_name': response.meta['channel_name']
            }
            yield scrapy.Request(url=tag_url, meta=response.meta, callback=self.get_room_list)

    def get_room_list(self, response):
        item = DouyuItem()

        # 获取当前分类的js数据
        json_data = json.loads(response.text)
        # 获取直播间列表数据
        room_list = json_data.get("data").get('rl')
        for room_info in room_list:
            # 直播间ID
            room_id = room_info.get("rid")
            # 直播间url
            room_url = "https://www.douyu.com%s" % room_info.get("url")
            # 直播间名称
            room_name = room_info.get("rn")
            # 主播名称
            room_user = room_info.get("nn")
            # 直播间热度
            room_hot = room_info.get("ol")

            # 分类名称
            item['classify_name'] = response.meta['classify_name']
            # 频道名称
            item['channel_name'] = response.meta['channel_name']
            # 直播间ID
            item['room_id'] = room_id
            # 直播间url
            item['room_url'] = room_url
            # 直播间名称
            item['room_name'] = room_name
            # 直播间主播
            item['room_user'] = room_user
            # 直播间热度
            item['room_hot'] = room_hot
            yield item