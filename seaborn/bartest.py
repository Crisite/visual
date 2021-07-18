
# 数据准备
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


a = np.random.randn(100) #随机生成1000个[0,1)之间的数据
# s = pd.Series(a) #转换数据
x =np.arange(8)
y = np.array([1,5,3,6,2,4,5,6])
df = pd.DataFrame({"x-axis": x,"y-axis": y})

# 用 Matplotlib 画直方图
# plt.hist(s) #绘制直方图
# plt.show() #展示图表

# 用 Seaborn 画直方图
# sns.distplot(s, kde=False) #不使用密度函数
# plt.show() #展示图表

# sns.distplot(s, kde=True) #使用密度函数
sns.barplot("x-axis","y-axis",palette="RdBu_r",data=df)
plt.xticks(rotation=90)
plt.show() #展示图表