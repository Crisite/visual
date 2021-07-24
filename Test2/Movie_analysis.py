import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt


# 读取数据
labels1 = ['UserId','Gender','Age','Occupation','Zip-code']
users = pd.read_csv('./data/users.dat',sep='::',engine='python',header=None,names=labels1)

labels2 = ['MoviesId','Title','Genres']
movies = pd.read_csv('./data/movies.dat',sep='::', encoding='utf-8', engine='python',header=None,names=labels2)

labels3 = ['UserId','MoviesId','Rating','Timstamp']
ratings = pd.read_csv('./data/ratings.dat',sep='::',engine='python',header=None,names=labels3)

# 建表

df1 = pd.merge(left = movies ,right=ratings)
# print(df1.head(10))

movie_data = pd.merge(df1,users,how="outer")

print(movie_data['Title'].unique().size)

movie_rate_mean = pd.pivot_table(movie_data,values=['Rating'],index=['Title'],aggfunc='mean')
movie_rate_mean.sort_values(by='Rating',ascending = False,inplace = True)

print(movie_rate_mean[0:20])

movie_gender_rating = pd.pivot_table(movie_data,values=['Rating'],index=['Title','Gender'],aggfunc='mean')

# 换种透视方法 去掉values中括号->去掉rating标题
movie_gender_rating2 = pd.pivot_table(movie_data,values='Rating',index=['Title'],columns=['Gender'],aggfunc='mean')

movie_gender_rating2['diff'] = movie_gender_rating2.F - movie_gender_rating2.M
movie_gender_rating2.sort_values(by="diff",ascending=False,inplace=True)
#
f = movie_gender_rating2[:10]
#
# 最后十个就男性最喜欢的
m = movie_gender_rating2[-10:]

#处理一下 去掉存在的许多NAN
m = movie_gender_rating2.dropna()[-10:]

# 将男女喜欢的电影合成一张表
diff = pd.concat([f,m])

"""
分析结果 进行数据可视化

barh水平柱状图
"""
diff.plot(y='diff',kind='barh',figsize=(16,9))
plt.savefig('./reasult/chart1.png')
plt.show()

#评论次数最多热门的电影
# 用groupby 按照title 来做数据聚合
rating_count = movie_data.groupby(['Title']).size()
rating_count.sort_values(ascending = False)
movie_data['Age'].plot(kind = 'hist',bins = 20)
plt.savefig('./reasult/chart2.png')
plt.show()

# 用pandas.cut 函数将用户年龄分组
# 建立分组索引
labels4 = ['0-9','10-19','20-29','30-39','40-49','50-59']
# range是左闭右开 所以取到61
movie_data['Age_range']=pd.cut(movie_data.Age,bins=range(0,61,10),labels=labels4)

movie_data.groupby('Age_range').agg({'Rating':[np.size,np.mean]})

# 评论最多的50部电影排行
top_movie_title = movie_data.groupby('Title').size().sort_values()[::-1][:50].index
# 获取布尔索引
flag = movie_gender_rating2.index.isin(top_movie_title)
df1 = movie_gender_rating2[flag].sort_values(by='diff')
df1.plot(kind ='barh',figsize =(12,9))
plt.savefig('./reasult/chart3.png')
plt.show()


movie_rating_mean = pd.pivot_table(movie_data,values='Rating',index='Title')
index = movie_data.groupby('Title').size().sort_values()[::-1][:50].index

flag2 = movie_rating_mean.index.isin(index)
movie_rating_top_mean = movie_rating_mean[flag2]
df3 = movie_rating_top_mean.sort_values(by = 'Rating', ascending = False)

# 进行排序
# movie_rating_top_mean.sort_values(by='Rating',ascending = False).head(10)
