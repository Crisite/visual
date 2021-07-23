import numpy as np
import pandas as pd
from dateutil import parser
from matplotlib import pyplot as plt
from matplotlib import dates
from scipy.optimize import fsolve
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
    ax.plot(day_milano, y1, 'r')

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
# plt.show()

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

# plt.savefig('./line_temp.png')
# cv2.imwrite('./new_img.jpg', img)  # 利用cv2.imwrite（）保存图像
# plt.imsave('./line_temp.png', format='png')  # 对于校正通道后的图像，需要利用plt.imsave()保存
# plt.show()

print(svr_lin1.coef_)  # 斜率
print(svr_lin1.intercept_)  # 截距
print(svr_lin2.coef_)
print(svr_lin2.intercept_)


# 定义两条拟合直线
def line1(x):
    a1 = svr_lin1.coef_[0][0]
    b1 = svr_lin1.intercept_[0]
    return a1 * x + b1


def line2(x):
    a2 = svr_lin2.coef_[0][0]
    b2 = svr_lin2.intercept_[0]
    return a2 * x + b2


# 定义找到两条直线交点的x的坐标函数
# fsolve(func(x), x0) fsolve求解func(x)=0时x的值，其中x0为初始值，若求解的x有多个值，寻找接近x0的值。
def findIntersection(fun1, fun2, x0):
    return fsolve(lambda x: fun1(x) - fun2(x), x0)


result = findIntersection(line1, line2, 0.0)
# 格式符%d 返回十进制整数
print("[x,y] = [%d, %d]" % (result, line1(result)))
# x = [0,10,20,...,300]
x = np.linspace(0, 300, 31)
plt.plot(x, line1(x), x, line2(x), result, line1(result), 'ro')
plt.savefig('./line_two.png')

# 规定x轴和y轴取值范围
plt.axis((0, 400, 15, 25))
plt.plot(dist, temp_min, 'bo')

# 选取离海最近的三个城市湿度数据和离海最远的三个城市湿度数据对比
# 读取湿度数据
y1 = df_ravenna['humidity']
x1 = df_ravenna['day']
y2 = df_faenza['humidity']
x2 = df_faenza['day']
y3 = df_cesena['humidity']
x3 = df_cesena['day']
y4 = df_milano['humidity']
x4 = df_milano['day']
y5 = df_asti['humidity']
x5 = df_asti['day']
y6 = df_torino['humidity']
x6 = df_torino['day']

# 重新定义fig, ax
fig, ax = plt.subplots()
plt.xticks(rotation=70)

# parse时间数据
# 将时间从str类型转换为标准datetime类型
day_ravenna = [parser.parse(x) for x in x1]
day_faenza = [parser.parse(x) for x in x2]
day_cesena = [parser.parse(x) for x in x3]
day_milano = [parser.parse(x) for x in x4]
day_asti = [parser.parse(x) for x in x5]
day_torino = [parser.parse(x) for x in x6]

# 设置坐标轴中时间显示格式为时：分（Y,m,d,H,M,S)(年月日时分秒)
hours = dates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(hours)

# 作图
ax.plot(day_ravenna, y1, 'r', day_faenza, y2, 'r', day_cesena, y3, 'r')
ax.plot(day_milano, y4, 'g', day_asti, y5, 'g', day_torino, y6, 'g')

plt.savefig('./line_three.png')
plt.show()

# 最大湿度与距离关系
hum_max = [
    df_ravenna['humidity'].max(),
    df_cesena['humidity'].max(),
    df_faenza['humidity'].max(),
    df_ferrara['humidity'].max(),
    df_bologna['humidity'].max(),
    df_mantova['humidity'].max(),
    df_piacenza['humidity'].max(),
    df_milano['humidity'].max(),
    df_asti['humidity'].max(),
    df_torino['humidity'].max()
]
plt.plot(dist, hum_max, 'bo')
plt.savefig('./scatter_max.png')
plt.show()

# 最小湿度与距离关系
hum_min = [
    df_ravenna['humidity'].min(),
    df_cesena['humidity'].min(),
    df_faenza['humidity'].min(),
    df_ferrara['humidity'].min(),
    df_bologna['humidity'].min(),
    df_mantova['humidity'].min(),
    df_piacenza['humidity'].min(),
    df_milano['humidity'].min(),
    df_asti['humidity'].min(),
    df_torino['humidity'].min()
]
plt.plot(dist, hum_min, 'bo')
plt.savefig('./scatter_min.png')
plt.show()

# 绘制极区图
hist, bins = np.histogram(df_ravenna['wind_deg'], 8, [0, 360])
print(hist)
print(bins)

N = 8
# 数据角度
theta = np.arange(0. + np.pi / 8, 2 * np.pi + np.pi / 8, 2 * np.pi / 8)
# 数据极径
radii = np.array(hist)
# 绘制极区图坐标系,此处的[0,0,1,1]为极坐标图所在位置下面坐标limit[xmin,ymin,xmax,ymax]
plt.axes([0, 0, 1, 1], polar=True)
# 定义每个扇区的RGB值（R,G,B），x越大，对应的颜色越接近蓝色
colors = [(1 - x / max(hist), 1 - x / max(hist), 0.75) for x in radii]
plt.bar(theta, radii, width=(2 * np.pi / N), bottom=0.0, color=colors)
plt.title("Ravenna", x=0.2, fontsize=20)

plt.savefig('./hist_ravenna.png')
plt.show()


def showRoseWind(values, city_name, max_value, file_name):
    N = 8
    theta = np.arange(0. + np.pi / 8, 2 * np.pi + np.pi / 8, 2 * np.pi / 8)
    # 数据极径
    radii = np.array(values)
    # 绘制极区图坐标系
    plt.axes([0, 0, 1, 1], polar=True)
    # 定义每个扇区的RGB值（R,G,B），x越大，对应的颜色越接近蓝色
    colors = [(1 - x / max_value, 1 - x / max_value, 0.75) for x in radii]
    plt.bar(theta, radii, width=(2 * np.pi / N), bottom=0.0, color=colors)
    plt.title(city_name, x=0.2, fontsize=20)
    plt.savefig('./{name}.png'.format(name=file_name))
    plt.show()


showRoseWind(hist, "Ravenna", max(hist), 'Renatest_rose')

# 查看都灵Torino风向
hist, bin = np.histogram(df_torino['wind_deg'], 8, [0, 360])
print(hist)
showRoseWind(hist, 'Torino', max(hist), 'Torino_rose')


# def RoseWind_Speed(df_city):
#     # degs = [45, 90, ..., 360]
#     degs = np.arange(45, 361, 45)
#     tmp = []
#     for deg in degs:
#         # 获取 wind_deg 在指定范围的风速平均值数据
#         tmp.append(df_city[(df_city['wind_deg'] > (deg - 46)) & (df_city['wind_deg'] < deg)]
#                    ['wind_speed'].mean())
#     return np.array(tmp)
#
#
# showRoseWind(RoseWind_Speed(df_ravenna), 'Ravenna', max(hist), 'Ravenna_windspeed')
