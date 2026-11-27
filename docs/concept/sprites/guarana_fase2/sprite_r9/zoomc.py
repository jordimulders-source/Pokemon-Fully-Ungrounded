# zoomc.py SPRITE x0 y0 x1 y1 schaal uit [SPRITE2 ...]: uitsnede(s) vergroot naast elkaar, met raster
import sys; sys.path.insert(0,'sprite_r9'); from gemeen2 import *; import numpy as np; from PIL import Image, ImageDraw
a=sys.argv; x0,y0,x1,y1,s=map(int,a[2:7]); uit=a[7]; ps=[a[1]]+a[8:]
W=(x1-x0)*s; T=Image.new('RGB',((W+10)*len(ps),(y1-y0)*s),'white')
for i,p in enumerate(ps):
    im=Image.open(p)
    if im.mode=='P' and im.size==(64,64): c=rgb(np.array(im),(255,255,255))
    else: c=im.convert('RGB').resize((64,64)) if im.size!=(64,64) else im.convert('RGB')
    c=c.crop((x0,y0,x1,y1)).resize((W,(y1-y0)*s),0); d=ImageDraw.Draw(c)
    for k in range(0,x1-x0,5): d.line([(k*s,0),(k*s,4)],fill=(0,0,255))
    T.paste(c,(i*(W+10),0))
T.save(uit)
