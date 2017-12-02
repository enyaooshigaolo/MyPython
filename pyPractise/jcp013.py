'''
Created on 2017年1月8日

@author: Think
【程序13】
题目：打印出所有的“水仙花数”，所谓“水仙花数”是指一个三位数，其各位数字立方和等于该数
　　　本身。例如：153是一个“水仙花数”，因为153=1的三次方＋5的三次方＋3的三次方。
1.程序分析：利用for循环控制100-999个数，每个数分解出个位，十位，百位。
2.程序源代码：
'''
import math

def jcp013():
    for n in range(100,1001):
        i = n // 100
        #print(i)
        j = n //10 % 10
        #print(j)
        k = n % 10
        #print(k)
        #if i * 100 + j * 10 + k == math.pow(i, 3) + math.pow(j, 3) + math.pow(k, 3):
        if i * 100 + j * 10 + k == i**3 + j**3 + k**3:
            print('%-5d ' %n)
        
jcp013()        