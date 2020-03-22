from PIL import Image
import imtools
from numpy import *

filelist = imtools.get_imlist(".")
print(len(filelist))

im = array(Image.open("data\AquaTermi_lowcontrast.JPG").convert("L"))
im2, cdf = imtools.histeq(im)

from pylab import *

for i in (im, im2):
  figure()
  gray()
  axis('off')
  imshow(i)

  figure()
  hist(i.flatten(),128)

figure()
plot(cdf)
show()