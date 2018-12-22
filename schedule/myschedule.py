#! /usr/bin/env python3
# _*_ coding=utf-8 _*_

"""
说明：任务调度
"""

import os
import pandas as pd
import datetime
import subprocess
import traceback

"""
说明：执行task.csv中的任务
bug： 1、self.rerun = True时，会不对历史的错误记录进行判断，即有可能有如下情况：
         在重跑模式的情况下，如果有其中一个任务执行报错了，而有多个任务依赖这个任务，
         这个任务会每次都重新执行并报错，而不是:在第一次执行失败后，后续的任务不再执行该任务
      2、记录日志时，记录的是当前执行的traceback，而不是对应任务脚本中的错误   
修改：jr 2018-12-22
"""
class myschedule():
    def __init__(self):
        # 是否重跑模式，默认为否
        self.rerun = False
        # 获取执行时间
        self.exec_date = self.get_date()
        # 执行相关任务
        self.exec_task()

    # 获取执行日期
    def get_date(self):
        exec_date = input("输入执行日期(YYYYMMDD):")
        # 如果不输入日期，则默认为今日
        if exec_date == '':
            exec_date = datetime.datetime.now().strftime('%Y%m%d')

        return exec_date

    # 获取路径以及调度任务
    def get_task(self):
        # 当前文件路径
        self.curr_path = os.path.abspath('.')
        self.pre_path = os.path.abspath('..')
        # 读取任务csv，并设置id列为索引
        self.task = pd.read_csv(self.curr_path + "\\task.csv", encoding='utf-8', header=0, dtype=str)
        self.task = self.task.set_index('id')

    """
    描述：记录执行日志并输出到屏幕
    修改：jr 2018-12-22
    """
    def exec_log(self, msg):
        # 执行记录表日志路径
        log_path = self.curr_path + r'\log\exec_log.txt'
        # 输出提示信息
        print(msg)
        # 写入执行日志
        with open(log_path, 'a+', encoding='utf-8') as log:
            log.write('\n' + str(msg))

    """
    描述：获取当前任务的依赖任务
    参数：id         --输入任务id（列表）
    返回：refer_id   --返回依赖任务id（集合）
    修改：jr 2018-12-19
    """
    def get_refer(self,id):
        curr_id = self.task.loc[id, 'refer']
        refer_id = set()
        for each in curr_id:
            if each != 'N':
                for refer in each.split(','):
                    refer_id.add(refer)
        return refer_id

    """
    描述：获取当前任务id的依赖（包括依赖任务的依赖）
          返回键值从0开始的字典，键值小的任务有可能依赖于键值大的任务
    参数：id        --主任务id
    返回：task_id   --返回当前任务id以及依赖任务id(字典)
    修改：jr 2018-12-19
    """
    def get_priority(self, id):
        # 任务编号
        task_id = {}
        # 任务编号计数器
        count = 0
        # 插入当前任务id
        task_id[count] = id
        # 插入依赖任务id
        curr_id = list()
        curr_id.append(id)
        while True:
            # 获取当前任务的依赖任务
            refer_id =self.get_refer(curr_id)
            # 当依赖任务都为空时（没有依赖），退出循环
            if refer_id == set():
                break
            # 插入依赖任务id
            for each in refer_id:
                count += 1
                task_id[count] = each
            # 更新当前任务id
            curr_id =  refer_id
        return task_id

    """
    描述：检查任务以及其依赖是否可以执行
          当前任务以及依赖中有以下情况为不可执行：
          1、enable为N的任务
          2、is_failed为Y的任务(任务执行失败为Y,执行成功为N)
    参数：id    --当前任务以及依赖id
    返回：flag  --可执行返回True，否则返回False
    修改：jr 2018-12-19
    """
    def check_task(self, task_id):
        # 是否可执行
        flag = True

        # 判断enable列
        task_enable = self.task.loc[task_id.values(), 'enable']
        e_na_count = sum(task_enable.isna())  # 空值数量
        # enable为空或者为'N'
        if 'N' in task_enable or e_na_count >= 1:
            msg = '|   ' + '当前批次中有enable为空或者为N'
            self.exec_log(msg)
            flag = False

        # 判断is_failed列
        task_is_failed = self.task.loc[task_id.values(), 'is_failed']
        i_na_count = sum(task_is_failed.isna())
        # is_failed为空或者为Y
        if 'Y' in task_is_failed or i_na_count>=1:
            msg = '|   ' + '当前批次中有is_failed为空或者为Y'
            self.exec_log(msg)
            flag = False

        return flag

    """
    描述：判断当前id是否需要执行：使用last_time和is_failed进行判断
          由于依赖，可能当前任务已经执行完毕，避免重复执行
          以下情况判断为需要执行：
          1、判断type的执行类型
             如果type与last_time匹配，且is_failed为N，则表示任务今天已经执行，不需要重复执行
             如果type与last_time匹配，且is_failed为Y，则表示任务今天执行失败，直接返回失败，不需要执行
             如果type与last_time不匹配，则表示任务今天未执行，可以执行任务
    参数：id            --当前任务id
    返回：flag   True   --需要执行
                 false  --不需要执行
    修改：jr 2018-12-20
    """
    def check_id(self, id):

        type_flag = True  # 执行类型在当前执行日期是否需要执行
        # 获取脚本执行类型
        task_type = self.task.loc[id, 'type']
        # 判断脚本执行类型是否跳过周末执行(不跳过节假日)
        if task_type == 'weekday':
            # 0-6表示周一到周日
            week = datetime.datetime.strptime(self.exec_date, '%Y%m%d').weekday()
            type_flag = week not in [5, 6]
            # 记录日志
            msg = '|      ' + '周末，不执行该任务：%s' % id
            self.exec_log(msg)

        # 判断是否重跑模式，如果重跑则跳过id检查
        if self.rerun:
            return type_flag

        # 读取任务执行记录，并设置id列为索引
        task_log = pd.read_csv(self.curr_path + r"\log\task_log.csv", encoding='utf-8', header=0, dtype=str)
        task_log = task_log.set_index('id')
        # 获取当前id的执行日志
        task_log_select = task_log.loc[id, ['exec_date','status']]
        # 只有一条记录时，dateframe会转化成series，因此需要分开处理
        task_select_type = isinstance(task_log_select, pd.core.series.Series)
        task_log_success = []
        task_log_failed = []
        if task_select_type:
            if task_log_select.exec_date != self.exec_date:
                pass
            elif task_log_select.type=='success':
                task_log_success = ['1']
            elif task_log_select.type=='failed':
                task_log_failed = ['1']
        else:
            # 筛选执行日期的成功的记录
            task_log_success = task_log_select[(task_log_select['exec_date'] == self.exec_date)
                                                   & (task_log_select['status'] == 'success')]
            # 筛选执行日期的失败记录
            task_log_failed = task_log_select[(task_log_select['exec_date'] == self.exec_date)
                                                       & (task_log_select['status'] == 'failed')]

        if len(task_log_success) > 0:
            # 如果执行日期有成功的记录，则返回F，不需要执行该任务
            msg = '|      ' +  'id有成功的记录:%s' % id
            self.exec_log(msg)
            task_flag = False
        elif len(task_log_failed) > 0:
            # 如果执行日期有失败的记录，则返回F，不需要执行该任务
            msg = '|      ' +  'id有失败的记录:%s' % id
            self.exec_log(msg)
            task_flag = False
        else:
            # 如果该id没有执行记录，则返回T，可执行该任务
            task_flag = True

        return task_flag & type_flag

    """
    说明：执行当前id任务
    参数：id  --当前需要执行的id
    修改：jr 2018-12-21
    """
    def exec_id(self, id):
        # 当前id的相对路径
        file_script = self.task.loc[id, 'file_script']
        # 当前id的名称
        task_name = self.task.loc[id, 'name']
        # 脚本路径
        script_path = self.curr_path + file_script
        try:
            # 执行脚本
            subprocess.run("python %s" % script_path, shell=True, check=True)
            # 执行成功插入success
            with open(self.curr_path + r"log\task_log.csv", 'a+', encoding='utf-8') as csv:
                line = ''.join([id,',',task_name,',',self.exec_date,',','success',',',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                csv.writelines('\n')
                csv.writelines(line)
            # 成功后返回True
            return True
        except Exception as e:
            # 执行失败插入failed
            msg = traceback.format_exc()
            self.exec_log(msg)
            with open(self.curr_path + r"\log\task_log.csv", 'a+', encoding='utf-8') as csv:
                line = ''.join([id,',',task_name,',',self.exec_date,',','failed',',',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                csv.writelines('\n')
                csv.writelines(line)

    """
    调度任务信息
    任务优先级：
    1、任务不考虑设置优先级，目前根据任务id由小到大依次执行
    2、如果任务没有依赖，则直接执行当前任务
    3、如果任务有依赖，则追溯到源头任务，并从源头开始依次执行(从字典的键值大的任务开始执行)
    """
    def exec_task(self):
        # 获取任务列表
        self.get_task()
        # 记录日志
        self.exec_log('\n'*5)
        msg = '执行日期为：%s' % self.exec_date
        self.exec_log(msg)
        msg = "总共：%s 个任务" % len(self.task)
        self.exec_log(msg)
        # 获取任务id
        for id in self.task.index:
            # 获取当前id的所有依赖
            task_id = self.get_priority(id)
            # 记录日志
            msg = '\n本批次执行的任务为：%s' % task_id.values()
            self.exec_log(msg)
            # 检查当前批次任务是否可执行
            if not self.check_task(task_id):
                continue
            # 从后向前依次执行任务
            exec_sort = sorted(task_id.keys(), reverse=True)
            for each in exec_sort:
                exec_id = task_id[each]
                # 记录日志
                msg ='|   ' + '开始执行任务：%(exec_id)s    %(stamptime)s' % \
                      {'exec_id': exec_id, 'stamptime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                self.exec_log(msg)
                # 检查当前任务是否需要执行
                if self.check_id(exec_id):
                    # 执行当前id任务
                    is_success = self.exec_id(exec_id)
                    # 记录日志
                    if is_success:
                        msg = '|      ' +  '执行任务完毕：%(exec_id)s    %(stamptime)s' % \
                              {'exec_id':exec_id, 'stamptime':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        self.exec_log(msg)


if __name__ == '__main__':
    myschedule = myschedule()
    os.system("pause")
