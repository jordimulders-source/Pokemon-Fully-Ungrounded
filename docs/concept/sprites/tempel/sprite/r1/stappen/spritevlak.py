# spritevlak.py: per spritepixel het meerderheidsvlak van het model, toon = uitgevlakte vlakhelderheid, lijnfractie
import numpy as np
from PIL import Image, ImageFilter
M='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp'
c=np.asarray(Image.open(M).convert('RGB')).astype(float); L=c.mean(2)
lab=np.load('labels.npy'); SL=np.load('SL.npy')
lines=np.asarray(Image.open('lijnen_model.png'))>0
d=np.load('red.npz'); s=float(d['s']); top=int(d['top']); left=int(d['left'])
X0,Y0=46,57
LS=np.zeros((64,64),int); TN=np.zeros((64,64)); THK=np.zeros((64,64)); DOOR=np.zeros((64,64)); COV=np.zeros((64,64))
GRN=np.zeros((64,64)); BR=np.zeros((64,64))
gr=(c[...,1]-c[...,0])
for by in range(60):
  for bx in range(62):
    ya,yb=int(Y0+by*s),int(Y0+(by+1)*s); xa,xb=int(X0+bx*s),int(X0+(bx+1)*s)
    y,x=top+by,left+bx
    lb=lab[ya:yb,xa:xb]; n=lb.size
    THK[y,x]=(lines[ya:yb,xa:xb]&(lb==0)).sum()/n
    DOOR[y,x]=(L[ya:yb,xa:xb]<45).sum()/n
    BR[y,x]=(L[ya:yb,xa:xb]>200).sum()/n
    v=lb[lb>0]
    if v.size:
        k=np.bincount(v).argmax(); LS[y,x]=k; COV[y,x]=(v==k).sum()/n
        sel=lb==k; TN[y,x]=SL[ya:yb,xa:xb][sel].mean(); GRN[y,x]=gr[ya:yb,xa:xb][sel].mean()
np.savez('sv.npz',LS=LS,TN=TN,THK=THK,DOOR=DOOR,COV=COV,GRN=GRN,BR=BR)
