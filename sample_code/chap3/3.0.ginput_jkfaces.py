
from PIL import Image
from pylab import *
from xml.dom import minidom
import imtools
import os

dir = 'jkfaces2008_small'
imlist = imtools.get_imlist(dir)

with open(dir + '/jkfaces.xml', 'w') as f:
  f.write('<?xml version="1.0" encoding="utf-8"?>\n')
  f.write('<faces>\n')
  for imfile in imlist:
    im = array(Image.open(imfile))
    imshow(im)
    print 'click left, right, mouth'
    x = ginput(3,timeout=0)
    print x
    f.write('<face file="' + os.path.basename(imfile) + '" ')
    f.write('xf="' + str(int(x[0][0])) + '" ')
    f.write('xm="' + str(int(x[2][0])) + '" ')
    f.write('xs="' + str(int(x[1][0])) + '" ')
    f.write('yf="' + str(int(x[0][1])) + '" ')
    f.write('ym="' + str(int(x[2][1])) + '" ')
    f.write('ys="' + str(int(x[1][1])) + '"/>\n')

  f.write('</faces>\n')


  

