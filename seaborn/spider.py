import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl

labels = np.array([" 推进 ", "KDA", " 生存 ", " 团战 ", " 发育 ", " 输出 "])
stats = [83, 61, 95, 67, 76, 88]
# 画图数据准备，角度、状态值
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)  # 数据准备
stats = np.concatenate((stats, [stats[0]]))  # 数值聚合
angles = np.concatenate((angles, [angles[0]]))  # 角度聚合

# 用 Matplotlib 画蜘蛛图
fig = plt.figure()  # 新建画布
ax = fig.add_subplot(111, polar=True)  # 创建极坐标
ax.plot(angles, stats, 'o-', linewidth=2)  # 绘制空心圆直线
ax.fill(angles, stats, alpha=0.25)  # 填充数据
ax.set_thetagrids(angles * 180 / np.pi, labels)  # 绘制网格线
plt.show()  # 显示图表
