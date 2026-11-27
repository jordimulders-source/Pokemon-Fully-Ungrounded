# Natief model groot met de spritepixelgrenzen (rood) erover, plus spritecoordinaten. gebruik: rasterover.py sx0 sy0 sx1 sy1 uit.png [S]
import sys, numpy as np
from PIL import Image, ImageDraw
D=__file__.rsplit('/',1)[0]
sx0,sy0,sx1,sy1=map(int,sys.argv[1:5]); uit=sys.argv[5]; S=float(sys.argv[6]) if len(sys.argv)>6 else 0.6
X0,Y0=10,24; W,H=int(np.ceil(85*S)),int(np.ceil(52*S)); OX,OY=(64-W)//2,64-H-4
Z=24
n=np.load(D+'/nat.npy')
nx0=X0+(sx0-OX)/S; ny0=Y0+(sy0-OY)/S; nx1=X0+(sx1-OX)/S; ny1=Y0+(sy1-OY)/S
a,b,c,d=int(np.floor(nx0)),int(np.floor(ny0)),int(np.ceil(nx1)),int(np.ceil(ny1))
im=Image.fromarray(n[b:d,a:c]).resize(((c-a)*Z,(d-b)*Z),Image.NEAREST).convert('RGB')
dr=ImageDraw.Draw(im)
for i in range(sx0,sx1+1):
    x=((X0+(i-OX)/S)-a)*Z; dr.line([(x,0),(x,im.height)],fill=(255,0,0),width=1)
    if i<sx1: dr.text((x+3,2),str(i),fill=(255,0,0))
for j in range(sy0,sy1+1):
    y=((Y0+(j-OY)/S)-b)*Z; dr.line([(0,y),(im.width,y)],fill=(255,0,0),width=1)
    if j<sy1: dr.text((2,y+3),str(j),fill=(255,0,0))
im.save(uit); print(im.size)
