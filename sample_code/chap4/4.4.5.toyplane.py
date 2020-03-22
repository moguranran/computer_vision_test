#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame, pygame.image
from pygame.locals import *
import pickle

width,height = 1000,747

def set_projection_from_camera(K):
  """ カメラのキャリブレーション行列から表示領域を設定する """ 

  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()

  fx = K[0,0]
  fy = K[1,1]
  fovy = 2*arctan(0.5*height/fy)*180/pi
  aspect = float(width*fy)/(height*fx)

  # 手前と奥のクリッピング平面を定義する
  near = 0.1
  far = 100.0

  # 射影を設定する
  gluPerspective(fovy,aspect,near,far)
  glViewport(0,0,width,height)
  glEnable(GL_DEPTH_TEST)

def set_modelview_from_camera(Rt):
  """ カメラの姿勢からモデルビュー行列を設定する """

  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()

  # ティーポットをX軸の周りに90度回転させ
  # Z軸が上向きになるようにする
  Rx = array([[1,0,0],[0,0,-1],[0,1,0]])

  # 回転を最適な近似にする
  R = Rt[:,:3]
  U,S,V = linalg.svd(R)
  R = dot(U,V)
  R[0,:] = -R[0,:] # X軸の符号を反転する

  # 平行移動を設定する
  t = Rt[:,3]

  # 4*4のモデルビュー行列を設定する
  M = eye(4)
  M[:3,:3] = dot(R,Rx)
  M[:3,3] = t

  # 列方向に平板化するために、まず転置する
  M = M.T
  m = M.flatten()

  # モデルビューを新しい行列に置き換える
  glLoadMatrixf(m)

def draw_background(imname):
  """ 四角形を使って背景画像を描画する """

  # 背景画像(拡張子は.bmp)をOpenGLのテクスチャに読み込む
  bg_image = pygame.image.load(imname).convert()
  bg_data = pygame.image.tostring(bg_image,"RGBX",1)

  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  # テクスチャを関連づける
  glEnable(GL_TEXTURE_2D)
  glBindTexture(GL_TEXTURE_2D,glGenTextures(1)) 
  glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,
               0,GL_RGBA,GL_UNSIGNED_BYTE,bg_data)
  glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
  glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)

  # 四角形を作ってウィンドウ全体を満たすようにする
  glBegin(GL_QUADS)
  glTexCoord2f(0.0,0.0); glVertex3f(-1.0,-1.0,-1.0)
  glTexCoord2f(1.0,0.0); glVertex3f( 1.0,-1.0,-1.0)
  glTexCoord2f(1.0,1.0); glVertex3f( 1.0, 1.0,-1.0)
  glTexCoord2f(0.0,1.0); glVertex3f(-1.0, 1.0,-1.0)
  glEnd()

  # テクスチャを消去する
  glDeleteTextures(1)

def load_and_draw_model(filename):
  """ objloader.pyを使って.objファイルからモデルを読み込む。
   材質ファイルは同じ名前で.mtlであることを仮定 """
  glEnable(GL_LIGHTING)
  glEnable(GL_LIGHT0)
  glEnable(GL_DEPTH_TEST)
  glClear(GL_DEPTH_BUFFER_BIT)

  # モデルの色を設定
  glMaterialfv(GL_FRONT,GL_AMBIENT,[0.1,0.1,0.1,0])
  glMaterialfv(GL_FRONT,GL_DIFFUSE,[0.5,0.75,1.0,0]) 
  glMaterialf(GL_FRONT,GL_SHININESS,0.25*128.0)

  glEnable(GL_NORMALIZE)
  glScalef(0.0085,0.0085,0.0085)

  # ファイルを読み込む
  import objloader
  obj = objloader.OBJ(filename)
  glCallList(obj.gl_list)


def setup():
  """ ウィンドウとpygame環境を設定する """
  pygame.init()
  pygame.display.set_mode((width,height),OPENGL | DOUBLEBUF)
  pygame.display.set_caption('OpenGL AR demo')

# カメラデータを読み込む
with open('ar_camera.pkl','r') as f:
  K = pickle.load(f)
  Rt = pickle.load(f)

setup()
draw_background('book_perspective.bmp')
set_projection_from_camera(K)
set_modelview_from_camera(Rt)
load_and_draw_model('toyplane.obj')

while True:
  event = pygame.event.poll()
  if event.type in (QUIT,KEYDOWN):
    break
  pygame.display.flip()
