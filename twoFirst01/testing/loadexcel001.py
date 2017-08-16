__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

datalut = pd.read_excel('sx7b_2dd_v2.xlsx','2DD_MLUT',index_col=None, na_values=['NA'])

print datalut.index
print datalut.columns
print datalut.values
print datalut.values[10][2]
print type(datalut)