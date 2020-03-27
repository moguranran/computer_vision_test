import os
from PIL import Image
from numpy import *

def get_imlist(path):
    """pathに指定されたディレクトリの全てのjpgファイル名のリストを返す"""
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]

def imresize(im, sz):
    pil_im = Image.fromarray(uint8(im))
    return array(pil_im.resize(sz))

def histeq(im, nbr_bins=256):
    """グレースケール画像のヒストグラム平坦化"""
    #画像のヒストグラムを得る
    imhist, bins = histogram(im.flatten(), nbr_bins, normed=True)
    cdf = imhist.cumsum() #累積分布関数
    cdf = 255 * cdf / cdf[-1] #正規化

    #cdfを線形補完し、新しいピクセル値とする
    im2 = interp(im.flatten(), bins[:-1], cdf)

    return im2.reshape(im.shape), cdf

def compute_average(imlist):
    """画像の平均を求める"""
    #最初の画像を開き、浮動小数点の配列に変換する
    averageim = array(Image.open(imlist[0]), "f")

    for imname in imlist[1:]:
        try:
            averageim += array(Image.open(imname))
        except:
            print(f"{imname}...skipped")
    
    averageim /= len(imlist)

    #平均を uint8 に変換する
    return array(averageim, "uint8")