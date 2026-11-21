# frac.py x0 y0 x1 y1: per spritepixel de oppervlaktefracties per modelklasse (K zwart, v vogel, w wolk, Y geel, W wit) in tienden
# en de gemiddelde modelhelderheid (L) -> om elke reparatie op een gemeten modelpixel te zetten.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen; from gemeen import *
a,c,L=klassen(); x0,y0,x1,y1=map(int,sys.argv[1:5])
for Y in range(y0,y1):
    row=[]
    for X in range(x0,x1):
        f=np.zeros(6); l=0
        for u,v,w in overlap(X,Y): f[c[v,u]]+=w; l+=w*L[v,u]
        s=''.join('%s%d'%(n,round(10*f[k])) for k,n in ((1,'K'),(2,'v'),(3,'w'),(4,'Y'),(5,'W')) if f[k]>=0.05)
        row.append('%2d,%2d:%-12s'%(X,Y,s or '-'))
    print(' '.join(row))
