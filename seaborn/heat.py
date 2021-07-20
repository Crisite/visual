import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

flights = pd.read_csv("flights.csv") #读取数据
data=flights.pivot('year','month','passengers') #转换数据

sns.heatmap(data)
plt.show()