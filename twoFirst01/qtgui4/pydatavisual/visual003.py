import seaborn as sns
# -*- coding: utf-8 -*-

import pandas as pd
df = pd.read_excel("first.xlsx","Sheet1")

sns.violinplot(df['Age'],df['Gender'])

sns.despine()