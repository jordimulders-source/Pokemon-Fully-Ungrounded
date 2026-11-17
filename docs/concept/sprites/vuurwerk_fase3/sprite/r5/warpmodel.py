# hulpmiddel: het model vervormd naar r5-coordinaten (zelfde vervorming als kop5.py), Z px per spritepixel, met raster,
# en de r5-kop ernaast. Voor de vergelijking per pixel (oog, lijnen) en de overlay.
import sys, numpy as np; from PIL import Image, ImageDraw
SCHAAL=float(sys.argv[1]); AX,AY,R=22.0,18.0,7.0; Z=int(sys.argv[3]) if len(sys.argv)>3 else 16
x0,y0,x1,y1=[int(v) for v in sys.argv[4].split(',')] if len(sys.argv)>4 else (0,0,26,32)
M=np.asarray(Image.open('../../referenties/model_v14.png').convert('RGB'))
uu=x0+(np.arange((x1-x0)*Z)+0.5)/Z; vv=y0+(np.arange((y1-y0)*Z)+0.5)/Z
U,V=np.meshgrid(uu,vv); d=AX-U; t=np.clip(d/R,0,1); s=1+(SCHAAL-1)*t*t*(3-2*t); s[d<0]=1
up=AX-d/s; vp=AY+(V-AY)/s
mx=np.clip((106+12*up).astype(int),0,1023); my=np.clip((120+12*vp).astype(int),0,1023)
im=Image.fromarray(M[my,mx]); dr=ImageDraw.Draw(im)
for i in range(x1-x0+1): dr.line([(i*Z,0),(i*Z,im.size[1])],fill=(0,200,255))
for j in range(y1-y0+1): dr.line([(0,j*Z),(im.size[0],j*Z)],fill=(0,200,255))
for i in range(x1-x0): dr.text((i*Z+1,1),str(x0+i),fill=(0,0,255))
for j in range(y1-y0): dr.text((1,j*Z+1),str(y0+j),fill=(0,0,255))
im.save(sys.argv[2])
