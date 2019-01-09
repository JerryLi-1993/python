#! /usr/bin/env python3
# _*_ coding = utf-8 _*_

from itertools import combinations
import sys


class Solution:
    def __init__(self):
        # 过桥前
        self.init_dic = self.start_dic = {
            '小明': 1,
            '弟弟': 3,
            '爸爸': 6,
            '妈妈': 8,
            '爷爷': 12
        }
        # 过桥后
        self.end_dic = {}
        # 时间限制
        self.time_limit = 30
        # 人数限定:考虑到限定的过桥问题，最优解显然都应该是从2人同时过桥，一人返回
        # 所以忽略一人独自过桥与2人同时返回的情况，直接限定过钱人员限制为2,返回人数为1
        self.amount_limit = 2
        self.amount_back = 1
        # 所需要的时间
        self.time_list = []
        # 过桥人员
        self.people_list = []

    # 检测是否满足约束:总用时不超过限定时间
    def conflict(self):
        if sum(self.time_list) > self.time_limit:
            return True
        else:
            return False

    # 检测是否结束：开始队列为没有元素，结束队列为长度为5
    def break_con(self):
        if len(self.start_dic) == 0 and len(self.end_dic) == 5:
            print("成功。。。。")
            return True
        else:
            return False

    '''
    描述：过桥，每次只能两人，时间算最长的人
    参数：item 剩下需要过桥的人员
    修改：jr 2018-01-08
    '''
    def through_bridge(self):
        while not self.break_con():
            # 调试信息
            print('''===========================================
            当前未过桥的人为%(start_dict)s
            当前已过桥的人为%(end_dict)s
            ''' % {'start_dict': self.start_dic, 'end_dict': self.end_dic})
            for name_list in combinations(self.start_dic.keys(), self.amount_limit):
                # 调试信息
                print("当前尝试过桥的人为：%s" % str(name_list))
                time_temp = []  # 时间，临时变量，用来判断对应取得最大的时间
                for name in name_list:
                    # 添加临时时间
                    time_temp.append(self.start_dic[name])
                    # 将对应人员从桥的左边移动到右边
                    self.end_dic[name] = self.start_dic[name]
                    del self.start_dic[name]
                # 添加时间,选择最大的时间
                time = max(time_temp)
                self.time_list.append(time)
                # 调试信息
                # print("当前所有时间为：%s" % str(self.time_list))
                # 判断是否冲突，冲突则回退
                if self.conflict():
                    # 如果是最后一组，则不进行回溯，否则可能死循环，并将人员分布重置
                    if len(self.start_dic) == 0:
                        self.start_dic = self.init_dic
                        self.end_dic = []
                        continue
                    # 调试信息
                    print("过桥回溯。。。。")
                    self.time_list.pop()
                    for name in name_list:
                        self.start_dic[name] = self.end_dic[name]
                        del self.end_dic[name]
                    continue
                # # 调试信息
                # print('''++++++++++++++++++++++++++++++++
                # 当前未过桥的人为%(start_dict)s
                # 当前已过桥的人为%(end_dict)s
                # ''' % {'start_dict': self.start_dic, 'end_dict': self.end_dic})

                # 判断是否所有人员都过桥了，如果没有，则需要返回一个人
                if not self.break_con():
                    for name_list_back in combinations(self.end_dic.keys(), self.amount_back):
                        # 调试信息
                        print("返回的人员为：%s" % str(name_list_back))
                        time_temp = []  # 时间，临时变量，用来判断对应取得最大的时间
                        for name in name_list_back:
                            # 添加临时时间
                            time_temp.append(self.end_dic[name])
                            # 将对应人员从桥的右边移动到左边
                            self.start_dic[name] = self.end_dic[name]
                            del self.end_dic[name]
                        # 添加时间,选择最大的时间
                        time = max(time_temp)
                        self.time_list.append(time)
                        # 调试信息
                        # print("当前所有时间为：%s" % str(self.time_list))
                        # 判断是否冲突
                        if self.conflict():
                            # 调试信息
                            print("返桥回溯。。。。")
                            self.time_list.pop()
                            for name in name_list_back:
                                self.end_dic[name] = self.start_dic[name]
                                del self.start_dic[name]
                            continue
                        self.through_bridge()


if __name__ == "__main__":
    # 设置递归深度
    sys.setrecursionlimit(10000)
    Solution = Solution()
    Solution.through_bridge()
