# Model op het spriteraster: uitsnede (sprite-lokaal X0..X1, Y0..Y1) op Z px per cel met rasterlijnen en labels
import sys, numpy as np
from PIL import Image, ImageDraw
X0,Y0,X1,Y1,Z=map(int,sys.argv[1:6]); out=sys.argv[6]; H=52
m=Image.open('../referenties/model_r3b.png').convert('RGB'); a=np.asarray(m).astype(int); fg=a.min(2)<225
ys,xs=np.nonzero(fg); x0,y0,y1=xs.min(),ys.min(),ys.max()+1; p=(y1-y0)/H
mc=m.crop((int(round(x0+X0*p)),int(round(y0+Y0*p)),int(round(x0+X1*p)),int(round(y0+Y1*p)))).resize(((X1-X0)*Z,(Y1-Y0)*Z),Image.NEAREST)
V=Image.new('RGB',(mc.width+40,mc.height+40),(255,255,255)); V.paste(mc,(40,40)); d=ImageDraw.Draw(V)
for i in range(X1-X0+1): d.line([(40+i*Z,40),(40+i*Z,40+mc.height)],fill=(255,0,0) if (X0+i)%5==0 else (0,200,255))
for j in range(Y1-Y0+1): d.line([(40,40+j*Z),(40+mc.width,40+j*Z)],fill=(255,0,0) if (Y0+j)%5==0 else (0,200,255))
for i in range(X1-X0): d.text((40+i*Z+Z//3,20),str(X0+i),fill=(0,0,0))
for j in range(Y1-Y0): d.text((5,40+j*Z+Z//3),str(Y0+j),fill=(0,0,0))
V.save(out)
