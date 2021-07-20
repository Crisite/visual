import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

x = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
y = [5, 3, 6, 20, 17, 16, 19, 30, 32, 35]

# 使用 Matplotlib 画折线图
plt.plot(x, y) #直接使用数组数据
plt.show() #展示图表

# 使用 Seaborn 画折线图
df = pd.DataFrame({'x': x, 'y': y})  # 转换数据
sns.lineplot(x="x", y="y", data=df)  # 绘制折线图
plt.show()  # 展示图表
