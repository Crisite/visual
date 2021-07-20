

# 数据准备
from matplotlib import pyplot as plt

nums = [25, 37, 33, 37, 6]
labels = ['High-school','Bachelor','Master','Ph.d', 'Others'] #标签数据

# 用 Matplotlib 画饼图
plt.pie(x = nums, labels=labels) #绘制饼图
plt.show() #展示图表