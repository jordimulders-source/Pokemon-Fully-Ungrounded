# reductie van een zone: python3 red.py x0 y0 x1 y1 -> per pixel: silhouet, donker, oog, helderheid
import sys,numpy as np
from mcov import *
x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]
fg=a.min(2)<235; c=cov(fg,x0,y0,x1,y1); dk=cov(L<75,x0,y0,x1,y1)
eye=(a[...,2]-a[...,0]>15)&(a[...,1]>165); ec=cov(eye,x0,y0,x1,y1)
Lm=cov(np.where(fg,L,np.nan) if False else L*fg,x0,y0,x1,y1)
print('     '+''.join('%3d'%i for i in range(x0,x1)))
for j in range(y0,y1):
    s=''
    for i in range(x0,x1):
        if c[j,i]<0.5: s+='  .'; continue
        if ec[j,i]>=0.3: s+='  E'; continue
        if dk[j,i]>=0.5: s+='  K'; continue
        s+='%3d'%int(Lm[j,i]/c[j,i])
    print('%3d  '%j+s)
