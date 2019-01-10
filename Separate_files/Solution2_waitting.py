#! /usr/bin/env python3
# _*_ coding = utf-8 _*_

from itertools import combinations
import sys


"""
问题：小明一家过一座桥，过桥时是黑夜，所以必须有灯。现在小明过桥要1秒，
      小明的弟弟要3秒，小明的爸爸要6秒，小明的妈妈要8秒，小明的爷爷要12秒。
      每次此桥最多可过两人，而过桥的速度依过桥最慢者而定，
      而且灯在点燃后30秒就会熄灭。问：小明一家如何过桥？
      
描述：考虑用枚举，过桥的时间需要越短越好，则添加以下假设：
        1、每次2人同时过桥，忽略1人过桥的情况
        2、每次1人返回，忽略2人同时返回的情况
      基于以上假设，则需要过桥与返回的次数固定：过桥4次，返回3次，共7次
      
修改：jr 2018-01-10
"""
class status:
    # 用于保存当前未过桥与已过桥人数的人员分布状态
    def __init__(self):
        self.start_list = [0]*7
        self.end_list = [0]*7

class Solution:
    def __init__(self):
        # 桥两端人员分布状态
        self.status = status()
        # 时间限制
        self.time_limit = 30
        # 过桥人数
        self.amount_limit = 2
        # 返回人数
        self.amount_back = 1
        # 当前递归层次
        self.level = 0
        # 所需要的时间
        self.time_list = []
        # 结果集
        self.result = []

    # 检测是否与条件有冲突，有冲突则返回1，否则返回0
    def conflict(self):
        if sum(self.time_list) > self.time_limit:
            return 1
        return 0

    # 判断是否需要返回，需要则返回1，不需要返回0
    @staticmethod
    def go_back(start_list):
        if len(start_list) == 0:
            return 0
        return 1

    """
    描述：将当前层次的时间以及人员信息插入相应的队列
          在插入当前层次的信息后，删除其层次后的信息，
          比如：插入第2层的时间为6之后，第3-7层的数据（如果存在）会被清除
          
    参数：level  当前所处层次           int
          time   当前方案所需时间       int
          scheme 当前过桥或者返回的方案 tuple
    
    修改：jr 2018-01-10
    """
    def insert(self, level, time, scheme):
        # 插入时间
        self.time_list = self.time_list[:level]
        self.time_list.append(time)
        # 插入人员方案
        self.result = self.result[:level]
        self.result.append(scheme)

        # 调试信息
        print("当前执行方案为：" + str(self.result))

    """
    描述：过桥，每次只能两人，时间算最长的人
    参数：start_list 未过桥的人员 list
          end_list   已过桥的人员 list
    修改：jr 2018-01-10
    """
    def through_bridge(self, start_list, end_list, level=0):
        # 调试信息
        print("=================================")
        print("当前处于%i" % level)
        print("未过桥的人为%s" % str(start_list))
        print("已过桥的人为%s" % str(end_list))
        # 保存当前人员分布状态
        self.status.start_list[level] = start_list[:]
        self.status.end_list[level] = end_list[:]
        # 过桥
        start_comb = combinations(start_list, self.amount_limit)
        for each_start in start_comb:
            # 调试信息
            print("=================================")
            print("当前处于%i" % level)
            print("当前尝试过桥的人为：%s" % str(each_start))
            # 恢复状态
            start_list = self.status.start_list[level][:]
            end_list = self.status.end_list[level][:]
            # 调试信息
            print("当前状态：{0}{1}".format(str(start_list), str(end_list)))
            # 将对应人员从桥的左边移动到右边
            for i in each_start:
                start_list.remove(i)
                end_list.append(i)
            # 添加时间以及人员信息
            self.insert(level, max(each_start), each_start)
            # 判断是否冲突,冲突则回退#
            if self.conflict():
                print("冲突#。。。。")
                continue

            # 判断是否需要人员返回
            if self.go_back(start_list):
                # 添加层级
                level = level + 1
                # 保存当前人员分布状态
                self.status.start_list[level] = start_list[:]
                self.status.end_list[level] = end_list[:]
                # 计算当前返回桥的组合
                back_comb = combinations(end_list, self.amount_back)
                for each_back in back_comb:
                    # 调试信息
                    print("=================================")
                    print("当前处于%i" % level)
                    print("当前尝试返回的人为：%s" % str(each_back))
                    # 恢复状态
                    start_list = self.status.start_list[level][:]
                    end_list = self.status.end_list[level][:]
                    # 调试信息
                    print("当前状态：{0}{1}".format(str(start_list), str(end_list)))
                    # 将对应人员从桥的右边移动到左边
                    for i in each_back:
                        end_list.remove(i)
                        start_list.append(i)
                    # 添加时间以及人员信息
                    self.insert(level, max(each_back), each_back)
                    # 判断是否冲突,冲突则回退
                    if self.conflict():
                        print("冲突#ht。。。。")
                        # for i in each_back:
                        #     end_list.append(i)
                        #     start_list.remove(i)
                        continue
                    self.through_bridge(start_list, end_list, level + 1)
                self.through_bridge(start_list, end_list, level - 1)


            # 如果人员不需要返回，则判断是否冲突，如果没有冲突，则输出
            if not self.conflict():
                print("符合要求的解为：%s" % str(self.result))
                print("所需要的时间为：%s" % str(self.time_list))
                print("累积时间为：%s" % str(sum(self.time_list)))
                # 暂停
                input("...请输入任意键继续...")


if __name__ == "__main__":
    # 设置递归深度
    # sys.setrecursionlimit(10000)
    Solution = Solution()
    start_list = [1, 3, 6, 8, 12]
    end_list = []
    Solution.through_bridge(start_list, end_list)


yy = status()
yy.start_list.append([111,1111,13331])
yy.end_list.append([222,22,2222,22222,22222,2222])