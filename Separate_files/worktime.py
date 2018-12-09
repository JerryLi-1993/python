# /usr/bin/env python3
# _*_ coding=utf-8 _*_
#===================================================================================
#         FILE: worktime.py
#
#  DESCRIPTION: 用来记录工时：记录当天第一次点开时间和当前点开时间，以及两个时间的差
#
#        USAGE: -
#
#       AUTHOR: jr
#      VERSION: 1.0
#       CREATE: 2018-12-09
#===================================================================================


import os
import datetime
import pandas as pd


# 生成日期时间
time_AM = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
today = datetime.datetime.now().strftime("%Y%m%d")
file_name = "workTime.csv"

# 写入csv
with open(file=file_name, mode='a+', encoding='utf-8') as csv_file:
    csv_file.writelines('\n' + time_AM)

# 读取csv
data = pd.read_csv(file_name, header=None)
# 获取记录最值
data.columns = ['log']
today_log = data[data.log > today]
today_min = today_log.log.min()
today_max = today_log.log.max()
# 计算时间差
today_min_ts = pd.to_datetime(today_min)
today_max_ts = pd.to_datetime(today_max)
print(today + "  最早时间记录:%s" % today_min_ts)
print(today + "  最晚时间记录:%s" % today_max_ts)
print(today + "  时长:%s" % (today_max_ts - today_min_ts))

os.system("pause")