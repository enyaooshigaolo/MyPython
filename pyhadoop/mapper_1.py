#!/usr/bin/env python
# encoding: utf-8
'''
pyhadoop.reducer -- shortdesc

pyhadoop.reducer is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2017 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
http://www.cnblogs.com/wing1995/p/hadoop.html?utm_source=tuicool&utm_medium=referral
'''

import sys

wordDict = {}

for line in sys.stdin:
    line = line.strp()
    word,count = line.split()
    
    try:
        count = int(count)
    except:
        continue
    
    if wordDict.has_key(word):
        wordDict[word] += 1
    else:
        wordDict.setdefault(word,count)
        
for eachKey in wordDict:
    print (eachKey + '\t' + str(wordDict[eachKey]))