# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import cx_Oracle
import datetime


class DouyuPipeline(object):
    def process_item(self, item, spider):
        return item


class OraclePipeline(object):
    def open_spider(self, spider):
        # 连接数据库
        self.connect = cx_Oracle.connect("aaaa/ffff@127.0.0.1/ORCL")
        # 建立游标
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # 插入数据
        sql = """
            INSERT INTO T_DOUYU_INFO(DATE_TODAY,ROOM_ID,CLASSIFY_NAME,CHANNEL_NAME,ROOM_NAME,ROOM_URL,ROOM_USER,ROOM_HOT,DATE_TIME)
                            VALUES(TO_DATE('{DATE_TODAY}','YYYY-MM-DD'),'{ROOM_ID}','{CLASSIFY_NAME}','{CHANNEL_NAME}',
                                   '{ROOM_NAME}','{ROOM_URL}','{ROOM_USER}','{ROOM_HOT}',SYSDATE)
        """.format( DATE_TODAY      = datetime.date.today().strftime("%Y-%m-%d"),
                    ROOM_ID         = item['room_id'],
                    CLASSIFY_NAME   = item['classify_name'],
                    CHANNEL_NAME    = item['channel_name'],
                    ROOM_NAME       = item['room_name'],
                    ROOM_URL        = item['room_url'],
                    ROOM_USER       = item['room_user'],
                    ROOM_HOT        = item['room_hot'])
        self.cursor.execute(sql)
        # 提交
        self.connect.commit()

        return item

    def close_spider(self):
        # 关闭连接
        self.cursor.close()
        self.connect.close()
