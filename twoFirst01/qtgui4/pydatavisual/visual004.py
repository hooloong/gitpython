__author__ = 'hoo'
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_excel("first.xlsx","Sheet1")
var = df.groupby('Gender').Sales.sum()
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
var.plot(kind='bar')
plt.show()