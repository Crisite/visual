import numpy as np
import pandas as pd
from numpy import random
from pyecharts import options as opts
from pyecharts.charts import Line, Bar, Scatter, Boxplot, Grid

# data_series = [[11, 11, 15, 13, 12, 13, 10],[1, -2, 2, 5, 3, 2, 0]]
# print(data_series)

line = (
    Line()
    .add_xaxis(xaxis_data=['星期一','星期二','星期三','星期四','星期五','星期七','星期日'])
    .add_yaxis(series_name='最高气温/℃', y_axis=[11, 11, 15, 13, 12, 13, 10])
    .add_yaxis(series_name='最低气温/℃', y_axis=[1, -2, 2, 5, 3, 2, 0])
    .set_global_opts(
        yaxis_opts=opts.AxisOpts(type_='value', axislabel_opts=opts.LabelOpts(formatter='{value} ℃')),
        title_opts=opts.TitleOpts(title='折线示意图',pos_top='50%',pos_left="20%"),
        legend_opts=opts.LegendOpts(pos_bottom='25%',pos_left='25%')
    )
)

x_data = ['可乐', '雪碧', '橙汁', '绿茶', '奶茶', '百威', '青岛']
y_data = [100,78, 27, 48, 34, 93,76]

bar = (
    Bar()
    .add_xaxis(xaxis_data=['苹果', '芒果', '猕猴桃', '香蕉', '车厘子'])
    .add_yaxis(
        series_name='bar',
        y_axis=[200,160,120,289,105]
    )
    .set_global_opts(
        yaxis_opts=opts.AxisOpts(type_='value', axislabel_opts=opts.LabelOpts(formatter='{value} 斤')),
        title_opts=opts.TitleOpts(title='柱状图-水果销量',pos_top='top',pos_left="20%"),
        legend_opts=opts.LegendOpts(pos_top='20%',pos_left='40%')
    )
)

scatter = (
    Scatter()
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name='es',
        y_axis=y_data,
        symbol_size=10 # 设置点的大小
    )
    .set_global_opts(
        yaxis_opts=opts.AxisOpts(type_='value', axislabel_opts=opts.LabelOpts(formatter='{value} 份')),
        title_opts=opts.TitleOpts(title='动态散点图示例',pos_top='50%',pos_right="15%"),
        legend_opts=opts.LegendOpts(pos_bottom='25%',pos_right='10%')
    )
)


# columns=['项目A', '项目B', '项目C', '项目D']
# df = np.random.randint(600,1000,size=(4,50))
# print(df)


min_ = 600
max_ = 1000
v1 = [
    [random.randint(min_, max_) for i in range(50)],
    [random.randint(min_, max_) for i in range(50)],
    [random.randint(min_, max_) for i in range(50)],
    [random.randint(min_, max_) for i in range(50)],
]
# print(v1)

c = Boxplot()
x_axis = ['项目A', '项目B', '项目C', '项目D']
# y_axis = boxplot.prepare_data(df)
# print(y_axis)
c.add_xaxis(['项目A', '项目B', '项目C', '项目D'])
c.add_yaxis('数量', c.prepare_data(v1))
# print(c.prepare_data(v1))
# boxplot.add('',x_axis,y_axis)
c.set_global_opts(
        # yaxis_opts=opts.AxisOpts(type_='value', axislabel_opts=opts.LabelOpts(formatter='{value} 斤')),
        title_opts=opts.TitleOpts(title='箱体图',pos_top='%50',pos_right="20%"),
        legend_opts=opts.LegendOpts(pos_top='20%',pos_right='right')
    )
# 比较全的各种图表 https://blog.csdn.net/moonhmilyms/article/details/100512398?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522162685717016780265417357%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=162685717016780265417357&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v29-7-100512398.pc_search_result_control_group&utm_term=pyecharts+grid%E5%88%9D%E5%A7%8B%E5%8C%96&spm=1018.2226.3001.4187

grid = (
    Grid()
    .add(bar,grid_opts=opts.GridOpts(
        pos_left="7%",pos_top="7%",width='35%',height='35%'
    ) )
    .add(c, grid_opts=opts.GridOpts(
        pos_right="7%",pos_top="7%",width='35%',height='35%'
    ))
    .add(line, grid_opts=opts.GridOpts(
        pos_left="7%",pos_bottom="5%",width='35%',height='35%'
    ))
    .add(scatter, grid_opts=opts.GridOpts(
        pos_right="7%",pos_bottom="5%",width='35%',height='35%'
    ))

    .render('./reasult/Gridtest.html')
)
