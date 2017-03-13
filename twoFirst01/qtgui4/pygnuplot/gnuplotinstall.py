#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
source = 'https://raw.github.com/baijian/bootstrap.py/1.0/bootstrap.py'
target = '%s/bootstrap.py' % os.path.dirname(os.path.abspath(__file__))

if not os.path.isfile(target):
    os.system('wget %s -O %s' % (source, target))

from bootstrap import bootstrap, ve

bootstrap(os.path.dirname(os.path.abspath(__file__)) + '/..')

#ve('pip install numpy==1.7.1')
ve('pip install gnuplot-py==1.8')