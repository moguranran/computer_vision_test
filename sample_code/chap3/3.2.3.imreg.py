#!/usr/bin/python
# -*- coding: utf-8 -*-

import imregistration 

# 制御点を読み込む
xmlFileName = 'jkfaces2008_small/jkfaces.xml' 
points = imregistration.read_points_from_xml(xmlFileName) 

# 位置合わせする
imregistration.rigid_alignment(points,'jkfaces2008_small/')
