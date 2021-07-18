import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

N = 1000
x = np.random.randn(N)
y = np.random.randn(N)

# matplotlib
plt.scatter(x, y,marker='<')
plt.show()

# Seaborn
df = pd.DataFrame( {'x':x,'y':y} )
sns.jointplot(
            x= "x",
            y= "y",
            data = df ,
            kind = 'scatter'
            )
plt.show()