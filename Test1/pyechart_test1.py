import pandas as pd
import seaborn as sns
import pyecharts.options as opts
from matplotlib import pyplot as plt
from pyecharts.charts import WordCloud


df = pd.read_csv('data/com.csv')

# index = 指定索引值 ，可以是一个列表

"""
数据处理
"""
# print(df.head(1))
# 删除后五列无效数据
df.drop(df.columns[-5:], axis=1, inplace=True)
# 删除第一列
df.drop('bianh', axis=1, inplace=True)

# print(df.loc[0].to_string())  # 返回[0]第0行的数据  [[0,1]]返回0到1行数据
# to_string()用于返回 DataFrame 类型的数据，如果不使用该函数，则输出结果为数据的前面 5 行和末尾 5 行
# df.info()
# 观察这一系列数据的范围、大小、波动趋势等等
# print(df.describe())

#  df = df[df['liver_days']>0]
"""
绘表
"""
# 设置UTF-8
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# fillna 处理缺失值 用无填充
df['death_reason'].fillna('无', inplace=True)
# df.isnull().sum() # 返回缺失值个数

# death_year death_month列
df['death_year'] = pd.to_datetime(df['death_data']).dt.year
df['death_month'] = pd.to_datetime(df['death_data']).dt.month


# 各年份淘汰公司总数柱形图
def year_bar():
    # 设置尺寸
    plt.figure(1, figsize=(16, 8))

    sns.countplot(x='death_year', data=df, color='CadetBlue')
    plt.title("各年份被淘汰的公司总数", fontsize=20)
    plt.xlabel('')

    plt.ylabel('')
    # xticks 设置刻度
    plt.xticks(rotation=45)
    plt.grid(False)
    con = list(df.groupby('death_year').death_year.count().values)
    for y, x in enumerate(con):
        plt.text(y, x, '%s' % x, va='center', size=14)
    plt.show()


# year_bar()
# 分析被淘汰的公司阵亡月份
def month_bar():
    # print(df['death_year'])
    # print(df['death_month'])
    df1 = df[df['death_year'].isin([2015, 2016, 2017, 2018, 2019])]
    # print(df1)
    # df1.info()
    plt.figure(1, figsize=(16, 8))
    sns.countplot(x='death_month', hue='death_year', data=df1, palette='Paired')
    plt.title('2015-2019年各月份被淘汰的公司总数', fontsize=20)
    plt.xlabel('')
    plt.ylabel('')
    plt.show()


# month_bar()

# 倒闭公司存活年数
def live_year():
    df['live_years'] = df['live_days'] / 365
    df['存活年限'] = pd.cut(x=df['live_years'], bins=[0, 1, 3, 5, 10, 25])

    sns.set_context("notebook", font_scale=1.3)
    sns.catplot(x='death_year', y='live_days', hue='存活年限', kind='swarm', data=df, height=8, aspect=2, palette='Set2')
    plt.title('各年份被淘汰公司的寿命', fontsize=20)

    plt.xticks(rotation=45)
    plt.show()


# live_year()
def death_reason():
    # value_count()查看有哪些不同的值，并计算每个值有多少个重复值
    reason_index = df['death_reason'].value_counts()[1, 11].index
    reason = df.loc[df['death_reason'].isin(reason_index), 'death_reason']

    plt.figure(1, figsize=(16, 8))
    sns.countplot(x=reason.values, order=reason_index, color='CadetBlue')
    plt.title('被淘汰公司的十大死亡原因', fontsize=20)

    plt.ylabel('')
    plt.xlabel('')
    plt.xticks(rotation=45)
    plt.grid(False)
    con = list(df['death_reason'].value_counts()[1:11].values)
    for y, x in enumerate(con):
        plt.text(y, x, '%s' % x, va='center', size=14)
    plt.show()


# death_reason()

# 不同地区淘汰公司
def death_addr():
    # 不同地区被淘汰的公司总数排名
    plt.figure(1, figsize=(16, 8))
    sns.countplot(x='com_addr', order=df['com_addr'].value_counts().index, data=df, color='CadetBlue')
    plt.title('近年来各省市被淘汰的公司总数排名', fontsize=20)

    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(rotation=45)
    plt.grid(False)
    con = list(df.groupby('com_addr').com_addr.count().values)
    con = sorted(con, reverse=True)
    for y, x in enumerate(con):
        plt.text(y, x, '%s' % x, va='center', size=12)
    plt.show()


# death_addr()

# 北上广淘汰公司
df2 = df[df['com_addr'].isin(['北京', '广东', '上海'])]


# 参考资料 https://www.cnblogs.com/cymx66688/p/10536403.html
# 北上广各行业淘汰数量排名
def city_death():
    plt.figure(1, figsize=(16, 8))
    sns.countplot(x='cat', order=df2['cat'].value_counts().index, hue='com_addr',
                  data=df2, palette='Paired')
    plt.title('北、上、广各行业被淘汰的总数排名', fontsize=20)

    plt.xlabel('')
    plt.ylabel('')
    plt.xticks(rotation=45)
    plt.legend(loc=1)
    plt.show()
#
# df.info()
# df2.info()
# print(df2.head().to_string())
# city_death()

# 死亡公司类型
def com_type():
    plt.figure(1, figsize=(16, 24))
    n = 0
    for x in ['电子商务', '企业服务', '本地生活', '金融', '社交网络']:
        n += 1
        #subplot(nrows, ncols, index, **kwargs)
        # 函数的nrows参数指定将数据图区域分成多少行
        # ncols参数指定将数据图区域分成多少列；
        # index参数指定获取第几个区域。
        plt.subplot(3, 2, n)
        sns.countplot(y='se_cat', hue='com_addr', order=df2[df2['cat'].isin([x])]['se_cat'].value_counts().index,
                      data=df2[df2['cat'].isin([x])], palette='Paired')
        plt.title(x, fontsize=18)
        plt.xlabel('')
        plt.ylabel('')
        plt.yticks(rotation=35)
        plt.legend(loc=7)
    plt.show()
# com_type()

# wordcloud
def financing_cloud():
    df_f = df['financing'].value_counts().reset_index(name='financing_count')
    x_data = df_f['index'].tolist()
    y_data = df_f['financing_count'].tolist()
    (
        WordCloud()
            .add(" ", [list(z) for z in zip(x_data, y_data)], word_size_range=[30, 90])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="融资情况", title_textstyle_opts=opts.TextStyleOpts(font_size=18)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    ).render_notebook()


# financing_cloud()

