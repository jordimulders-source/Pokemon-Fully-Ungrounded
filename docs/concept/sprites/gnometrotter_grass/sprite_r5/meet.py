# meet.py: per spritepixel uit model_hybride.png (gedeelde geometrie): gemiddelde helderheid (hel) en
# aandeel donkere lijnpixels (donk: lum < 115 roze / < 100 blauw, zoals de facetdrempels in GEDEELD.md) -> meet.npz
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../../gnometrotter_rock/sprite')
from reductie_gedeeld import bron
a=np.asarray(Image.open('../hybride/model_hybride.png').convert('RGB')).astype(float)
L=0.30*a[...,0]+0.59*a[...,1]+0.11*a[...,2]; fg=a.min(2)<235
blauw=a[...,2]>a[...,0]+20
donk=np.zeros((64,64)); hel=np.zeros((64,64))
for Y in range(64):
    for X in range(64):
        tw=dw=hs=hw=0
        for u,v,w in bron(X,Y):
            if not fg[v,u]: continue
            tw+=w
            if L[v,u] < (100 if blauw[v,u] else 115): dw+=w
            else: hw+=w; hs+=w*L[v,u]
        if tw: donk[Y,X]=dw/tw
        if hw: hel[Y,X]=hs/hw
np.savez('meet.npz',donk=donk,hel=hel)
