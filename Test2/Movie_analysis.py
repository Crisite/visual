# import inline as inline
# import matplotlib
# import pandas as pd
# import numpy as np
# from IPython.core.display import display
#
# from pandas import Series,DataFrame
# import matplotlib.pyplot as plt
# # %matplotlib inline
#
#
# # 读取数据
# labels = ['UserId', 'Gender', 'Age', 'Occupation', 'Zip-code']
# users = pd.read_csv('./data/users.dat', sep='::', engine='python', header=None, names=labels)
#
# display(users.head(), users.shape)
#
# print(users.head())
#
# labels = ['Movied', 'Title', 'Genres']
# movies = pd.read_csv('./data/movies.dat', sep='::', engine='python', header=None, names=labels)
#
# display(movies.head(), movies.shape)
#
# labels = ['UserId', 'MovieId', 'Rating', 'Timstamp']
# ratings = pd.read_csv('./data/ratings.dat', sep='::', engine='python', header=None, names=labels)
#
# display(ratings.head(), ratings.shape)
#
# # movie_data.head()