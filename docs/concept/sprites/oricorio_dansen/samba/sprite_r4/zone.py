# hulpbeeld per zone: links het klassenraster, rechts het natieve model met het spriteraster erover (zelfde schaal, 16x), coördinaten = spritecoördinaten
# gebruik: zone.py raster.npy fam.npy|- y0 y1 x0 x1 uit.png [gen3|model]
import numpy as np, sys, json; from PIL import Image, ImageDraw
from palet import pal
o=np.load(sys.argv[1]); fam=np.load(sys.argv[2]) if sys.argv[2]!='-' else None
y0,y1,x0,x1=map(int,sys.argv[3:7]); z=int(sys.argv[9]) if len(sys.argv)>9 else 16; F,OY,OX=2.9,0,0.97; pl=json.load(open('plaats.json'))
P=pal(sys.argv[8] if len(sys.argv)>8 else 'model')
h,w=y1-y0,x1-x0; im=Image.new('RGB',(2*w*z+70,h*z+20),'white'); d=ImageDraw.Draw(im)
for y in range(h):
    for x in range(w):
        v=o[y+y0,x+x0]; c=P[v] if v else (235,235,235)
        if fam is not None and v==1 and fam[y+y0,x+x0]>0: c=[(0,0,0),(0,90,0),(150,110,0),(140,40,60)][fam[y+y0,x+x0]]
        d.rectangle([30+x*z,20+y*z,30+x*z+z-1,20+y*z+z-1],fill=c,outline=(190,190,190))
# model: spritepixel (Y,X) <- natief (Y-dy)*F+OY ..
n=np.asarray(Image.open('natief.png')); X0=50+w*z
for y in range(h*z):
    for x in range(w*z):
        ny=int(((y0+y/z)-pl['dy'])*F+OY); nx=int(((x0+x/z)-pl['dx'])*F+OX)
        if 0<=ny<200 and 0<=nx<200: im.putpixel((X0+x,20+y),tuple(int(c) for c in n[ny,nx]))
for k in range(w+1): d.line([X0+k*z,20,X0+k*z,20+h*z],fill=(255,120,120) if (x0+k)%5==0 else (200,200,200))
for k in range(h+1): d.line([X0,20+k*z,X0+w*z,20+k*z],fill=(255,120,120) if (y0+k)%5==0 else (200,200,200))
for x in range(w):
    if (x+x0)%5==0: d.text((30+x*z,4),str(x+x0),fill='black'); d.text((X0+x*z,4),str(x+x0),fill='black')
for y in range(h):
    if (y+y0)%5==0: d.text((2,20+y*z),str(y+y0),fill='black'); d.text((X0-20,20+y*z),str(y+y0),fill='black')
im.save(sys.argv[7])
