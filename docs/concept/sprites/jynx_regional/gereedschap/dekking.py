# dekking.py x0 y0 x1 y1: per spritepixel de modeldekking per klasse (K,O,H,W,M,P,E,C) in %, plus huidige r1-index
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *; from klassen import klassen, NAMEN
a,c,L=klassen(); x0,y0,x1,y1=map(int,sys.argv[1:5])
o=np.asarray(Image.open(sys.argv[5])) if len(sys.argv)>5 else None
for Y in range(y0,y1):
    for X in range(x0,x1):
        f=np.zeros(9); lum=np.zeros(9)
        for u,v,w in overlap(X,Y): f[c[v,u]]+=w; lum[c[v,u]]+=w*L[v,u]
        t=f.sum(); s=' '.join('%s%2d'%(NAMEN[k],round(100*f[k]/t)) for k in range(9) if f[k]/t>=0.05)
        print('(%d,%d) %s %s'%(X,Y,CH[o[Y,X]] if o is not None else '',s))
