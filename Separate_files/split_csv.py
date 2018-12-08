#! /usr/bin/env python3
# _*_ coding = utf-8 _*_
#===================================================================================
#         FILE: split_csv.py
#
#  DESCRIPTION: 将文本文件，分割成多个文件，每个文件指定行数
#
#        USAGE: 修改main函数中的，splitByLineCount('gfls_org_base.csv', 200)
#               分别指定待分割的文件名和文件行数
#
#       AUTHOR: jr
#      VERSION: 1.0
#       CREATE: 2018-12-08
#===================================================================================


import os
import time


def mkSubFile(lines, head, srcName, sub):
    # 分割文件名和文件类型
    [des_filename, extname] = os.path.splitext(srcName)
    filename = des_filename + '_' + str(sub) + extname
    print( 'make file: %s' %filename)
    fout = open(filename, mode='w', encoding='utf-8')
    try:
        fout.writelines([head])
        fout.writelines(lines)
        return sub + 1
    finally:
        fout.close()


def splitByLineCount(filename, count):
    fin = open(filename, mode='r', encoding='utf-8')
    try:
        head = fin.readline()
        buf = []
        sub = 1
        for line in fin:
            buf.append(line)
            if len(buf) == count:
                sub = mkSubFile(buf, head, filename, sub)
                buf = []
        if len(buf) != 0:
            sub = mkSubFile(buf, head, filename, sub)
    finally:
        fin.close()


if __name__ == '__main__':
    begin = time.time()
    splitByLineCount('gfls_org_base.csv', 200)
    end = time.time()
    print('time is %d seconds ' % (end - begin))
    os.system('pause')
