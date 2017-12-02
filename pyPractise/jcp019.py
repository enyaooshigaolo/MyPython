'''
Created on 2017年1月9日

@author: Think
【程序19】
题目：一个数如果恰好等于它的因子之和，这个数就称为“完数”。例如6=1＋2＋3.编程
　　　找出1000以内的所有完数。
1. 程序分析：请参照程序<--上页程序14. 
2.程序源代码
'''
from sys import stdout

def jcp019():
    for j in range(2,1001):
        k = []
        n = -1
        s = j
        for i in range(1,j):
            if j % i == 0:
                n += 1
                s -= i
                k.append(i)
        if s == 0:
            print(' ')
            print('%d =' %j)
            for i in range (n):
                print('%d+ ' %k[i])                
            print(k[n])
            
jcp019()            