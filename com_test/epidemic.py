from datetime import timedelta, date
from pyecharts import options as opts

import pandas as pd
from pyecharts.charts import Timeline, Pie, Map

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
china_epidemic_data['updateDate'] = china_epidemic_data['updateTime'].apply(lambda updatetime:updatetime.date())

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
unique_epidemic_data = china_epidemic_data.drop_duplicates(subset=['provinceName','updateDate'],keep='first')
# print(unique_epident_data.head(1000).to_string())
# unique_epident_data.info()

# 获取所有省份名
provinces = unique_epidemic_data.provinceName.drop_duplicates().tolist()
# print(province)

# 获取所有日期
updateDates = unique_epidemic_data.updateDate.drop_duplicates().tolist()
updateDates.sort()
# print(updateDates)
print('省份个数', len(provinces))
print('记录天数', len(updateDates))
print('原始数据记录数', len((unique_epidemic_data)))

# unique_epidemic_data.info()

def _fill_one_province_day_data(total_data, today_filter_condition, last_day_filter_condition):
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
        today_filter_condition = (unique_epidemic_data['updateDate'] == updateDate) & (
                                    unique_epidemic_data['provinceName'] == province)
        """
        timedelta代表两个datetime之间的时间差
        updateDate - timedelta(days=1) 意指当前天数减一
        如 + timedelta(days = 365)  时则值加365天
        """
        last_day = updateDate - timedelta(days=1)
        last_day_filter_condition = (unique_epidemic_data['updateDate'] == last_day)&(
            unique_epidemic_data['provinceName'] == province)
        if today_filter_condition.any():
            # ValueError: cannot reindex from a duplicate axis 执行函数即出现该错误
            # _fill_one_province_day_data(unique_epidemic_data, today_filter_condition, last_day_filter_condition)
            pass
        else:
            last_province_data = unique_epidemic_data[last_day_filter_condition]
            last_province_data = last_province_data.copy()
            last_province_data['updateDate'] = updateDate
            unique_epidemic_data = pd.concat([unique_epidemic_data, last_province_data])

# unique_epidemic_data.info()

# 计算全国每天的各种病例数量
national_epdimic_data = unique_epidemic_data.groupby('updateDate').agg('sum')
# print(national_epdimic_data)

"""
数据处理完毕，绘制图形
"""

# 创建时间轴，并使其自动播放，1s切换一次
epidemic_percent_time = Timeline()
epidemic_percent_time.add_schema(
    is_auto_play=True,
    play_interval=1000,
    is_timeline_show=False
)

for updateDate in updateDates:
    data = national_epdimic_data.loc[updateDate]
    one_day_data = [
        ['确诊', int(data['province_confirmedCount'])],
        ['疑似', int(data['province_suspectedCount'])],
        ['治愈', int(data['province_curedCount'])],
        ['死亡', int(data['province_deadCount'])]
    ]
    one_day_pie = (
        Pie()
        .add(
            '疫情情况',
            one_day_data,
            rosetype='radius',
            radius=['30%','50%']
        )
        .set_global_opts(title_opts=opts.TitleOpts("{}".format(updateDate)))
        # .render('./reasult/test/{}.html'.format(updateDate))
        )
    epidemic_percent_time.add(one_day_pie, updateDate)




# epidemic_percent_time.render('./reasult/epidemic_Timeline.html')


# map

# 处理数据 将名称匹配
print(type(unique_epidemic_data.provinceName))
print(unique_epidemic_data.provinceName)
# unique_epidemic_data["provinceName"] = unique_epidemic_data['provinceName'].apply(lambda province_name: province_name.apply('省', ''))
# unique_epidemic_data["provinceName"] = unique_epidemic_data.provinceName.apply(lambda province_name: province_name.apply('自治区', ''))
# unique_epidemic_data["provinceName"] = unique_epidemic_data.provinceName.apply(lambda province_name: province_name.apply('市', ''))


epidemic_map_timeline = Timeline()
epidemic_percent_time.add_schema(
    is_auto_play=True,
    play_interval=1000,
    is_timeline_show=False
)
for updateDate in updateDates:
    one_day_map = Map()
    data = unique_epidemic_data[unique_epidemic_data.updateDate == updateDate]
    one_day_data = [province_data for province_data in zip(data.provinceName.tolist(),
                                                           data.province_confirmedCount.tolist())]

    # 绘制单天地图
    one_day_map.add('全国疫情',one_day_data,'china', is_map_symbol_show= False)
    one_day_map.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    one_day_map.set_global_opts(
        title_opts=opts.TitleOpts(title='{}确诊'.format(updateDate)),
        visualmap_opts=opts.VisualMapOpts(max_=1000)
    )
    epidemic_map_timeline.add(one_day_map, updateDate)

epidemic_map_timeline.render('./reasult/epidemic_map.html')





