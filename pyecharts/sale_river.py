import pandas as pd

df = pd.read_csv('./resource/sale_amount.csv')
df.info()
print(df.head().to_string())
x_data = ['超市A', '超市B', '超市C', '超市D', '超市E']
ya_data = df['超市A']
yb_data = df['超市B']
yc_data = df['超市C']
yd_data = df['超市D']
ye_data = df['超市E']