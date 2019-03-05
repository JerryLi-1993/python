# !/usr/bin/env python3
# _*_ coding=utf-8 _*_

# from scrapy.cmdline import execute
import subprocess
import os
from mylogging import MyLog
from myEmail import myEmail

# =======================================================================
# 记录日志(分别记录debug级别以及error级别的日志)
myLog = MyLog()
myLogger = myLog.get_logger()
myLogger.info('\n'*5)  # 每次记录日之前插入5行，与之前的日志进行分割
myLogger.info("开始执行项目**************************************")

# =======================================================================
# 获取当前路径
my_path = os.path.abspath('.')
# 1. 创建用户以及创建表
myLogger.info("创建用户及相关表**************************************")
file_path = my_path + '\\sql\\create_table.bat'
command = file_path + " " + my_path + '\\sql'
subprocess.run(command, shell=True)
myLogger.info("创建用户及相关表完成**************************************")

# =======================================================================
# 2. 执行爬虫，并将数据插入oracle
myLogger.info("开始执行爬虫,并将数据插入oracle**************************************")
subprocess.run(r"scrapy crawl douyu_spider", shell=True)
# execute("scrapy crawl douyu_spider".split())
myLogger.info("执行爬虫完成**************************************")

# =======================================================================
# 3. 对oracle中的数据进行处理
myLogger.info("对oracle中的数据进行处理**************************************")
file_path = my_path + '\\sql\\exec_proc.bat'
command = file_path + " " + my_path + '\\sql'
subprocess.run(command, shell=True)
myLogger.info("对oracle中的数据进行处理完成**************************************")

# =======================================================================
# 4. 数据可视化:R
myLogger.info("启动Rstudio对数据进行可视化**************************************")
# 删除历史html文件
html_path = my_path + "\\html\\douyu_analysis.html"
if os.path.exists(html_path):
    os.remove(html_path)
# 启动Rstudio
rstudio_path = r"D:\R\RStudio\bin\rstudio.exe"
rmd_path = my_path + "\\html\\\douyu_analysis.Rmd"
command = rstudio_path + " " + rmd_path
subprocess.run(command, shell=True)
myLogger.info("Rstudio数据处理完成**************************************")

# =======================================================================
# 5. 发送邮件
myLogger.info("开始发送邮件**************************************")
# 读取html
html = open(html_path, encoding='utf-8').read()
# 发送邮件
myEmail = myEmail()
myEmail.send_email(html)
myLogger.info("邮件发送结束**************************************")

# =======================================================================
# 6. 发送邮件
myLogger.info("项目结束**************************************")