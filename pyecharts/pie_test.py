from pyecharts.charts import Pie
from pyecharts import options as opts

# 内部
inner_x_data = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋"]
inner_y_data = [11, 12, 13, 10, 10]
inner_pair_data = [list(z) for z in zip(inner_x_data, inner_y_data)]

# 外部
outter_x_data = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋"]
outter_y_data = [19, 21, 32, 20, 33]
outter_pair_data = [list(z) for z in zip(outter_x_data, outter_y_data)]

# pie.add()
# add(name, attr, value,
#     radius=None,
#     center=None,
#     rosetype=None, **kwargs)
# name -> str 图例名称
# attr -> list 属性名称
# value -> list 属性所对应的值
# radius -> list
# 饼图的半径，数组的第一项是内半径，第二项是外半径，默认为 [0, 75]
# 默认设置成百分比，相对于容器高宽中较小的一项的一半
# center -> list
# 饼图的中心（圆心）坐标，数组的第一项是横坐标，第二项是纵坐标，默认为 [50, 50]
# 默认设置成百分比，设置成百分比时第一项是相对于容器宽度，第二项是相对于容器高度
# rosetype -> str
# 是否展示成南丁格尔图，通过半径区分数据大小，有'radius'和'area'两种模式。默认为'radius'
# radius：扇区圆心角展现数据的百分比，半径展现数据的大小
# area：所有扇区圆心角相同，仅通过半径展现数据大小

pie =(
    # 初始化
    Pie()
    .add(
        '',
        outter_pair_data,
        radius=['50%','80%'],
        center=['50%', '50%']
         )
    # .set_global_opts(title_opts=opts.TitleOpts(title="Pie-示例图外圈"))

    # 内圈玫瑰图

    .add(
        '',
        inner_pair_data,
        radius=['10%','45%'],
        center=['50%', '50%'],
        rosetype='radius'
         )

    # 配置项可参考教程 https://blog.csdn.net/qq_43527959/article/details/110872389

    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="Pie-示例图外圈",
            pos_left='center',
            # pos_top= '10%'
            ),
        # 图例配置项 LegendOpts
        # 参考资料 https://blog.csdn.net/qq_42374697/article/details/105630669
        legend_opts=opts.LegendOpts(
            is_show= True,
            pos_left='left',
            pos_bottom='20%',
            orient='vertical' # 图例布局朝向('horizontal' / 'vertical')
        )
    )


)
pie.render('./reasult/pietest.html')