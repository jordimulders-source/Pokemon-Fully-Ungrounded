# lijnenkaart van het model (aandeel donkere bronpixels per spritepixel) naast de lijnen van de sprite
import sys, numpy as np
from PIL import Image
src=np.array(Image.open('/home/user/pokemon-fully-ungrounded/docs/concept/sprites/poedelmot/referenties/samengesteld.png').convert('RGB')).astype(int)
k=(854-139)/62; X0=139-k; Y0=150-17*k
lum=src.mean(2); dark=(lum<95)&~((src[...,1]>src[...,0]+15))
M=np.zeros((64,64))
import os
for y in range(64):
    for x in range(64):
        a=dark[int(Y0+y*k):int(Y0+(y+1)*k), int(X0+x*k):int(X0+(x+1)*k)]
        M[y,x]=a.mean() if a.size else 0
r=[l.rstrip('\n') for l in open(sys.argv[1])]
S=10; W=Image.new('RGB',(64*S*2+20,64*S),'white'); P=W.load()
COL={'1':(16,8,8),'2':(56,40,32),'3':(96,72,56),'4':(152,120,104)}
for y in range(64):
    for x in range(64):
        v=M[y,x]; c=(255,255,255) if v<0.2 else (int(255-200*min(1,v)),)*3
        cs=COL.get(r[y][x],(255,255,255))
        for dy in range(S):
            for dx in range(S):
                P[x*S+dx,y*S+dy]=c; P[64*S+20+x*S+dx,y*S+dy]=cs
from PIL import ImageDraw
d=ImageDraw.Draw(W)
for i in range(0,64,5):
    for o in (0,64*S+20):
        d.line([(o+i*S,0),(o+i*S,64*S)],fill=(255,180,180)); d.line([(o,i*S),(o+64*S,i*S)],fill=(255,180,180))
W.save(sys.argv[2])
np.save(os.path.join(os.path.dirname(os.path.abspath(sys.argv[2])),'modellijnen.npy'),M)
