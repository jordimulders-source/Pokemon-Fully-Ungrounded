# meet10.py: per spritepixel uit model_hybride.png de gemiddelde helderheid van de niet-lijnpixels (lum >= 70) -> hel10.npy
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'../../gnometrotter_rock/sprite')
from reductie_gedeeld import bron
a=np.asarray(Image.open('../hybride/model_hybride.png').convert('RGB')).astype(float)
L=0.30*a[...,0]+0.59*a[...,1]+0.11*a[...,2]; fg=a.min(2)<235
hel=np.zeros((64,64))
for Y in range(64):
    for X in range(64):
        s=w0=0
        for u,v,w in bron(X,Y):
            if fg[v,u] and L[v,u]>=70: s+=w*L[v,u]; w0+=w
        if w0: hel[Y,X]=s/w0
np.save('hel10.npy',hel)
