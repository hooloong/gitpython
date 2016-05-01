__author__ = 'hoo'
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_excel("first.xlsx","Sheet1")

var = df.groupby('Gender').sum().stack()
temp = var.unstack()
type(temp)
x_list = temp['Sales']
label_list = temp.index
plt.axis("equal")

plt.pie(x_list,labels=label_list,autopct="%1.1f%%")
# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# ax.scatter(df['Age'],df['Sales'],s=df['Income'])
plt.title("Pastafarianism expenses")
plt.show()