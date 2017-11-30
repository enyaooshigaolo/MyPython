#!/usr/bin/env python
# encoding: utf-8
'''
pyhadoop.mapper -- shortdesc

pyhadoop.mapper is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2017 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
http://www.cnblogs.com/wing1995/p/hadoop.html?utm_source=tuicool&utm_medium=referral
'''

import sys

for line in sys.stdin:  # 遍历读入数据的每一行
    line = line.strip() # 将行尾行首的空格去除
    words = line.split()    #按空格将句子分割成单个单词
    for word in words:
        print ('%s\t%s' %(word,1))