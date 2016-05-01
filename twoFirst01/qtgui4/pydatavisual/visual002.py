__author__ = 'hoo'
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_excel("first.xlsx","Sheet1")
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.boxplot(df['Age'])
plt.show()