'''
Created on 2017年1月6日

@author: Think
【程序6】
题目：用*号输出字母C的图案。
1.程序分析：可先用'*'号在纸上写出字母C，再分行输出。
2.程序源代码：
'''

import os
import sys

def jcp006():
    print ('Hello Python world!\n')
    print ('*' * 10)
    for i in range(5):
        print ('*        *')
    print ('*' * 10)
    print ('*\n' * 6)
    
jcp006()    