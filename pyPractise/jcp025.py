'''
Created on 2017年1月14日

@author: Think
【程序25】 
题目：求1+2!+3!+...+20!的和
1.程序分析：此程序只是把累加变成了累乘。 
2.程序源代码：
'''

def jcp025():
    #method 1
    n = 0 
    s = 0
    t = 1
    for n in range(1,21):
        t *= n 
        s += t 
    print('1! + 2! + 3! + ... + 20! = %d' %s)
    
    #method 2
    s = 0
    l = range(1,21)
    def op(x):
        r = 1
        for i in range(1,x + 1):
            r *= i
        return r
    s = sum(map(op,l))
    print('1! + 2! + 3! + ... + 20! = %d' %s)
    
jcp025()    