#!/usr/bin/python3
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

# histogram (example #1)
x = sc.parallelize([1,3,1,2,3])
y = x.histogram(buckets = 2)
print(x.collect())
print(y)

'''
[1, 3, 1, 2, 3]
([1, 2, 3], [2, 3])
'''

# histogram (example #2)
x = sc.parallelize([1,3,1,2,3])
y = x.histogram([0,0.5,1,1.5,2,2.5,3,3.5])
print(x.collect())
print(y)

'''
[1, 3, 1, 2, 3]
([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5], [0, 0, 2, 0, 1, 0, 2])
'''

# mean
x = sc.parallelize([1,3,2])
y = x.mean()
print(x.collect())
print(y)
'''
[1, 3, 2]
2.0
'''

# variance方差
x = sc.parallelize([1,3,2])
y = x.variance()  # divides by N
print(x.collect())
print(y)

'''
[1, 3, 2]
0.666666666667
'''

# stdev 标准偏差
x = sc.parallelize([1,3,2])
y = x.stdev()  # divides by N
print(x.collect())
print(y)
 
'''
[1, 3, 2]
0.816496580928
'''

# sampleStdev
x = sc.parallelize([1,3,2])
y = x.sampleStdev() # divides by N-1
print(x.collect())
print(y)
'''
[1, 3, 2]
1.0
'''

# sampleVariance
x = sc.parallelize([1,3,2])
y = x.sampleVariance()  # divides by N-1
print(x.collect())
print(y)

''' 
[1, 3, 2]
1.0
'''

# countByValue
x = sc.parallelize([1,3,1,2,3])
y = x.countByValue()
print(x.collect())
print(y)

'''
[1, 3, 1, 2, 3]
defaultdict(<type 'int'>, {1: 2, 2: 1, 3: 2})
'''

# top
x = sc.parallelize([1,3,1,2,3])
y = x.top(num = 3)
print(x.collect())
print(y)

''' 
[1, 3, 1, 2, 3]
[3, 3, 2]
'''

# takeOrdered
x = sc.parallelize([1,3,1,2,3])
y = x.takeOrdered(num = 3)
print(x.collect())
print(y)

'''
[1, 3, 1, 2, 3]
[1, 1, 2]
'''

# take
x = sc.parallelize([1,3,1,2,3])
y = x.take(num = 3)
print(x.collect())
print(y)

'''
[1, 3, 1, 2, 3]
[1, 3, 1]
'''

# first
x = sc.parallelize([1,3,1,2,3])
y = x.first()
print(x.collect())
print(y)

''' 
[1, 3, 1, 2, 3]
1
'''

# collectAsMap
x = sc.parallelize([('C',3),('A',1),('B',2)])
y = x.collectAsMap()
print(x.collect())
print(y)

'''
[('C', 3), ('A', 1), ('B', 2)]
{'A': 1, 'C': 3, 'B': 2}
'''

# keys
x = sc.parallelize([('C',3),('A',1),('B',2)])
y = x.keys()
print(x.collect())
print(y.collect())

'''
[('C', 3), ('A', 1), ('B', 2)]
['C', 'A', 'B']
'''

# values
x = sc.parallelize([('C',3),('A',1),('B',2)])
y = x.values()
print(x.collect())
print(y.collect())

'''
[('C', 3), ('A', 1), ('B', 2)]
[3, 1, 2]
'''

# reduceByKey
x = sc.parallelize([('B',1),('B',2),('A',3),('A',4),('A',5)])
y = x.reduceByKey(lambda agg, obj: agg + obj)
print(x.collect())
print(y.collect())

'''
[('B', 1), ('B', 2), ('A', 3), ('A', 4), ('A', 5)]
[('A', 12), ('B', 3)]
'''

# reduceByKeyLocally
x = sc.parallelize([('B',1),('B',2),('A',3),('A',4),('A',5)])
y = x.reduceByKeyLocally(lambda agg, obj: agg + obj)
print(x.collect())
print(y)

'''
[('B', 1), ('B', 2), ('A', 3), ('A', 4), ('A', 5)]
{'A': 12, 'B': 3}
'''

# countByKey
x = sc.parallelize([('B',1),('B',2),('A',3),('A',4),('A',5)])
y = x.countByKey()
print(x.collect())
print(y)

''' 
[('B', 1), ('B', 2), ('A', 3), ('A', 4), ('A', 5)]
defaultdict(<type 'int'>, {'A': 3, 'B': 2})
'''
# join
x = sc.parallelize([('C',4),('B',3),('A',2),('A',1)])
y = sc.parallelize([('A',8),('B',7),('A',6),('D',5)])
z = x.join(y)
print(x.collect())
print(y.collect())
print(z.collect())

''' 
[('C', 4), ('B', 3), ('A', 2), ('A', 1)]
[('A', 8), ('B', 7), ('A', 6), ('D', 5)]
[('A', (2, 8)), ('A', (2, 6)), ('A', (1, 8)), ('A', (1, 6)), ('B', (3, 7))]
'''

# leftOuterJoin
x = sc.parallelize([('C',4),('B',3),('A',2),('A',1)])
y = sc.parallelize([('A',8),('B',7),('A',6),('D',5)])
z = x.leftOuterJoin(y)
print(x.collect())
print(y.collect())
print(z.collect())

'''
[('C', 4), ('B', 3), ('A', 2), ('A', 1)]
[('A', 8), ('B', 7), ('A', 6), ('D', 5)]
[('A', (2, 8)), ('A', (2, 6)), ('A', (1, 8)), ('A', (1, 6)), ('C', (4, None)), ('B', (3, 7))]
'''

# rightOuterJoin
x = sc.parallelize([('C',4),('B',3),('A',2),('A',1)])
y = sc.parallelize([('A',8),('B',7),('A',6),('D',5)])
z = x.rightOuterJoin(y)
print(x.collect())
print(y.collect())
print(z.collect())

'''
[('C', 4), ('B', 3), ('A', 2), ('A', 1)]
[('A', 8), ('B', 7), ('A', 6), ('D', 5)]
[('A', (2, 8)), ('A', (2, 6)), ('A', (1, 8)), ('A', (1, 6)), ('B', (3, 7)), ('D', (None, 5))]
'''

# partitionBy
x = sc.parallelize([(0,1),(1,2),(2,3)],2)
y = x.partitionBy(numPartitions = 3, partitionFunc = lambda x: x)  # only key is passed to paritionFunc
print(x.glom().collect())
print(y.glom().collect())

'''
[[(0, 1)], [(1, 2), (2, 3)]]
[[(0, 1)], [(1, 2)], [(2, 3)]]
'''
# combineByKey
x = sc.parallelize([('B',1),('B',2),('A',3),('A',4),('A',5)])
createCombiner = (lambda el: [(el,el**2)]) 
mergeVal = (lambda aggregated, el: aggregated + [(el,el**2)]) # append to aggregated
mergeComb = (lambda agg1,agg2: agg1 + agg2 )  # append agg1 with agg2
y = x.combineByKey(createCombiner,mergeVal,mergeComb)
print(x.collect())
print(y.collect())

'''
[('B', 1), ('B', 2), ('A', 3), ('A', 4), ('A', 5)]
[('A', [(3, 9), (4, 16), (5, 25)]), ('B', [(1, 1), (2, 4)])]
'''

# aggregateByKey
x = sc.parallelize([('B',1),('B',2),('A',3),('A',4),('A',5)])
zeroValue = [] # empty list is 'zero value' for append operation
mergeVal = (lambda aggregated, el: aggregated + [(el,el**2)])
mergeComb = (lambda agg1,agg2: agg1 + agg2 )
y = x.aggregateByKey(zeroValue,mergeVal,mergeComb)
print(x.collect())
print(y.collect())

'''
[('B', 1), ('B', 2), ('A', 3), ('A', 4), ('A', 5)]
[('A', [(3, 9), (4, 16), (5, 25)]), ('B', [(1, 1), (2, 4)])]
'''

# foldByKey
x = sc.parallelize([('B',1),('B',2),('A',3),('A',4),('A',5)])
zeroValue = 1 # one is 'zero value' for multiplication
y = x.foldByKey(zeroValue,lambda agg,x: agg*x )  # computes cumulative product within each key
print(x.collect())
print(y.collect())
 
'''
[('B', 1), ('B', 2), ('A', 3), ('A', 4), ('A', 5)]
[('A', 60), ('B', 2)]
'''

# groupByKey
x = sc.parallelize([('B',5),('B',4),('A',3),('A',2),('A',1)])
y = x.groupByKey()
print(x.collect())
print([(j[0],[i for i in j[1]]) for j in y.collect()])

'''
[('B', 5), ('B', 4), ('A', 3), ('A', 2), ('A', 1)]
[('A', [3, 2, 1]), ('B', [5, 4])]
'''

# flatMapValues
x = sc.parallelize([('A',(1,2,3)),('B',(4,5))])
y = x.flatMapValues(lambda x: [i**2 for i in x]) # function is applied to entire value, then result is flattened
print(x.collect())
print(y.collect())

'''
[('A', (1, 2, 3)), ('B', (4, 5))]
[('A', 1), ('A', 4), ('A', 9), ('B', 16), ('B', 25)]
'''

# mapValues
x = sc.parallelize([('A',(1,2,3)),('B',(4,5))])
y = x.mapValues(lambda x: [i**2 for i in x]) # function is applied to entire value
print(x.collect())
print(y.collect())

'''
[('A', (1, 2, 3)), ('B', (4, 5))]
[('A', [1, 4, 9]), ('B', [16, 25])]
'''

# groupWith
x = sc.parallelize([('C',4),('B',(3,3)),('A',2),('A',(1,1))])
y = sc.parallelize([('B',(7,7)),('A',6),('D',(5,5))])
z = sc.parallelize([('D',9),('B',(8,8))])
a = x.groupWith(y,z)
print(x.collect())
print(y.collect())
print(z.collect())
print("Result:")
for key,val in list(a.collect()): 
    print(key, [list(i) for i in val])

'''
[('C', 4), ('B', (3, 3)), ('A', 2), ('A', (1, 1))]
[('B', (7, 7)), ('A', 6), ('D', (5, 5))]
[('D', 9), ('B', (8, 8))]
Result:
D [[], [(5, 5)], [9]]
C [[4], [], []]
B [[(3, 3)], [(7, 7)], [(8, 8)]]
A [[2, (1, 1)], [6], []]
'''

# cogroup
x = sc.parallelize([('C',4),('B',(3,3)),('A',2),('A',(1,1))])
y = sc.parallelize([('A',8),('B',7),('A',6),('D',(5,5))])
z = x.cogroup(y)
print(x.collect())
print(y.collect())
for key,val in list(z.collect()):
    print(key, [list(i) for i in val])
'''
[('C', 4), ('B', (3, 3)), ('A', 2), ('A', (1, 1))]
[('A', 8), ('B', 7), ('A', 6), ('D', (5, 5))]
A [[2, (1, 1)], [8, 6]]
C [[4], []]
B [[(3, 3)], [7]]
D [[], [(5, 5)]]
'''

# sampleByKey
x = sc.parallelize([('A',1),('B',2),('C',3),('B',4),('A',5)])
y = x.sampleByKey(withReplacement=False, fractions={'A':0.5, 'B':1, 'C':0.2})
print(x.collect())
print(y.collect())

'''
[('A', 1), ('B', 2), ('C', 3), ('B', 4), ('A', 5)]
[('B', 2), ('C', 3), ('B', 4)]
'''

# subtractByKey
x = sc.parallelize([('C',1),('B',2),('A',3),('A',4)])
y = sc.parallelize([('A',5),('D',6),('A',7),('D',8)])
z = x.subtractByKey(y)
print(x.collect())
print(y.collect())
print(z.collect())

'''
[('C', 1), ('B', 2), ('A', 3), ('A', 4)]
[('A', 5), ('D', 6), ('A', 7), ('D', 8)]
[('C', 1), ('B', 2)]
'''

# subtract
x = sc.parallelize([('C',4),('B',3),('A',2),('A',1)])
y = sc.parallelize([('C',8),('A',2),('D',1)])
z = x.subtract(y)
print(x.collect())
print(y.collect())
print(z.collect())

'''
[('C', 4), ('B', 3), ('A', 2), ('A', 1)]
[('C', 8), ('A', 2), ('D', 1)]
[('A', 1), ('C', 4), ('B', 3)]
'''

# keyBy
x = sc.parallelize([1,2,3])
y = x.keyBy(lambda x: x**2)
print(x.collect())
print(y.collect())

''' 
[1, 2, 3]
[(1, 1), (4, 2), (9, 3)]
'''

# repartition
x = sc.parallelize([1,2,3,4,5],2)
y = x.repartition(numPartitions=3)
print(x.glom().collect())
print(y.glom().collect())

'''
[[1, 2], [3, 4, 5]]
[[], [1, 2, 3, 4], [5]]
'''

# coalesce
x = sc.parallelize([1,2,3,4,5],2)
y = x.coalesce(numPartitions=1)
print(x.glom().collect())
print(y.glom().collect())

'''
[[1, 2], [3, 4, 5]]
[[1, 2, 3, 4, 5]]
'''

# zip
x = sc.parallelize(['B','A','A'])
# zip expects x and y to have same #partitions and #elements/partition
y = x.map(lambda x: ord(x))  
z = x.zip(y)
print(x.collect())
print(y.collect())
print(z.collect())

'''
['B', 'A', 'A']
[66, 65, 65]
[('B', 66), ('A', 65), ('A', 65)]
'''

# zipWithIndex
x = sc.parallelize(['B','A','A'],2)
y = x.zipWithIndex()
print(x.glom().collect())
print(y.collect())

'''
[['B'], ['A', 'A']]
[('B', 0), ('A', 1), ('A', 2)]
'''

# zipWithUniqueId
x = sc.parallelize(['B','A','A'],2)
y = x.zipWithUniqueId()
print(x.glom().collect())
print(y.collect())

'''
[['B'], ['A', 'A']]
[('B', 0), ('A', 1), ('A', 3)]
'''