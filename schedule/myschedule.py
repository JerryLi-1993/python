#! /usr/bin/env python3
# _*_ coding=utf-8 _*_

"""
说明：任务调度
"""

import os
import pandas as pd
import datetime



class myschedule():
    def __init__(self):
        # 是否重跑模式，默认为否
        self.rerun = False
        # 执行相关任务
        self.exec_task()

    # 获取执行日期
    def get_date(self):
        exec_date = input("输入执行日期(YYYYMMDD):")
        # 如果不输入日期，则默认为今日
        if exec_date == '':
            exec_date = datetime.datetime.now().strftime('%Y%m%d')

        return date_str


    # 获取路径以及调度任务
    def get_task(self):
        # 当前文件路径
        self.curr_path = os.path.abspath('.')
        self.pre_path = os.path.abspath('..')
        # 读取任务csv，并设置id列为索引
        self.task = pd.read_csv(self.curr_path + "\\task.csv", encoding='utf-8', header=0, dtype=str)
        self.task = self.task.set_index('id')
        # 读取任务执行记录，并设置id列为索引
        self.task_log = self.task = pd.read_csv(self.curr_path + "\\task_log.csv", encoding='utf-8', header=0, dtype=str)
        self.task_log = self.task_log.set_index('id')

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
        task_enable = self.task[task_id.values(), 'enable']
        e_na_count = sum(task_enable.isna())  # 空值数量
        # enable为空或者为'N'
        if 'N' in task_enable or e_na_count >= 1:
            print("当前批次中有enable为空或者为'N'")
            flag = False

        # 判断is_failed列
        task_is_failed = self.task.loc[task_id.values(), 'is_failed']
        i_na_count = sum(task_is_failed.isna())
        # is_failed为空或者为Y
        if 'Y' in task_is_failed or i_na_count>=1:
            print("当前批次中有is_failed为空或者为'Y'")
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
        flag = False
        # 判断是否重跑模式，如果重跑则跳过id检查
        if self.rerun:
            return True

        # 获取执行时间
        exec_date = self.get_date()

        # 获取当前id的执行日志
        task_log = self.task_log.loc[id, 'exec_date']
        if exec_date in task_log:
            pass
        # 当前执行时间
        return flag



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
        # 获取任务id
        for id in self.task.index:
            print(id)
            # 获取当前id的所有依赖
            task_id = self.get_priority(id)
            print(task_id)
            # 检查当前批次任务是否可执行
            if not self.check_task(task_id):
                break
            # 检查当前任务是否需要执行


if __name__ == '__main__':
    myschedule = myschedule()
    os.system("pause")


task_id = get_priority('3')
task_enable = task.loc[task_id.values(), 'enable']
na_count = sum(task_enable.isna())
if 'N' in task_enable or na_count>=1 :
    print('xxx')

task['last_time'][0]

sum(task_enable.isna())

task.loc[task_id.values(), 'is_failed']
check_task(task_id)

def check_task(task_id):
    # 是否可执行
    flag = True

    # 判断enable列
    task_enable = task.loc[task_id.values(), 'enable']
    e_na_count = sum(task_enable.isna())  # 空值数量
    # enable为空或者为'N'
    if 'N' in task_enable or e_na_count >= 1:
        print("当前批次中有enable为空或者为'N'")
        flag = False

    # 判断is_failed列
    task_is_failed = task.loc[task_id.values(), 'is_failed']
    i_na_count = sum(task_is_failed.isna())
    # is_failed为空或者为Y
    if 'Y' in task_is_failed or i_na_count >= 1:
        print("当前批次中有is_failed为空或者为'Y'")
        flag = False

    return flag


task_log = task = pd.read_csv(r"E:\git_file\python\schedule\task_log.csv", encoding='utf-8', header=0, dtype=str)
task_log = task_log.set_index('id')

id = '2'
task_log = task_log.loc[id, ['exec_date','status']]


