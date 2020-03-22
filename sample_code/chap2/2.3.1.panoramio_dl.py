#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib, urlparse 
import simplejson as json 

# 画像を問い合わせる
url = 'http://www.panoramio.com/map/get_panoramas.php?order=popularity&\
set=public&from=0&to=20&minx=-77.037564&miny=38.896662&\
maxx=-77.035564&maxy=38.898662&size=medium'
c = urllib.urlopen(url)

# JSONから各画像のURLを取り出す
j = json.loads(c.read())
imurls = []
for im in j['photos']:
  imurls.append(im['photo_file_url'])

# 画像をダウンロードする
for url in imurls:
  image = urllib.URLopener()
  image.retrieve(url, 'panoramio/' + os.path.basename(urlparse.urlparse(url).path))
  print 'downloading:', url
