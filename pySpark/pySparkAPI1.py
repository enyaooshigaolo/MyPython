#!/usr/bin/python
# coding:utf-8

'''
https://www.iteblog.com/archives/1395.html
'''
import sys
import os
from pyspark import SparkConf,SparkContext

#print spark version
sc = SparkContext()
print('pyspark version:' + str(sc.version))

# map
# sc = spark context, parallelize creates an RDD from the passed object
x = sc.parallelize([1,2,3])
y = x.map(lambda x : (x,x**2))

# collect copies RDD elements to a list on the driver
print(x.collect())
print(y.collect())

'''
[1, 2, 3]
[(1, 1), (2, 4), (3, 9)]
'''
# flatMap
x = sc.parallelize([1,2,3])
y = x.flatMap(lambda x : (x, 100*x, x**2))
print(x.collect())
print(y.collect())
'''
[1, 2, 3]
[1, 100, 1, 2, 200, 4, 3, 300, 9]
'''

# mapPartitions
x = sc.parallelize([1,2,3],2)
def f(iterator) : yield sum(iterator)
y = x.mapPartitions(f)

# glom() flattens elements on the same partition
print(x.glom().collect())
print(y.glom().collect())

'''
[[1], [2, 3]]
[[1], [5]]
'''

# mapPartitionsWithIndex
x = sc.parallelize([1,2,3],2)
def f(partitionIdex,iterator) : yield (partitionIdex,sum(iterator))
y = x.mapPartitionsWithIndex(f)

# glom() flattens elements on the same partition
print(x.glom().collect())  
print(y.glom().collect())

'''
[[1], [2, 3]]
[[(0, 1)], [(1, 5)]]
'''

# getNumPartitions
x = sc.parallelize([1,2,3], 2)
y = x.getNumPartitions()
print(x.glom().collect())
print(y)

'''
[[1], [2, 3]]
2
'''

# filter
x = sc.parallelize([1,2,3])
y = x.filter(lambda x: x%2 == 1)  # filters out even elements
print(x.collect())
print(y.collect())

'''
[1, 2, 3]
[1, 3]
'''

# distinct
x = sc.parallelize(['A','A','B'])
y = x.distinct()
print(x.collect())
print(y.collect())

''' 
['A', 'A', 'B']
['A', 'B']
'''

#sample
x = sc.parallelize(range(7))
#call 'sample' 5 times
ylist = [x.sample(withReplacement=False,fraction=0.5) for i in range(5)]
print('x = ' + str(x.collect()))
for cnt,y in zip(range(len(ylist)),ylist):
    print('sample:' + str(cnt) + 'y= ' + str(y.collect()))

'''
x = [0, 1, 2, 3, 4, 5, 6]
sample:0 y = [0, 2, 5, 6]
sample:1 y = [2, 6]
sample:2 y = [0, 4, 5, 6]
sample:3 y = [0, 2, 6]
sample:4 y = [0, 3, 4]
'''

# takeSample
x = sc.parallelize(range(7))
#call 'sample' 5 time
ylist = [x.takeSample(withReplacement= False,num = 3) for i in range(5)]
print('x= ' + str(x.collect()))
for cnt,y in zip(range(len(ylist)),ylist):
    print('sample:' + str(cnt) + 'y= ' + str(y)) #no collent n y

'''
x = [0, 1, 2, 3, 4, 5, 6]
sample:0 y = [0, 2, 6]
sample:1 y = [6, 4, 2]
sample:2 y = [2, 0, 4]
sample:3 y = [5, 4, 1]
sample:4 y = [3, 1, 4]
'''

# union
x = sc.parallelize(['A','A','B'])
y = sc.parallelize(['D','C','A'])
z = x.union(y)
print(x.collect())
print(y.collect())
print(z.collect())

''' 
['A', 'A', 'B']
['D', 'C', 'A']
['A', 'A', 'B', 'D', 'C', 'A']
'''

# intersection
x = sc.parallelize(['A','A','B'])
y = sc.parallelize(['A','C','D'])
z = x.intersection(y)
print(x.collect())
print(y.collect())
print(z.collect())

'''
['A', 'A', 'B']
['A', 'C', 'D']
['A']
'''

# sortByKey
x = sc.parallelize([('B',1),('A',2),('C',3)])
y = x.sortByKey()
print(x.collect())
print(y.collect())

'''
[('B', 1), ('A', 2), ('C', 3)]
[('A', 2), ('B', 1), ('C', 3)]
'''

#sortBy
x = sc.parallelize(['Cat','Apple','Bat'])
def keyGen(val) : return val[0]
y = x.sortBy(keyGen)
print(y.collect())

'''
['Apple', 'Bat', 'Cat']
'''

# glom
x = sc.parallelize(['C','B','A'], 2)
y = x.glom()
print(x.collect()) 
print(y.collect())

'''
['C', 'B', 'A']
[['C'], ['B', 'A']]
'''

# cartesian
x = sc.parallelize(['A','B'])
y = sc.parallelize(['C','D'])
z = x.cartesian(y)
print(x.collect())
print(y.collect())
print(z.collect())

'''
['A', 'B']
['C', 'D']
[('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D')]
'''

# groupBy
x = sc.parallelize([1,2,3])
y = x.groupBy(lambda x: 'A' if (x%2 == 1) else 'B' )
print(x.collect())
# y is nested, this iterates through it
print([(j[0],[i for i in j[1]]) for j in y.collect()]) 

'''
[1, 2, 3]
[('A', [1, 3]), ('B', [2])]
'''

# foreach
from __future__ import print_function
x = sc.parallelize([1,2,3])
def f(el):
    '''side effect: append the current RDD elements to a file'''
    f1=open("./foreachExample.txt", 'a+') 
    print(el,file=f1)
 
# first clear the file contents
open('./foreachExample.txt', 'w').close()  
 
y = x.foreach(f) # writes into foreachExample.txt
 
print(x.collect())
print(y) # foreach returns 'None'
# print the contents of foreachExample.txt
with open("./foreachExample.txt", "r") as foreachExample:
    print (foreachExample.read())

'''     
[1, 2, 3]
None
3
1
2
'''

# foreachPartition
from __future__ import print_function
x = sc.parallelize([1,2,3],5)
def f(parition):
    '''side effect: append the current RDD partition contents to a file'''
    f1=open("./foreachPartitionExample.txt", 'a+') 
    print([el for el in parition],file=f1)
 
# first clear the file contents
open('./foreachPartitionExample.txt', 'w').close()  
 
y = x.foreachPartition(f) # writes into foreachExample.txt
 
print(x.glom().collect())
print(y)  # foreach returns 'None'
# print the contents of foreachExample.txt
with open("./foreachPartitionExample.txt", "r") as foreachExample:
    print (foreachExample.read())

''' 
[[], [1], [], [2], [3]]
None
[]
[]
[1]
[2]
[3]
'''

# collect
x = sc.parallelize([1,2,3])
y = x.collect()
print(x)  # distributed
print(y)  # not distributed

'''
ParallelCollectionRDD[87] at parallelize at <span class="wp_keywordlink_affiliate"><a href="https://www.iteblog.com/archives/tag/python/" title="" target="_blank" data-original-title="View all posts in Python">Python</a></span>RDD.scala:382
[1, 2, 3]
'''

# fold
x = sc.parallelize([1,2,3])
neutral_zero_value = 0  # 0 for sum, 1 for multiplication
y = x.fold(neutral_zero_value,lambda obj, accumulated: accumulated + obj) # computes cumulative sum
print(x.collect())
print(y)

'''
[1, 2, 3]
6
'''

# aggregate
x = sc.parallelize([2,3,4])
neutral_zero_value = (0,1) # sum: x+0 = x, product: 1*x = x
seqOp = (lambda aggregated, el: (aggregated[0] + el, aggregated[1] * el)) 
combOp = (lambda aggregated, el: (aggregated[0] + el[0], aggregated[1] * el[1]))
y = x.aggregate(neutral_zero_value,seqOp,combOp)  # computes (cumulative sum, cumulative product)
print(x.collect())
print(y)

'''
[2, 3, 4]
(9, 24)
'''

# max
x = sc.parallelize([1,3,2])
y = x.max()
print(x.collect())
print(y)
 
'''
[1, 3, 2]
3
'''
# min
x = sc.parallelize([1,3,2])
y = x.min()
print(x.collect())
print(y)

''' 
[1, 3, 2]
1
'''

# sum
x = sc.parallelize([1,3,2])
y = x.sum()
print(x.collect())
print(y)

''' 
[1, 3, 2]
6
'''

# count
x = sc.parallelize([1,3,2])
y = x.count()
print(x.collect())
print(y)

''' 
[1, 3, 2]
3
'''

