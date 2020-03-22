#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
pil_im = Image.open('empire.jpg').convert('L')
pil_im.show()

pil_im.thumbnail((128,128))
pil_im.show()

pil_im = Image.open('empire.jpg').convert('L')
box = (100,100,400,400)
region = pil_im.crop(box)
region = region.transpose(Image.ROTATE_180)
pil_im.paste(region,box)
pil_im.show()

pil_im = Image.open('empire.jpg').convert('L')
out = pil_im.resize((128,128))
out.show()

pil_im = Image.open('empire.jpg').convert('L')
out = pil_im.rotate(45)
out.show()


