#! /usr/bin/env python3
# _*_ coding=utf-8 _*_

import logging
import logging.handlers
import os


'''
USAGE:
    记录日志:
    1、记录所有级别的所有日志，写入磁盘，要求在每天凌晨进行日志切割，日志格式为：日期和时间-日志级别-日志信息
    2、单独记录error及以上级别的日志信息，不要求日志切割，日志格式为：日期和时间-日志级别-文件名[:行号]-日志信息
PARAMETERS:
    无
MODIFIED:
    jr 20180913  create
'''
class MyLog:
    # 设置日志文件的路径，默认为当前路径：
    # ./log/debug/debug 最新的日志文件为debug，历史的日志文件为debug%Y-%m-%d.log
    # ./log/error/error
    def __init__(self, debug_file_name='debug', error_file_name='error',
                 log_path=None):

        self.log_path = log_path

        # 默认路径为当前路径
        self.debug_file_path = './log/debug'
        self.error_file_path = './log/error'

        # 创建文件目录
        self.create_path()

        # 设置debug级别以上的日志的文件路径：debug_file_path
        self.debug_file = self.debug_file_path + '/' + debug_file_name
        # 设置error级别以上的日志的文件路径：error_file_name
        self.error_file = self.error_file_path + '/' + error_file_name

    def create_path(self):
        # 创建日志文件路径
        # 如果路径为空(默认值),则使用当前路径,否则就使用输入的路径
        if self.log_path:
            self.debug_file_path = str(self.log_path) + '/log/debug'
            self.error_file_path = str(self.log_path) + '/log/error'

        # 判断日志路径是否存在，如果不存在则创建对应的目录
        if not os.path.exists(self.debug_file_path):
            os.makedirs(self.debug_file_path)
        if not os.path.exists(self.error_file_path):
            os.makedirs(self.error_file_path)

    def get_logger(self):
        # 获取logger实例，如果参数为空，则返回root logger
        logger = logging.getLogger('MyLogger')
        # 设置logger等级 ***********************************************
        logger.setLevel(logging.DEBUG)

        # 设置handler debug
        # when-日志以天为单位,过了0点就进行分割
        # interval-when个单位的日志记录写在同一日志文件，设为为同一天的日志写在同一日志文件
        # backupCount-保留365个日志文件
        debug_log_handler = logging.handlers.TimedRotatingFileHandler(filename=self.debug_file, when='MIDNIGHT',
                                                                      interval=1, backupCount=365)
        # 设置日志文件名后缀
        debug_log_handler.suffix = "%Y-%m-%d.log"
        # debug_log_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}")
        # 设置日期格式
        debug_log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        # 添加handler
        logger.addHandler(debug_log_handler)

        # 设置handler error
        error_log_handler = logging.FileHandler(self.error_file)
        error_log_handler.setLevel(logging.ERROR)
        error_log_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
        # 添加handler
        logger.addHandler(error_log_handler)

        return logger


if __name__ == '__main__':
    # from mylogging import MyLog
    myLog = MyLog()
    myLogger = myLog.get_logger()
    # 测试10个日志文件
    for i in range(10):
        # 每次记录日之前插入5行，与之前的日志进行分割
        myLogger.info('\n'*5)
        # 记录日志
        myLogger.debug("logging.debug")
        myLogger.info("logging.info")
        myLogger.warning("logging.warning")
        myLogger.error("logging.error")
