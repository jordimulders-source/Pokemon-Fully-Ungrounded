# Sprite-raster (npy of png) naast het model op dezelfde schaal, met coordinaten. python3 naast.py raster.npy c0 c1 r0 r1 schaal uit.png
import sys, numpy as np; from PIL import Image, ImageDraw
from palet import PAL
z=np.load('reductie.npz'); xs,ys=z['xs'],z['ys']
arr=np.load(sys.argv[1]); c0,c1,r0,r1,s=map(int,sys.argv[2:7]); out=sys.argv[7]
im=Image.open('../referenties/gemini_gekozen_v2.png').convert('RGB')
w,h=(c1-c0+1)*s,(r1-r0+1)*s
mod=im.crop((int(xs[c0]),int(ys[r0]),int(xs[c1+1]),int(ys[r1+1]))).resize((w,h),Image.LANCZOS)
sp=np.zeros((r1-r0+1,c1-c0+1,3),'uint8'); sp[:]=255
for j in range(r0,r1+1):
    for i in range(c0,c1+1):
        v=arr[j,i]
        if v: sp[j-r0,i-c0]=PAL[v]
spi=Image.fromarray(sp).resize((w,h),Image.NEAREST)
cv=Image.new('RGB',(2*w+50,h+20),'white'); cv.paste(spi,(30,20)); cv.paste(mod,(w+50,20)); d=ImageDraw.Draw(cv)
for off in (30,w+50):
    for i in range(c0,c1+2):
        x=off+(i-c0)*s; d.line([(x,20),(x,h+20)],fill=(200,200,200))
        if i<=c1 and off==30: d.text((x+2,6),str(i%100),fill=(0,0,0))
    for j in range(r0,r1+2):
        y=20+(j-r0)*s; d.line([(off,y),(off+w,y)],fill=(200,200,200))
        if j<=r1 and off==30: d.text((3,y+2),str(j),fill=(0,0,0))
cv.save(out)
