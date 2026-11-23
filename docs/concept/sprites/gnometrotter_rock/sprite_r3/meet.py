# meet.py: per spritepixel uit het model (gedeelde geometrie): donker-aandeel (lum < 80) en gemiddelde helderheid van de niet-donkere
# figuurpixels -> meet.npz (donk, hel). Print een uitsnede: meet.py x0 y0 x1 y1
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../sprite')
from reductie_gedeeld import bron
import os
if not os.path.exists('meet.npz'):
    a=np.asarray(Image.open('../r8/gemini_r8.png').convert('RGB')).astype(float); L=0.30*a[...,0]+0.59*a[...,1]+0.11*a[...,2]; fg=a.min(2)<235
    donk=np.zeros((64,64)); hel=np.zeros((64,64))
    for Y in range(64):
        for X in range(64):
            tw=dw=hw=hs=0
            for u,v,w in bron(X,Y):
                tw+=w
                if not fg[v,u]: continue
                if L[v,u]<80: dw+=w
                else: hw+=w; hs+=w*L[v,u]
            if tw: donk[Y,X]=dw/tw
            if hw: hel[Y,X]=hs/hw
    np.savez('meet.npz',donk=donk,hel=hel)
d=np.load('meet.npz'); donk,hel=d['donk'],d['hel']
if len(sys.argv)>4:
    x0,y0,x1,y1=map(int,sys.argv[1:5])
    print('    '+''.join('%4d'%x for x in range(x0,x1)))
    for Y in range(y0,y1): print('%2d  '%Y+''.join(('  ##' if donk[Y,X]>=0.35 else '%4d'%hel[Y,X]) for X in range(x0,x1)))
