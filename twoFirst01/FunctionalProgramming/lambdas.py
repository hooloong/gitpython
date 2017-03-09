from __future__ import print_function
__author__ = 'hooloongge'
# -*- coding: utf-8 -*-
import sys, random,string,struct,json
import numpy as np
import csv

def my_func(f,arg):
    return f(arg)

print (my_func(lambda x:2*x*x,5))

print ((lambda x:x**2+5*x+4)(-4))

double = lambda x:x*2
print (double(2))

def add_five(x):
    return x+5
nums = [11,22,33,44,55]

result = list(map(add_five,nums))

print(result)
resultx = list(map(lambda x:x+5,nums))
print (resultx)

res = list(filter(lambda x:x%2 == 0,nums))
print(res)

