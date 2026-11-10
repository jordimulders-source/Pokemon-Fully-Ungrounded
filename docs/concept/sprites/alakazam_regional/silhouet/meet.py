# per spritepixel: modelgemiddelde (vlak), p15-helderheid, fractie donker (<45) -> meet.npz
import numpy as np
from geo import *
c=model(); L=c.mean(2)
m=np.asarray(__import__('PIL.Image',fromlist=['x']).open('silhouet.png'))[...,3]>0
mean=np.zeros((64,64,3)); p15=np.zeros((64,64)); dark=np.zeros((64,64)); red=np.zeros((64,64))
for Y in range(64):
  for X in range(64):
    ya,yb,xa,xb=blok(X,Y); ya,xa=max(ya,0),max(xa,0)
    b=c[ya:yb,xa:xb].reshape(-1,3); l=b.mean(1)
    mean[Y,X]=b.mean(0); p15[Y,X]=np.percentile(l,15); dark[Y,X]=(l<45).mean()
    red[Y,X]=((b[:,0]-b[:,1])>50).mean()
np.savez('meet.npz',mean=mean,p15=p15,dark=dark,red=red,m=m)
