'''
Created on 2017年1月6日

@author: Think
【程序7】
题目：输出特殊图案，请在c环境中运行，看一看，Very Beautiful!
1.程序分析：字符共有256个。不同字符，图形不一样。　　　　　　
2.程序源代码：
'''

import os
import sys

def jcp007():
    a = 176
    b = 219
    
    print(chr(b),chr(a),chr(a),chr(a),chr(b))
    print(chr(a),chr(b),chr(a),chr(a),chr(a))
    print(chr(a),chr(a),chr(a),chr(b),chr(a))
    print(chr(a),chr(b),chr(a),chr(a),chr(a))
    print(chr(b),chr(a),chr(a),chr(a),chr(b))
    
jcp007()    