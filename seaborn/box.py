import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 数据准备
# 生成 0-1 之间的 10*4 维度数据
data=np.random.normal(size=(10,4))
lables = ['A','B','C','D'] #标签数据

# 用 Matplotlib 画箱线图
plt.boxplot(data,labels=lables)
plt.show() #展示图表
# 用 Seaborn 画箱线图
df = pd.DataFrame(data, columns=lables)
sns.boxplot(data=df)
plt.show() #展示图表