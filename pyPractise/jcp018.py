'''
Created on 2017年1月8日

@author: Think
题目：求s=a+aa+aaa+aaaa+aa...a的值，其中a是一个数字。例如2+22+222+2222+22222(此时
　　　共有5个数相加)，几个数相加有键盘控制。
1.程序分析：关键是计算出每一项的值。
2.程序源代码：
'''
from pip._vendor.distlib.compat import raw_input
from _functools import reduce

def jcp018():
    tn = 0
    sn = []
    n = int(raw_input('n = :\n'))
    a = int(raw_input('a = :\n'))
    for count in range(n):
        tn = tn + a
        a = a* 10
        sn.append(tn)
        print(tn)
    sn = reduce(lambda x,y : x + y,sn)
    print(sn)
    
jcp018()    