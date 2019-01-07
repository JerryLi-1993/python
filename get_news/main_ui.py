#！/usr/bin/env python3
# _*_ coding=utf-8 _*_

from PyQt5 import QtCore, QtWidgets
import sys

"""
说明：底层模板ui
修改：jr 2019-01-02
"""


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    # 底板
    def init_ui(self):
        # self.setFixedSize(1200, 700)  # 设置窗口大小
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.top_ui()  # 顶部ui设置
        self.left_ui()  # 左侧功能栏ui设置

        self.right_widget_1 = QtWidgets.QWidget()  # 创建右侧第1个部件
        self.create_right_ui(self.right_widget_1, 'right_widget_1') # 设置部件
        self.right_widget_2 = QtWidgets.QWidget()  # 创建右侧第2个部件
        self.create_right_ui(self.right_widget_2, 'right_widget_2')  # 设置部件
        self.right_widget_3 = QtWidgets.QWidget()  # 创建右侧第3个部件
        self.create_right_ui(self.right_widget_3, 'right_widget_3')  # 设置部件
        self.right_widget_4 = QtWidgets.QWidget()  # 创建右侧第一个部件
        self.create_right_ui(self.right_widget_4, 'right_widget_4')  # 设置部件
        self.right_widget_5 = QtWidgets.QWidget()  # 创建右侧第一个部件
        self.create_right_ui(self.right_widget_5, 'right_widget_5')  # 设置部件

        self.main_layout.addWidget(self.top_widget, 0, 0, 1, 17)
        self.main_layout.addWidget(self.left_widget, 1, 0, 15, 2)
        self.main_layout.addWidget(self.right_widget_1, 1, 2, 15, 3)
        self.main_layout.addWidget(self.right_widget_2, 1, 5, 15, 3)
        self.main_layout.addWidget(self.right_widget_3, 1, 8, 15, 3)
        self.main_layout.addWidget(self.right_widget_4, 1, 11, 15, 3)
        self.main_layout.addWidget(self.right_widget_5, 1, 14, 15, 3)

        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框:由于隐藏边框需要重写鼠标动作才能移动
        # self.setWindowOpacity(0.95)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # 避免隐藏窗口边框后，左侧部件没有背景颜色和边框显示，我们再对左侧部件添加QSS属性
        self.main_widget.setStyleSheet('''
            QWidget#left_widget{
                background:gray;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-right:1px solid white;
                border-bottom-left-radius:10px;
            }
        ''')
        # 设置布局内部件的间隙
        # self.main_layout.setSpacing(0)
        # 设置全屏
        self.showFullScreen()

    # 顶栏ui内容
    def top_ui(self):
        self.top_widget = QtWidgets.QWidget()  # 创建顶栏
        self.top_widget.setObjectName('top_widget')  # 设置名称
        self.top_layout = QtWidgets.QHBoxLayout()  # 创建顶栏部件的水平布局层
        self.top_widget.setLayout(self.top_layout)  # 设置顶栏部件的布局
        self.top_widget.setFixedHeight(42)  # 设置高度
        # 文本框
        self.top_tip = QtWidgets.QLabel()
        # 关闭按钮
        self.left_close = QtWidgets.QPushButton("×")
        self.left_close.clicked.connect(self.close)
        # 最小化按钮
        self.left_mini = QtWidgets.QPushButton("－")
        self.left_mini.clicked.connect(self.showMinimized)
        # 将按钮放在最右边
        self.top_layout.addWidget(self.top_tip)
        self.top_layout.addStretch(3)
        self.top_layout.addWidget(self.left_mini)
        self.top_layout.addWidget(self.left_close)

        # 左侧的最顶端是三个窗口控制按钮，我们需要将其设置为小圆点的形式。首先，我们使用QPushButton()的setFixedSize()方法，设置按钮的大小：
        self.left_close.setFixedSize(25, 25)  # 设置关闭按钮的大小
        self.left_mini.setFixedSize(25, 25)  # 设置最小化按钮大小

        # 通过setStyleSheet()方法，设置按钮部件的QSS样式，在这里，左侧按钮默认为淡绿色，鼠标悬浮时为深绿色；
        # 中间按钮默认为淡黄色，鼠标悬浮时为深黄色；右侧按钮默认为浅红色，鼠标悬浮时为红色。
        self.left_close.setStyleSheet('''
            QPushButton{
                background:#F76677;
                border-radius:5px;
            }
            QPushButton:hover{background:red;}
        ''')
        self.left_mini.setStyleSheet('''
            QPushButton{
                background:#6DDF6D;
                border-radius:5px;
            }
            QPushButton:hover{background:green;}
        ''')
        self.top_widget.setStyleSheet('''
            QWidget#top_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-top-left-radius:10px;
                border-bottom-right-radius:10px;
                border-bottom-left-radius:10px;
            }
        ''')

    # 左侧栏ui内容
    def left_ui(self):
        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件，作为控件窗口
        self.left_widget.setObjectName('left_widget')  # 设置名称
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.left_label_1 = QtWidgets.QPushButton("模块1")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("模块2")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("模块3")
        self.left_label_3.setObjectName('left_label')

        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)

        # 左侧的部件背景是灰色的，所以我们需要将左侧菜单中的按钮和文字颜色设置为白色，并且将按钮的边框去掉，在left_widget中设置qss样式为：
        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{
                border-left:4px solid red;
                font-weight:700;
            }
        ''')

    # 右侧ui
    def create_right_ui(self, widget, widget_name):
        widget.setObjectName(widget_name)  # 设置名称
        widget.setStyleSheet('''
            QWidget#'''+widget_name+'''{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
        ''')


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

