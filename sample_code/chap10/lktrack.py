#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
import cv2

# 定数と、デフォルトのパラメータ
lk_params = dict(winSize=(15,15),maxLevel=2,
  criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,0.03))

subpix_params = dict(zeroZone=(-1,-1),winSize=(10,10),
  criteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS,20,0.03))

feature_params = dict(maxCorners=500,qualityLevel=0.01,minDistance=10)

class LKTracker(object):
  """ ピラミッド型Lucas-Kanade法でオプティティルフローを
      計算するクラス """

  def __init__(self,imnames):
    """ 画像名のリストを用いて初期化する """

    self.imnames = imnames
    self.features = []
    self.tracks = []
    self.current_frame = 0

  def detect_points(self):
    """ 現在フレームの「追跡に適する特徴点」（コーナー）を
      サブピクセル精度で検出する """

    # 画像を読み込みグレースケール版を作る
    self.image = cv2.imread(self.imnames[self.current_frame])
    self.gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)

    # 特徴点を見つける
    features = cv2.goodFeaturesToTrack(self.gray, **feature_params)

    # コーナー点の座標を改善する
    cv2.cornerSubPix(self.gray,features, **subpix_params)
    self.features = features
    self.tracks = [[p] for p in features.reshape((-1,2))]
    self.prev_gray = self.gray

  def track_points(self):
    """ 検出した特徴点を追跡する """

    if self.features != []:
      self.step() # 次のフレームに移る

      # 画像を読み込みグレースケール版を作成する
      self.image = cv2.imread(self.imnames[self.current_frame])
      self.gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)

      # 入力フォーマットに合うように変換する
      tmp = float32(self.features).reshape(-1, 1, 2)

      # オプティカルフローを計算する
      features,status,track_error = cv2.calcOpticalFlowPyrLK(self.prev_gray,
                                      self.gray,tmp,None,**lk_params)

      # 消失した点を削除する
      self.features = [p for (st,p) in zip(status,features) if st]

      # 消失した点の追跡を消去する
      features = array(features).reshape((-1,2))
      for i,f in enumerate(features):
        self.tracks[i].append(f)
      ndx = [i for (i,st) in enumerate(status) if not st]
      ndx.reverse() # 後ろから削除する
      for i in ndx:
        self.tracks.pop(i)

      self.prev_gray = self.gray

  def step(self,framenbr=None):
    """ 他のフレームに移る。引数がなければ次のフレームに移る """

    if framenbr is None:
      self.current_frame = (self.current_frame + 1) % len(self.imnames)
    else:
      self.current_frame = framenbr % len(self.imnames)

  def draw(self):
    """ OpenCVの描画関数を使って、現在の画像に点を描画する。
      何かキーを押すと、ウィンドウを閉じる """

    # 緑の円で特徴点を描画する
    for point in self.features:
      cv2.circle(self.image,(int(point[0][0]),int(point[0][1])),3,(0,255,0),-1)

    cv2.imshow('LKtrack',self.image)
    cv2.waitKey()

  def track(self):
    """ シーケンスを順番に返すジェネレータ """

    for i in range(len(self.imnames)):
      if self.features == []:
        self.detect_points()
      else:
        self.track_points()

    # RGBでコピーを作成する
    f = array(self.features).reshape(-1,2)
    im = cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
    yield im,f
