#!/usr/bin/python
# -*- coding: utf-8 -*-

from pylab import *
from mpl_toolkits.mplot3d import axes3d

fig = figure()
ax = fig.gca(projection="3d")

# 3Dのサンプルデータを生成する
X,Y,Z = axes3d.get_test_data(0.25)

# 3Dの点を描画する
ax.plot(X.flatten(),Y.flatten(),Z.flatten(),'o')

show()
