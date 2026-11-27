# Haarmasker (manen) in r3b en r3c: pixels die afwijken van r3 (zelfde ontwerp, beeld pixel-gelijk buiten de manen)
# binnen het manengebied. Zo is een lok = modelpixels, geen getekende vorm. Uit: haar_r3b.npy, haar_r3c.npy, haar_viz.png
import numpy as np
from PIL import Image
from scipy import ndimage as nd
L=lambda n:np.asarray(Image.open(n).convert('RGB')).astype(int)
r3=L('../gemini/r3/kudu_r3.png')
for n,p in [('r3b','../referenties/model_r3b.png'),('r3c','../gemini/r3c/kudu_r3c.png')]:
    a=L(p)
    d=np.abs(a-r3).sum(2)>70
    reg=np.zeros(d.shape,bool); reg[360:780,200:640]=True
    m=d&reg&(a.min(2)<232)
    m=nd.binary_closing(m,iterations=3); m=nd.binary_opening(m,iterations=2)
    lab,n_=nd.label(m); sz=nd.sum(m,lab,range(1,n_+1)); m=np.isin(lab,1+np.nonzero(sz>=400)[0])
    m=nd.binary_fill_holes(m)&(a.min(2)<232)
    np.save(f'haar_{n}.npy',m)
    v=a.copy(); v[m]=(v[m]*0.4+np.array([255,0,0])*0.6).astype(int)
    Image.fromarray(v[300:800,150:700].astype('uint8')).save(f'r1/haar_{n}_viz.png'); print(n,m.sum())
