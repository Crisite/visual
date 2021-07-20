import pandas as pd

df = pd.read_csv('./resource/sale_amount.csv')
df.info()
print(df.head().to_string())