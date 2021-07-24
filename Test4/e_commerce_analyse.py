import pandas as pd
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Line, Funnel, Bar
from pyecharts.charts import Grid

user=pd.read_csv('./resource/tianchi_fresh_comp_train_user.csv')

user.info()

user.isnull().sum()
user.drop_duplicates(keep='last',inplace=True)

user['time']=pd.to_datetime(user['time'])
user['dates'] = user.time.dt.date
user['month'] = user.dates.values.astype('datetime64[M]')
user['hours'] = user.time.dt.hour
user['behavior_type']=user['behavior_type'].apply(str)
user['user_id']=user['user_id'].apply(str)
user['item_id']=user['item_id'].apply(str)

pv_day=user[user.behavior_type=="1"].groupby("dates")["behavior_type"].count()
uv_day=user[user.behavior_type=="1"].drop_duplicates(["user_id","dates"]).groupby("dates")['user_id'].count()

attr=list(pv_day.index)
pv = (
    Line(init_opts=opts.InitOpts(width="1000px", height="500px"))
    .add_xaxis(xaxis_data=attr)
    .add_yaxis(
        "pv",
        np.around(pv_day.values / 10000, decimals=2),
        label_opts=opts.LabelOpts(is_show=False),
    )

    .add_yaxis(
        series_name="uv",
        yaxis_index=1,
        y_axis=np.around(uv_day.values / 10000, decimals=2),
        label_opts=opts.LabelOpts(is_show=False),
    )

    .extend_axis(
        yaxis=opts.AxisOpts(
            name="uv",
            type_="value",
            min_=0,
            max_=0.16,
            interval=0.4,
            axislabel_opts=opts.LabelOpts(formatter="{value} 万人"),
        )
    )
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger="axis", axis_pointer_type="cross"
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
        ),
        yaxis_opts=opts.AxisOpts(
            name="pv",
            type_="value",
            min_=0,
            max_=10,
            interval=20,
            axislabel_opts=opts.LabelOpts(formatter="{value} 万次"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        title_opts=opts.TitleOpts(title="pv与uv趋势图"),

    )
)
pv.render('./reasult/chart1.html')




pv_uv = pd.concat([pv_day,uv_day],join='outer', axis=1)
pv_uv.columns = ['pv_day','uv_day']
new_day=pv_uv.diff()
new_day.columns=['new_pv','new_uv']


attr = new_day.index
v = new_day.new_uv
w = new_day.new_pv

li=(
    Line(init_opts=opts.InitOpts(width="1000px" , height="500px"))
    .add_xaxis(xaxis_data=attr)
    .add_yaxis(
        "新增pv",
        w,
        label_opts=opts.LabelOpts(is_show=False)
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
        name="新增uv",
        type_="value",
        min_=-2000,
        max_=1600,
        interval=400,
        axislabel_opts=opts.LabelOpts(formatter="{value}"),
        )
    )
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            is_show=True,trigger="axis", axis_pointer_type="cross"
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
        ),
        yaxis_opts=opts.AxisOpts(
            name="新增pv",
            type_="value",
            min_=-350000,
            max_=250000,
            interval=100000,
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        title_opts=opts.TitleOpts(title="pv、uv差异分析"),
     )
)
il=(
    Line()
    .add_xaxis(xaxis_data=attr)
    .add_yaxis("新增uv" ,v, yaxis_index='1', label_opts=opts.LabelOpts(is_show=False),)
)
c=li.overlap(il)
c.render('./reasult/chart2.html')


shopping_cart= user[user.behavior_type == '3'].groupby('dates')['behavior_type'].count()
collect=user[user.behavior_type=='2'].groupby('dates')['behavior_type'].count()
buy=user[user.behavior_type=='4'].groupby('dates')['behavior_type'].count()

attr_a=list(shopping_cart.index)
v_1=shopping_cart.values.tolist()
v_2=collect.values.tolist()
v_3=buy.values.tolist()

b=(
    Line()
    .add_xaxis(xaxis_data=attr_a)
    .add_yaxis(
        "加购人数",
        v_1,
        label_opts=opts.LabelOpts(is_show=False)
    )
    .add_yaxis(
        "收藏人数",
        v_2,
        label_opts=opts.LabelOpts(is_show=False)
    )
    .add_yaxis(
        "购买人数",
        v_3,
        label_opts=opts.LabelOpts(is_show=False)
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="不同时期用户行为数据"))
)
b.render('./reasult/chart3.html')



user['dates']=pd.to_datetime(user['dates'])
active=user[user["dates"].isin(["2014/12/11","2014/12/12","2014/12/13"])]
daily=user[~user["dates"].isin(["2014/12/11","2014/12/12","2014/12/13"])]

# 活动数据
cart_h=active[active.behavior_type == '3'].groupby('hours')['behavior_type'].count()
collect_h=active[active.behavior_type=='2'].groupby('hours')['behavior_type'].count()
buy_h=active[active.behavior_type=='4'].groupby('hours')['behavior_type'].count()
uv_h=active[active.behavior_type== '1'].groupby('hours')['user_id'].count()

attr_h=list(cart_h.index)
h1=np.around(cart_h.values/3,decimals=0).tolist()
h2=np.around(collect_h.values/3,decimals=0).tolist()
h3=np.around(buy_h.values/3,decimals=0).tolist()
h4=np.around(uv_h.values/3,decimals=0).tolist()


h=(
    Line(init_opts=opts.InitOpts(width="1000px",height="500px"))
    .add_xaxis(xaxis_data=attr_h)
    .add_yaxis(
        "加购人数",
        h1,
        label_opts=opts.LabelOpts(is_show=False)
    )
    .add_yaxis(
        "收藏人数",
        h2,
        label_opts=opts.LabelOpts(is_show=False)
    )
    .add_yaxis(
        "购买人数",
        h3,
        label_opts=opts.LabelOpts(is_show=False)
    )
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=15)),
        title_opts=opts.TitleOpts(title="日均各时段活动用户行为",pos_top="48%"),
        legend_opts=opts.LegendOpts(pos_top="48%"),
    )
)
bar=(
    Bar()
    .add_xaxis(xaxis_data=attr_h)
    .add_yaxis(
    "浏览人数",
        h4,
        label_opts=opts.LabelOpts(is_show=False)
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="活动pv对比数据"),
    )
)

ggrid = (
    Grid()
    .add(bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
    .add(h, grid_opts=opts.GridOpts(pos_top="60%"))
)
ggrid.render('./reasult/chart4_grid.html')

cart_d= daily[daily.behavior_type == '3'].groupby('hours')['behavior_type'].count()
collect_d=daily[daily.behavior_type=='2'].groupby('hours')['behavior_type'].count()
buy_d=daily[daily.behavior_type=='4'].groupby('hours')['behavior_type'].count()
uv_d=daily[daily.behavior_type== '1'].groupby('hours')['user_id'].count()

attr_d=list(cart_d.index)
d1=np.around(cart_d.values/28,decimals=0).tolist()
d2=np.around(collect_d.values/28,decimals=0).tolist()
d3=np.around(buy_d.values/28,decimals=0).tolist()
d4=np.around(uv_d.values/3,decimals=0).tolist()

d=(
    Line(init_opts=opts.InitOpts(width="1000px",height="500px"))
    .add_xaxis(xaxis_data=attr_d)
    .add_yaxis(
        "加购人数",
        d1,
        label_opts=opts.LabelOpts(is_show=False)
    )
    .add_yaxis(
        "收藏人数",
        d2,
        label_opts=opts.LabelOpts(is_show=False)
    )
    .add_yaxis(
        "购买人数",
        d3,
        label_opts=opts.LabelOpts(is_show=False)
    )
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=15)),
        title_opts=opts.TitleOpts(title="日均各时段活动用户行为",pos_top="48%"),
        legend_opts=opts.LegendOpts(pos_top="48%"),
    )
)
y=(
    Bar()
    .add_xaxis(xaxis_data=attr_d)
    .add_yaxis(
    "浏览人数",
        d4,
        label_opts=opts.LabelOpts(is_show=False)
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="日常pv对比数据"),
    )
)

ggrid = (
    Grid()
    .add(y, grid_opts=opts.GridOpts(pos_bottom="60%"))
    .add(d, grid_opts=opts.GridOpts(pos_top="60%"))
)
ggrid.render('./reasult/chart5_grid.html')


# 活动时购买率
hour_buy_user_num = active[active.behavior_type == '4'].drop_duplicates(['user_id','dates', 'hours']).groupby('hours')['user_id'].count()
hour_active_user_num = active.drop_duplicates(['user_id','dates', 'hours']).groupby('hours')['user_id'].count()
hour_buy_rate = hour_buy_user_num / hour_active_user_num
attr_o = list(hour_buy_user_num.index)
vo_2 =np.around(hour_buy_rate.values,decimals=2)
# 日常时购买率
hour_buy_daily_num = daily[daily.behavior_type == '4'].drop_duplicates(['user_id','dates', 'hours']).groupby('hours')['user_id'].count()
hour_active_daily_num = daily.drop_duplicates(['user_id','dates', 'hours']).groupby('hours')['user_id'].count()
daily_buy_rate = hour_buy_daily_num / hour_active_daily_num
vi_2 =np.around(daily_buy_rate.values,decimals=2)

hbu=(
    Line()
    .add_xaxis(xaxis_data=attr_o)
    .add_yaxis(
        "日常购买率",
        vi_2,
    )
    .add_yaxis(
        "活动购买率",
        vo_2,
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="不同时段购买率"))
)

hbu.render('./reasult/chart6_line.html')

# 活动转化
a_pv=active[active.behavior_type=="1"]["user_id"].count()
a_cart=active[active.behavior_type=="3"]["user_id"].count()
a_collect=active[active.behavior_type=="2"]["user_id"].count()
a_buy=active[active.behavior_type=="4"]["user_id"].count()

a_attr=["点击","加入购物车","收藏","购买"]
values=[np.around((a_pv/a_pv*100),2),
        np.around((a_cart/a_pv*100),2),
        np.around((a_collect/a_pv*100),2),
        np.around((a_buy/a_pv*100),2),
       ]

data = [[a_attr[i], values[i]] for i in range(len(a_attr))]


a=(
    Funnel()
    .add(
        series_name="用户行为",
        data_pair=data,
        gap=2,
        tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%",is_show=True),
        label_opts=opts.LabelOpts(is_show=True, position="ourside"),
        itemstyle_opts=opts.ItemStyleOpts(border_color="#fff", border_width=1),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="用户转化漏斗", subtitle="活动"))
)

a.render("./reasult/chart7_funnel.html")

l_pv=daily[daily.behavior_type=="1"]["user_id"].count()
l_cart=daily[daily.behavior_type=="3"]["user_id"].count()
l_collect=daily[daily.behavior_type=="2"]["user_id"].count()
l_buy=daily[daily.behavior_type=="4"]["user_id"].count()

l_attr=["点击","加入购物车","收藏","购买"]
valuel=[np.around((l_pv/l_pv*100),2),
        np.around((l_cart/l_pv*100),2),
        np.around((l_collect/l_pv*100),2),
        np.around((l_buy/l_pv*100),2),
       ]

datal = [[l_attr[i], valuel[i]] for i in range(len(l_attr))]


dy=(
    Funnel()
    .add(
        series_name="用户行为",
        data_pair=datal,
        gap=2,
        tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%",is_show=True),
        label_opts=opts.LabelOpts(is_show=True, position="ourside"),
        itemstyle_opts=opts.ItemStyleOpts(border_color="#fff", border_width=1),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="用户转化漏斗", subtitle="日常"))
)
dy.render('./reasult/chart8_funner.html')
