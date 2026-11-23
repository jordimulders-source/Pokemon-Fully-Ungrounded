import sys, numpy as np; sys.path.insert(0,'.'); sys.path.insert(0,'r2')
from PIL import Image
from cc import label
SRC='eindkeuring/claydol_eind.png'
E=np.array(Image.open(SRC)); PAL=np.array(Image.open(SRC).getpalette()[:48]).reshape(16,3)
M=np.load('r5/M.npy')
comp,_=label(E>0,diag=True); MAIN=comp==comp[50,30]
yy,xx=np.mgrid[0:64,0:64]
ONDERKOP=MAIN&(yy>=29)&(yy<=39)&(xx>=9)&(xx<=47)&~((yy>=30)&(yy<=36)&(xx<=14))  # zonder krans-bolletje L5 links
LIJF=MAIN&(yy>=40)&(xx>=10)&(xx<=50)
L=lambda c:(np.asarray(c,float)*[0.299,0.587,0.114]).sum(-1)
