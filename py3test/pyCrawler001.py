#!/usr/bin/python3
# -*- coding: utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup as bs
import re
import jieba #分词包
import pandas as pd
import numpy #numpy计算包
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc_params['figure.figsize'] = (10.0,5.0)
#from wordcloud import WordCloud #词云包

#第一步要对网页进行访问，python中使用的是urllib库。
resp = request.urlopen('https://movie.douban.com/cinema/nowplaying/changsha/')
#html_data是字符串类型的变量，里面存放了网页的html代码。
html_data = resp.read().decode('utf-8')

#print(html_data)

#第二步，需要对得到的html代码进行解析，得到里面提取我们需要的数据。
#第一个参数为需要提取数据的html，第二个参数是指定解析器，然后使用find_all()读取html标签中的内容。
soup = bs(html_data,'html.parser')

#在div id=”nowplaying“标签开始是我们想要的数据，里面有电影的名称、评分、主演等信息。
nowplaying_movie = soup.find_all('div',id='nowplaying')

nowplaying_movie_list = nowplaying_movie[0].find_all('li',class_='list-item')

#其中nowplaying_movie_list 是一个列表，可以用print(nowplaying_movie_list[0])查看里面的内容
#print(nowplaying_movie_list[0])

#在上图中可以看到data-subject属性里面放了电影的id号码，而在img标签的alt属性里面放了电影的名字，因此我们就通过这两个属性来得到电影的id和名称。（注：打开电影短评的网页时需要用到电影的id，所以需要对它进行解析）
nowplaying_list = []

for item in nowplaying_movie_list:
    nowplaying_dict = {}
    nowplaying_dict['id'] = item['data-subject']
    for tag_img_item in item.find_all('img'):
        nowplaying_dict['name'] = tag_img_item['alt']
        nowplaying_list.append(nowplaying_dict)

#print(nowplaying_list)
#print(nowplaying_list[0]['id'])
#print(nowplaying_list[0]['name'])   

'''
可以看到和豆瓣网址上面是匹配的。这样就得到了最新电影的信息了。
接下来就要进行对最新电影短评进行分析了。例如《战狼2》的短评网址为：
https://movie.douban.com/subject/26363254/comments?start=0&limit=20
'''
comment_requrl='https://movie.douban.com/subject/' + nowplaying_list[0]['id'] + '/comments' + '?' + 'start=0' + '&limit=20'
comment_resp = request.urlopen(comment_requrl)
comment_html_data = comment_resp.read().decode('utf-8')
comment_soup = bs(comment_html_data,'html.parser')
comment_div_lists = comment_soup.find_all('div',class_='comment')

eachCommentList = [];
for item in comment_div_lists:
    if item.find_all('p')[0].string is not None:
        eachCommentList.append(item.find_all('p')[0].string)

#此时在comment_div_lits 列表中存放的就是div标签和comment属性下面的html代码了
#print(eachCommentList)

#数据清晰开始
#为了方便进行数据进行清洗，我们将列表中的数据放在一个字符串数组中
comments = ''
for k in range(len(eachCommentList)):
    comments = comments + (str(eachCommentList[k])).strip()

'''
可以看到所有的评论已经变成一个字符串了，但是我们发现评论中还有不少的标点符号等。
这些符号对我们进行词频统计时根本没有用，因此要将它们清除。所用的方法是正则表达式。
python中正则表达式是通过re模块来实现的
'''
pattern = re.compile(r'[\u4e00-\u9fa5]+')
filterdata = re.findall(pattern,comments)
cleaned_comments = ''.join(filterdata)

#print(cleaned_comments)

'''
因此要进行词频统计，所以先要进行中文分词操作。在这里我使用的是结巴分词。
如果没有安装结巴分词，可以在控制台使用pip install jieba进行安装。
（注：可以使用pip list查看是否安装了这些库）
'''

segment = jieba.lcut(cleaned_comments)
words_df = pd.DataFrame({'segment':segment})

#print(words_df.head(5))
#我们的数据中有“看”、“太”、“的”等虚词（停用词），而这些词在任何场景中都是高频时，并且没有实际的含义，所以我们要他们进行清除。
stopwords = pd.read_csv("D:\Development\Python\stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'],encoding='utf-8')#quoting=3全不引用
words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

#print(words_df.head(5))

#接下来就要进行词频统计了
words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
words_stat = words_stat.reset_index().sort_values(by=["计数"],ascending=False)

#print(words_stat.head(5))


