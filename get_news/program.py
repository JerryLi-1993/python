#! /usr/bin/env python3
# _*_ coding=utf-8 _*_

import pandas as pd
from main_ui import MainUi
from PyQt5 import QtCore, QtWidgets
import webbrowser
import sys


class Program(MainUi):
    def __init__(self):
        super().__init__()
        self.table_weibo_hot()  # 微博热搜
        self.table_weibo_topic()  # 微博热门话题
        self.table_huanqiu_news()  # 环球新闻

    # 微博热门搜索展示
    def table_weibo_hot(self):
        # 读取微博热门内容
        self.table_weibo_hot = pd.read_csv(r"csv\weibo_hot.csv", encoding='utf-8', dtype=str)
        self.table_weibo_hot = self.table_weibo_hot.fillna('')  # 将Nane设置为'',否则表格会显示nane
        # 设置表格
        table_select = self.table_weibo_hot[['hot_sort', 'title', 'amount']]
        row, column = table_select.shape
        TableWidget = QtWidgets.QTableWidget(row, column)
        # 将表格变为禁止编辑
        TableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置表头
        # self.TableWidget.setSpan(2,0,4,1)
        # self.TableWidget.setHorizontalHeaderLabels(['', '微博热搜'])  # 合并单元格
        TableWidget.verticalHeader().setVisible(False)  # 隐藏行表头
        TableWidget.horizontalHeader().setVisible(False)  # 隐藏列表头
        # 设置列宽
        TableWidget.setColumnWidth(0, 30)
        # 表格中不显示分割线
        TableWidget.setShowGrid(False)
        # 设置表格背景
        TableWidget.setStyleSheet('''
        QWidget{
            background:rgba(0,0,0,0);
            border-radius:5px;
            }
        ''')
        # 插入数据
        for i in range(row):
            for j in range(column):
                itemcontent = table_select.iloc[i, j]
                TableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(itemcontent)))

        # 添加标题
        title = QtWidgets.QPushButton("微博热搜")
        title.setObjectName('微博热搜')
        title.setStyleSheet(
            '''QPushButton{background:#00FFFF;border-radius:5px;}''')
        # 禁用水平滚动栏
        TableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # 设置垂直滚动栏的样式
        TableWidget.verticalScrollBar().setStyleSheet(
            "QScrollBar{background:transparent; width: 10px;}"
            "QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}"
            "QScrollBar::handle:hover{background:gray;}"
            "QScrollBar::sub-line{background:transparent;}"
            "QScrollBar::add-line{background:transparent;}"
        )
        # 双击打开网页
        TableWidget.itemDoubleClicked.connect(lambda: self.openUrl(TableWidget, 'weibo_hot'))

        # self.TableWidget.font().setStyleSheet("text-overflow: ellipsis")

        # 添加布局
        layout = QtWidgets.QGridLayout()
        self.right_widget_1.setLayout(layout)  # 设置右侧部件布局为网格
        layout.addWidget(title)
        layout.addWidget(TableWidget)

    # 微博热门话题展示
    def table_weibo_topic(self):
        # 读取微博热门内容
        self.table_weibo_topic = pd.read_csv(r"csv\weibo_topic.csv", encoding='utf-8', dtype=str)
        self.table_weibo_topic = self.table_weibo_topic.fillna('')  # 将Nane设置为'',否则表格会显示nane
        # 设置表格
        table_select = self.table_weibo_topic[['hot_sort', 'topic', 'amount']]
        row, column = table_select.shape
        TableWidget = QtWidgets.QTableWidget(row, column)
        # 将表格变为禁止编辑
        TableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置表头
        # self.TableWidget.setSpan(2,0,4,1)
        # self.TableWidget.setHorizontalHeaderLabels(['', '微博热搜'])  # 合并单元格
        TableWidget.verticalHeader().setVisible(False)  # 隐藏行表头
        TableWidget.horizontalHeader().setVisible(False)  # 隐藏列表头
        # 设置列宽
        TableWidget.setColumnWidth(0, 30)
        # 表格中不显示分割线
        TableWidget.setShowGrid(False)
        # 设置表格背景
        TableWidget.setStyleSheet('''
        QWidget{
            background:rgba(0,0,0,0);
            border-radius:5px;
            }
        ''')
        # 插入数据
        for i in range(row):
            for j in range(column):
                itemcontent = table_select.iloc[i, j]
                TableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(itemcontent)))

        # 添加标题
        title = QtWidgets.QPushButton("微博热门话题")
        title.setObjectName('微博热门话题')
        title.setStyleSheet('''QPushButton{background:#CCFFFF;border-radius:5px;}''')
        # 禁用水平滚动栏
        TableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # 设置垂直滚动栏的样式
        TableWidget.verticalScrollBar().setStyleSheet(
            "QScrollBar{background:transparent; width: 10px;}"
            "QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}"
            "QScrollBar::handle:hover{background:gray;}"
            "QScrollBar::sub-line{background:transparent;}"
            "QScrollBar::add-line{background:transparent;}"
        )
        # 双击打开网页
        TableWidget.itemDoubleClicked.connect(lambda: self.openUrl(TableWidget, 'weibo_topic'))

        # self.TableWidget.font().setStyleSheet("text-overflow: ellipsis")

        # 添加布局
        layout = QtWidgets.QGridLayout()
        self.right_widget_2.setLayout(layout)  # 设置右侧部件布局为网格
        layout.addWidget(title)
        layout.addWidget(TableWidget)

    # 环球网新闻展示
    def table_huanqiu_news(self):
        # 读取环球新闻的内容
        self.table_huanqiu_news = pd.read_csv(r"csv\huangqiu_news.csv", encoding='utf-8', dtype=str)
        self.table_huanqiu_news = self.table_huanqiu_news.fillna('')  # 将Nane设置为'',否则表格会显示nane
        # 设置表格
        table_select = self.table_huanqiu_news[['news_type', 'news']]
        row, column = table_select.shape
        TableWidget = QtWidgets.QTableWidget(row, column)
        # 将表格变为禁止编辑
        TableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        TableWidget.verticalHeader().setVisible(False)  # 隐藏行表头
        TableWidget.horizontalHeader().setVisible(False)  # 隐藏列表头
        # 设置列宽
        TableWidget.setColumnWidth(0, 50)
        TableWidget.setColumnWidth(1, 240)
        # 表格中不显示分割线
        TableWidget.setShowGrid(False)
        # 设置表格背景
        TableWidget.setStyleSheet('''
        QWidget{
            background:rgba(0,0,0,0);
            border-radius:5px;
            }
        ''')
        # 插入数据
        for i in range(row):
            for j in range(column):
                itemcontent = table_select.iloc[i, j]
                TableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(itemcontent)))

        # 添加标题
        title = QtWidgets.QPushButton("环球网新闻")
        title.setObjectName('环球网新闻')
        title.setStyleSheet('''QPushButton{background:#FFFFCC;border-radius:5px;}''')
        # 禁用水平滚动栏
        TableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # 设置垂直滚动栏的样式
        TableWidget.verticalScrollBar().setStyleSheet(
            "QScrollBar{background:transparent; width: 10px;}"
            "QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}"
            "QScrollBar::handle:hover{background:gray;}"
            "QScrollBar::sub-line{background:transparent;}"
            "QScrollBar::add-line{background:transparent;}"
        )
        # 双击打开网页
        TableWidget.itemDoubleClicked.connect(lambda: self.openUrl(TableWidget, 'huanqiu_news'))

        # self.TableWidget.font().setStyleSheet("text-overflow: ellipsis")

        # 添加布局
        layout = QtWidgets.QGridLayout()
        self.right_widget_3.setLayout(layout)  # 设置右侧部件布局为网格
        layout.addWidget(title)
        layout.addWidget(TableWidget)


    # 打开网页
    def openUrl(self, table, type):
        # 如果是标题列(第一列)，则打开对应的网页
        if table.currentColumn() == 1:
            if type == 'weibo_hot':
                url = self.table_weibo_hot.loc[table.currentRow(), 'url']
            elif type == 'weibo_topic':
                url = self.table_weibo_topic.loc[table.currentRow(), 'url']
            elif type == 'huanqiu_news':
                url = self.table_huanqiu_news.loc[table.currentRow(), 'url']
            else:
                # 如果没有连接，则返回脚本检查
                url = 'https://github.com/jr12137/python/tree/master/get_news'
            webbrowser.open_new_tab(url)


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = Program()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
