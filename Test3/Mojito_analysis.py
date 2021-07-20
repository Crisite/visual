import numpy as np
import pandas as pd
import jieba
import time
import requests
import json

from IPython.display import Image  # 用于在jupyter lab中显示本地图片

from pyecharts.charts import Pie, Bar, Line, Page
from pyecharts import options as opts
from pyecharts.globals import SymbolType

df_douban = pd.read_csv('./data/Mojito6.12.csv')
# 查看信息
# print(df_douban.head().to_string())
# df_douban.info()

# 查看重复条数
# print(df_douban.duplicated().sum())

# 新建一列star记录分数
df_douban['star'] = df_douban.rating_num.str.extract(r'(\d)')

# 删除 rating_num、user_url、comment_time
df_douban = df_douban.drop(['rating_num', 'comment_time', 'user_url'], axis=1)
# print(df_douban.head(20).to_string())

# 处理异常值 b替换a
df_douban['content'] = df_douban.content.replace('🤨', '微笑')

# 输入API Key和Secret Key
ak = 'iBrqRI4BQunrDH7Bi1060bBG'
sk = 'IkBdZFZQ2kBKVp3i1iXlDVcZzPQdGNmP'

host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(ak,
                                                                                                                     sk)

# 发起请求
r = requests.post(host)

# 获取token
token = r.json()['access_token']

# def get_sentiment_score(text):
#     """
#     输入文本，返回情感倾向得分
#     """
#     url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token={}'.format(token)
#     data = {
#         'text': text
#     }
#     data = json.dumps(data)  #字典-字符串
#     # 发起请求
#     try:
#         res = requests.post(url, data=data, timeout=3)
#         items_score = res.json()['items']
#     except Exception as e:
#         time.sleep(3)
#         res = requests.post(url, data=data, timeout=3)
#         items_score = res.json()['items']
#     return items_score
#
#
# # 调用函数分析每条评论的情感倾向
#
# score_list = []
#
# step = 0
# for i in df_douban['content']:
#     score = get_sentiment_score(i)
#     # 打印进度
#     step += 1
#     print('我正在获取第{}个评分'.format(step), end='\r')
#     score_list.append(score)
#
# # 提取正负概率
# positive_prob = [i[0]['positive_prob'] for i in score_list]
# negative_prob = [i[0]['negative_prob'] for i in score_list]
#
# df_douban['positive_prob'] = positive_prob
# df_douban['negative_prob'] = negative_prob
#
# # 正负向
# df_douban['label'] = ['正向' if i >0.5 else '负向' for i in df_douban.positive_prob]
# print(df_douban.head())

# 各星级数量
star_num = df_douban.star.value_counts()
star_num = star_num.sort_index()
print(star_num)

#   各评论星级占比Pie图
data_pair = [list(z) for z in zip([i + '星' for i in star_num.index], star_num.values.tolist())]
pie1 = (
    Pie(init_opts=opts.InitOpts(width='1350px', height='750px'))
        .add('', data_pair, radius=['35%', '60%'])
        .set_global_opts(
        title_opts=opts.TitleOpts(title='豆瓣短评评分占比'),
        legend_opts=opts.LegendOpts(orient='vertical', pos_top='15%', pos_left='2%')
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter='{b}:{d}%'))
        .render_notebook()
)


# def get_cut_words(content_series):
#     # 读入停用词表
#     stop_words = []
#
#     with open(r"./input/哈工大停用词表.txt", 'r', encoding='gb18030') as f:
#         lines = f.readlines()
#         for line in lines:
#             stop_words.append(line.strip())
#
#     # 添加关键词
#     my_words = ['周杰伦', '一首歌']
#     for i in my_words:
#         jieba.add_word(i)
#
#     #     自定义停用词
#     my_stop_words = ['歌有', '真的', '这首', '一首', '一点',
#                      '反正', '一段', '一句', '首歌']
#     stop_words.extend(my_stop_words)
#
#     # 分词
#     word_num = jieba.lcut(content_series.str.cat(sep='。'), cut_all=False)
#
#     # 条件筛选
#     word_num_selected = [i for i in word_num if i not in stop_words and len(i) >= 2]
#
#     return word_num_selected
#
#
# text1 = get_cut_words(content_series=df_douban[(df_douban.star == '4') | (df_douban.star == '5')]['content'])
# text1[:5]
#
#
# # 绘制词云图
# stylecloud.gen_stylecloud(text=' '.join(text1),
#                           max_words=1000,
#                           collocations=False,
#                           font_path=r'./input/经典综艺体简.TTF',
#                           icon_name='fas fa-thumbs-up',
#                           size=612,
#                           output_name='豆瓣正向评分词云图.png')
# Image(filename='豆瓣正向评分词云图.png')
