import numpy as np
import pandas as pd
from dateutil import parser
from matplotlib import pyplot as plt
from matplotlib import dates
from sklearn.svm import SVR

df_asti = pd.read_csv('./resource/asti_270615.csv')
df_bologna = pd.read_csv('./resource/bologna_270615.csv')
df_cesena = pd.read_csv('./resource/cesena_270615.csv')
df_faenza = pd.read_csv('./resource/faenza_270615.csv')
df_ferrara = pd.read_csv('./resource/ferrara_270615.csv')
df_mantova = pd.read_csv('./resource/mantova_270615.csv')
df_milano = pd.read_csv('./resource/milano_270615.csv')
df_piacenza = pd.read_csv('./resource/piacenza_270615.csv')
df_ravenna = pd.read_csv('./resource/ravenna_270615.csv')
df_torino = pd.read_csv('./resource/torino_270615.csv')

df_milano.info()
print(df_milano.head().to_string())


y1 = df_milano['temp']
x1 = df_milano['day']

def max_temp():
    # 把日期数据转换成 datetime 的格式
    day_milano = [parser.parse(x) for x in x1]
    print(day_milano)

    # 调用 subplot 函数, fig 是图像对象，ax 是坐标轴对象
    fig, ax = plt.subplots()


    # 调整x轴坐标刻度，使其旋转70度，方便查看
    plt.xticks(rotation=70)


    # 设定时间的格式
    hours = dates.DateFormatter('%H:%M')
    print(hours)

    # 设定X轴显示的格式
    ax.xaxis.set_major_formatter(hours)

    # 画出图像，day_milano是X轴数据，y1是Y轴数据，‘r’代表的是'red' 红色
    ax.plot(day_milano ,y1, 'r')


    # 显示图像
    # fig
    # plt.show()


def temperate():
    # 读取温度和日期数据
    y1 = df_ravenna['temp']
    x1 = df_ravenna['day']
    y2 = df_faenza['temp']
    x2 = df_faenza['day']
    y3 = df_cesena['temp']
    x3 = df_cesena['day']
    y4 = df_milano['temp']
    x4 = df_milano['day']
    y5 = df_asti['temp']
    x5 = df_asti['day']
    y6 = df_torino['temp']
    x6 = df_torino['day']

    # 把日期从 string 类型转化为标准的 datetime 类型
    day_ravenna = [parser.parse(x) for x in x1]
    day_faenza = [parser.parse(x) for x in x2]
    day_cesena = [parser.parse(x) for x in x3]
    dat_milano = [parser.parse(x) for x in x4]
    day_asti = [parser.parse(x) for x in x5]
    day_torino = [parser.parse(x) for x in x6]


    # 调用 subplots() 函数，重新定义 fig, ax 变量
    fig, ax = plt.subplots()

    plt.xticks(rotation=70)

    hours = dates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(hours)

    # 这里需要画出三根线，所以需要三组参数， 'g'代表'green'
    ax.plot(day_ravenna, y1, 'r', day_faenza, y2, 'r', day_cesena, y3, 'r')
    ax.plot(dat_milano, y4, 'g', day_asti, y5, 'g', day_torino, y6, 'g')
    # fig
    plt.show()

def line_temp():
    dist = [df_ravenna['dist'][0],
            df_cesena['dist'][0],
            df_faenza['dist'][0],
            df_ferrara['dist'][0],
            df_bologna['dist'][0],
            df_mantova['dist'][0],
            df_piacenza['dist'][0],
            df_milano['dist'][0],
            df_asti['dist'][0],
            df_torino['dist'][0]
            ]

    # temp_max 是一个存放每个城市最高温度的列表
    temp_max = [df_ravenna['temp'].max(),
                df_cesena['temp'].max(),
                df_faenza['temp'].max(),
                df_ferrara['temp'].max(),
                df_bologna['temp'].max(),
                df_mantova['temp'].max(),
                df_piacenza['temp'].max(),
                df_milano['temp'].max(),
                df_asti['temp'].max(),
                df_torino['temp'].max()
                ]

    # temp_min 是一个存放每个城市最低温度的列表
    temp_min = [df_ravenna['temp'].min(),
                df_cesena['temp'].min(),
                df_faenza['temp'].min(),
                df_ferrara['temp'].min(),
                df_bologna['temp'].min(),
                df_mantova['temp'].min(),
                df_piacenza['temp'].min(),
                df_milano['temp'].min(),
                df_asti['temp'].min(),
                df_torino['temp'].min()
                ]

    fig, ax = plt.subplots()

    ax.plot(dist, temp_max, 'ro')

    # fig
    plt.show()

    # dist1是靠近海的城市集合，dist2是远离海洋的城市集合
    dist1 = dist[0:5]
    dist2 = dist[5:10]

    # 改变列表的结构，dist1现在是5个列表的集合
    # 之后我们会看到 numpy 中 reshape() 函数也有同样的作用
    dist1 = [[x] for x in dist1]
    dist2 = [[x] for x in dist2]

    # temp_max1 是 dist1 中城市的对应最高温度
    temp_max1 = temp_max[0:5]
    # temp_max2 是 dist2 中城市的对应最高温度
    temp_max2 = temp_max[5:10]

    # 我们调用SVR函数，在参数中规定了使用线性的拟合函数
    # 并且把 C 设为1000来尽量拟合数据（因为不需要精确预测不用担心过拟合）
    svr_lin1 = SVR(kernel='linear', C=1e3)
    svr_lin2 = SVR(kernel='linear', C=1e3)

    # 加入数据，进行拟合（这一步可能会跑很久，大概10多分钟，休息一下:) ）
    svr_lin1.fit(dist1, temp_max1)
    svr_lin2.fit(dist2, temp_max2)

    # 关于 reshape 函数请看代码后面的详细讨论
    xp1 = np.arange(10, 100, 10).reshape((9, 1))
    xp2 = np.arange(50, 400, 50).reshape((7, 1))
    yp1 = svr_lin1.predict(xp1)
    yp2 = svr_lin2.predict(xp2)

    # 限制了 x 轴的取值范围
    ax.set_xlim(0, 400)

    # 画出图像
    ax.plot(xp1, yp1, c='b', label='Strong sea effect')
    ax.plot(xp2, yp2, c='g', label='Light sea effect')
    fig
    plt.show()

line_temp()