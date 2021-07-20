from matplotlib import pyplot as plt
import seaborn as sns

x = ['Cat1', 'Cat2', 'Cat3', 'Cat4', 'Cat5']
y = [5, 4, 8, 12, 7]
# 用 Matplotlib 画条形图
plt.bar(x, y)
plt.show() #展示图表
# 用 Seaborn 画条形图
sns.barplot(x, y)
plt.show() #展示图表