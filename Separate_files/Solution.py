#! /usr/bin/env python3
# _*_ coding = utf-8 _*_

from itertools import combinations


"""
问题：小明一家过一座桥，过桥时是黑夜，所以必须有灯。现在小明过桥要1秒，
      小明的弟弟要3秒，小明的爸爸要6秒，小明的妈妈要8秒，小明的爷爷要12秒。
      每次此桥最多可过两人，而过桥的速度依过桥最慢者而定，
      而且灯在点燃后30秒就会熄灭。问：小明一家如何过桥？
      
描述：考虑用枚举，过桥的时间需要越短越好，则添加以下假设：
        1、每次2人同时过桥，忽略1人过桥的情况
        2、每次1人返回，忽略2人同时返回的情况
      基于以上假设，则需要过桥与返回的次数固定：过桥4次，返回3次，共7次

bug：未考虑剪枝，需遍历所有组合
修改：jr 2018-01-14
"""
class Solution:
    def __init__(self):
        # 时间限制
        self.time_limit = 30
        # 过桥人数
        self.amount_limit = 2
        # 返回人数
        self.amount_back = 1
        # 结果集
        self.result_list = []

    """
    说明：计算时间  -多人通过计算耗时最长的人员
    参数：result_list 当前过桥组合列表 list
    返回: total_time  当前累积耗时 int
    修改：jr 2018-01-14
    """
    @staticmethod
    def get_total_time(result_list):
        total_time = 0
        for each in result_list:
            total_time = total_time + max(each)
        return total_time

    """
    说明：检测是否与条件有冲突
          判断传入列表的累计时间，如果时间大于限定时间，则表示冲突
    参数：result_list  当前方案 list
    返回：有冲突则返回1，否则返回0
    修改：jr 2018-01-14
    """
    def conflict(self, result_list):
        # 计算耗时
        total_time = self.get_total_time(result_list)
        if total_time > self.time_limit:
            return 1
        return 0

    # 输出
    @staticmethod
    def output(result_list):
        # 时间人员关系
        time_mapping = {
            1: "小明",
            3: "弟弟",
            6: "爸爸",
            8: "妈妈",
            12: "爷爷"
        }
        # 输出信息
        output_str = ""
        for each in result_list:
            # 判断过桥还是返回
            if len(each) == 2:
                action = "过桥"
            elif len(each) == 1:
                action = "返回"
            else:
                action = "error"
            for time in each:
                output_str = output_str + time_mapping.get(time) + ","
            output_str = output_str[:len(output_str)-1]
            output_str = output_str + action + "\n"
        print(output_str)
        input("...按任意键查找下一方案...")

    """
    描述：过桥，每次只能两人，时间算最长的人
    参数：start_list 未过桥的人员 list
          end_list   已过桥的人员 list
    修改：jr 2018-01-14
    """
    def through_bridge(self, start_list, end_list):
        # 过桥
        start_comb = combinations(start_list, self.amount_limit)
        for each_start in start_comb:
            # 保存当前人员分布状态
            self.result_list.append(each_start)
            # 将对应人员从桥的左边移动到右边
            for i in each_start:
                start_list.remove(i)
                end_list.append(i)

            # 检查结果集长度，没有未过桥人员，则输出当前方案
            if len(start_list) == 0:
                # 检查冲突
                if not self.conflict(self.result_list):
                    print(self.result_list, end="  ")
                    print("共耗时：%s秒" % self.get_total_time(self.result_list))
                    self.output(self.result_list)
            else:
                # 回桥
                self.back_bridge(start_list[:], end_list[:])
            # 回退
            self.result_list.pop()
            for i in each_start:
                start_list.append(i)
                end_list.remove(i)

    # 返回桥
    def back_bridge(self, start_list, end_list):
        # 回桥
        back_comb = combinations(end_list, self.amount_back)
        for each_back in back_comb:
            # 保存当前人员分布状态
            self.result_list.append(each_back)
            # 将对应人员从桥的右边移动到左边
            for i in each_back:
                end_list.remove(i)
                start_list.append(i)

            # 检查结果集长度，没有未过桥人员，则输出当前方案
            if len(start_list) == 0:
                if not self.conflict(self.result_list):
                    print(self.result_list, end="  ")
                    print("共耗时：%s秒" % self.get_total_time(self.result_list))
                    self.output(self.result_list)
            else:
                self.through_bridge(start_list[:], end_list[:])
            # 回退
            self.result_list.pop()
            for i in each_back:
                start_list.remove(i)
                end_list.append(i)


if __name__ == "__main__":
    # 设置递归深度
    # sys.setrecursionlimit(10000)
    Solution = Solution()
    start_list = [1, 3, 6, 8, 12]
    end_list = []
    Solution.through_bridge(start_list, end_list)

"""
部分结果：
================================================
[(1, 3), (1,), (6, 1), (3,), (8, 12), (1,), (3, 1)]  共耗时：29秒
小明,弟弟过桥
小明返回
爸爸,小明过桥
弟弟返回
妈妈,爷爷过桥
小明返回
弟弟,小明过桥

...按任意键查找下一方案...

[(1, 3), (1,), (6, 1), (1,), (8, 12), (3,), (1, 3)]  共耗时：29秒
小明,弟弟过桥
小明返回
爸爸,小明过桥
小明返回
妈妈,爷爷过桥
弟弟返回
小明,弟弟过桥
...
================================================
"""