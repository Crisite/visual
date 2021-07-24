import jieba
import pandas as pd
from pyecharts.charts import WordCloud, Pie , Timeline
from pyecharts import options as opts
from datetime import date, timedelta

news_title = pd.read_csv('./resource/news_title.csv')
# print(news_title.head().to_string())

# title列的数据存在一个列表 以字符串形式
title_list = news_title.title.tolist()

# print(title_list)

cuted_words = []

for title in title_list:
    words = jieba.cut(title)
    cuted_words.extend(words)

# print(cuted_words)

def is_contain_chinese(check_skr):
    """
    判断是否有中文字符
    :param check_skr:
    :return:
    """
    for ch in check_skr:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
        return False

# 处理后的中文单词列表
cn_words = []
for index, word in enumerate(cuted_words):
    if len(word) >=2 and is_contain_chinese(word):
        cn_words.append(word)
# print(cn_words)

# 把分词后的单词组装成DataFrame ，每个单词后计数为1
words_df = pd.DataFrame({'word':cn_words,'count':1})
# words_df.info()

# 根据单词分组并且计数
word_frequency = words_df.groupby('word').count()
# print(word_frequency)
# print(type(word_frequency))
# word_frequency.info()
# print(word_frequency.head())

word_cloud_data = [data for data in zip(word_frequency.index, word_frequency['count'].tolist())]
# print(word_cloud_data)
# print(type(word_cloud_data))

wordcloud = (
    WordCloud()
    .add(series_name='疫情分析',data_pair=word_cloud_data,word_size_range=[15,200])
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title = '热点分析',
            title_textstyle_opts=opts.TextStyleOpts(font_size=23)
        ),
        tooltip_opts=opts.TooltipOpts(is_show=True)
    )
    .render('./reasult/virues_dath.html')
)

