import pandas as pd
from pyecharts.charts import ThemeRiver
from pyecharts import options as opts

df = pd.read_csv('./resource/sale_amount.csv',index_col='date')
series = df.columns.values
# print(series)
# print(df.head())
data_list = []
for column_name in series:
    for x,y in zip(df[column_name].index,df[column_name].values):
        data_list.append([x,int(y),column_name])
# print(data_list)


rv = (
    ThemeRiver(init_opts=opts.InitOpts(width="900px", height="600px"))
    .add(
        series_name=series,
        data=data_list,
        singleaxis_opts=opts.SingleAxisOpts(type_='time')
         )
    .render('./reasult/rivertest.html')
)