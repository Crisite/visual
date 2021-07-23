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

"""
统计确诊，意思，治愈，死亡病例的占比
"""

# 关于pd.read_csv参数详解 https://blog.csdn.net/luoyu_bie/article/details/79823705

epidemic_data = pd.read_csv('./resource/epidemic_data.csv',parse_dates=['updateTime'],
                            usecols=['countryName','provinceName','province_confirmedCount',
                                     'province_suspectedCount','province_curedCount',
                                     'province_deadCount','updateTime'
                                     ])
# print(epidemic_data.head().to_string())
# my_test = epidemic_data.groupby('countryName').count()
# print(my_test)

# 处理中国的疫情数据
# 全是中国的数据处理个p？
china_epidemic_data = epidemic_data[epidemic_data['countryName'] == '中国']

# updatetime 列 只保留到日，不保存 分秒时等数据
china_epidemic_data['updateTime'] = china_epidemic_data['updateTime'].apply(lambda updatetime:updatetime.date())

"""
drop.duplicates 简单去重函数
主要参数有 
subset=['A','B'],           输入要进行去重的列名，默认为None
keep='first',           first表示： 保留第一次出现的重复行，删除后面的重复行。
                            last表示： 删除重复项，保留最后一次出现。
                            False表示： 删除所有重复项。
inplace=True(默认为False)    是否直接在原数据上删除重复项或删除重复项后返回副本。
"""

# 只保留每个省份每日一条数据
unique_epidemic_data = china_epidemic_data.drop_duplicates(subset=['provinceName','updateTime'],keep='first')
# print(unique_epident_data.head(1000).to_string())
# unique_epident_data.info()

# 获取所有省份名
provinces = unique_epidemic_data.provinceName.drop_duplicates().tolist()
# print(province)

# 获取所有日期
updateDates = unique_epidemic_data.updateTime.drop_duplicates().tolist()
updateDates.sort()
# print(updateDates)
print('省份个数', len(provinces))
print('记录天数', len(updateDates))
print('原始数据记录数', len((unique_epidemic_data)))


def _fill_onr_province_day_data(total_data, today_filter_condition, last_day_filter_condition):
    """
    34个省份29天应有986条数据，
    原始数据只有896条，
    检查当天和前一天的数据，补全当天数据
    """
    all_cases = ['province_confirmedCount','province_suspectedCount',
                 'province_curedCount','province_deadCount']
    today_data = total_data[today_filter_condition]
    last_day_data = today_data[last_day_filter_condition]
    for case in all_cases:
        # isna()判断是否是空值（数字字段？ isnull是字符型）
        # .any()是做或判断 任意为Ture则返回True .all()是与判断 ，全为True则输出True
        if today_data[case].isna().any() and not last_day_data[case].isna().any():
            today_data[today_filter_condition, case] = unique_epidemic_data[last_day_filter_condition, case]
        elif today_data[case].isna().any() and last_day_data[case].isna().any():
            today_data[today_filter_condition, case] = 0

# 补全各省每天的数据
for updateDate in updateDates:
    for province in provinces:
        today_filter_condition = (unique_epidemic_data['updateTime'] == updateDate) & (
                                    unique_epidemic_data['provinceName'] == province)
        """
        timedelta代表两个datetime之间的时间差
        updateDate - timedelta(days=1) 意指当前天数减一
        如 + timedelta(days = 365)  时则值加365天
        """
        last_day = updateDate - timedelta(days=1)
        last_day_filter_condition = (unique_epidemic_data['updateTime'] == last_day)&(
            unique_epidemic_data['provinceName'] == province)
        if today_filter_condition.any():
            _fill_onr_province_day_data(unique_epidemic_data, today_filter_condition, last_day_filter_condition)
        else:
            last_province_data = unique_epidemic_data[last_day_filter_condition]
            last_province_data = last_province_data.copy()
            last_province_data['updateTime'] = updateDate
            unique_epidemic_data = pd.concat([unique_epidemic_data, last_province_data])

unique_epidemic_data.info()
