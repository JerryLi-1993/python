#! /usr/bin/env python3
# _*_ coding=utf-8 _*_

import os
import shutil
import subprocess
import program

# 删除历史数据
if os.path.exists("csv"):
    shutil.rmtree("csv")

# 执行微博热门搜索爬虫
subprocess.run(r"scrapy crawl get_weibo_hot -o .\csv\weibo_hot.csv", shell=True)
# 执行微博热门话题爬虫
subprocess.run(r"scrapy crawl get_weibo_topic -o .\csv\weibo_topic.csv", shell=True)
# 执行环球网部分新闻的爬虫
subprocess.run(r"scrapy crawl get_huangqiu_news -o .\csv\huangqiu_news.csv", shell=True)

if __name__ == '__main__':
    # 启动界面
    program.main()
