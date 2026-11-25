# kop/onderdeel op 20x met raster en spritecoordinaten (sprite-lokaal, zonder OX/OY) naast het model op dezelfde cellen
import sys, json, numpy as np
from PIL import Image, ImageDraw
RN=sys.argv[1]; X0,Y0,X1,Y1=map(int,sys.argv[2:6]); out=sys.argv[6]; Z=20
meta=json.load(open(f'{RN}/grid.json')); OX,OY=meta['OX'],meta['OY']; H=len(meta['grid'])
sp=Image.open(f'{RN}/dikdik_{RN}.png').convert('RGBA').crop((OX+X0,OY+Y0,OX+X1,OY+Y1))
m=Image.open('../referenties/model_r3b.png').convert('RGB'); a=np.asarray(m).astype(int); fg=a.min(2)<225
ys,xs=np.nonzero(fg); x0,y0,y1=xs.min(),ys.min(),ys.max()+1; p=(y1-y0)/H
mc=m.crop((int(x0+X0*p),int(y0+Y0*p),int(x0+X1*p),int(y0+Y1*p))).resize(((X1-X0)*Z,(Y1-Y0)*Z),Image.NEAREST)
w,h=(X1-X0)*Z,(Y1-Y0)*Z
V=Image.new('RGBA',(2*w+60,h+30),(255,255,255,255)); V.paste(sp.resize((w,h),Image.NEAREST),(30,30),sp.resize((w,h),Image.NEAREST)); V.paste(mc,(w+60,30))
d=ImageDraw.Draw(V)
for off in (30,w+60):
    for i in range(X1-X0+1): d.line([(off+i*Z,30),(off+i*Z,30+h)],fill=(255,0,0) if (X0+i)%5==0 else (190,190,190))
    for j in range(Y1-Y0+1): d.line([(off,30+j*Z),(off+w,30+j*Z)],fill=(255,0,0) if (Y0+j)%5==0 else (190,190,190))
for i in range(X1-X0):
    if (X0+i)%5==0: d.text((30+i*Z+2,12),str(X0+i),fill=(0,0,0))
for j in range(Y1-Y0):
    if (Y0+j)%5==0: d.text((4,30+j*Z+2),str(Y0+j),fill=(0,0,0))
V.save(out)
