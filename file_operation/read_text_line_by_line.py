# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) doudoudzj
# All rights reserved.
#

'''Python 逐行读取文本内容'''

import os.path


# 当前测试文件
test_file = os.path.join(os.path.dirname(__file__), 'read_text_test.txt')
print(test_file)


def method_1():
    '''方法一，每次只读取一行，并逐步提供输出，内存占用率较低，处理速度不会受到影响。
    '''
    f = open(test_file)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:  # readline() 每读取一行 line 变化，循环再次执行，直至读到文本最后
        print('method_1', line)  # 可以使用 strip() 移除结尾换行符
        line = f.readline()
    f.close()


def method_2():
    '''方法二'''
    for line in open(test_file):
        print('method_2', line.strip())  # 使用 strip() 移除结尾换行符


def method_3():
    '''方法三，一次性读取所有行，内存占用率较高，处理速度可能会受到影响。'''
    f = open(test_file)  # 返回一个文件对象
    lines = f.readlines()  # 读取全部内容后输出
    for line in lines:  # 从读取的全部行中循环
        print('method_3', line.strip())  # 使用 strip() 移除结尾换行符
    f.close()


if __name__ == '__main__':
    method_1()
    method_2()
    method_3()
