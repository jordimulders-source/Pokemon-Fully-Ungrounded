# Per grijze vulcel (d/g/w) de meest voorkomende modeltint (k/d/g/w op helderheid) i.p.v. het vlakgemiddelde.
# Gelijkspel: huidige tint blijft. Geeft lijst (x,y,nieuw) per zone; wordt niet automatisch toegepast.
import numpy as np; from PIL import Image
from collections import Counter
src=open('zones.py').read(); exec(src[src.index('def zone'):src.index('from collections')])
nat=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); grp=np.load('ngrp.npy'); L=nat.mean(-1)
X0,Y0,fx,fy,OX,OY=21,12,109/56,123/63,4,1
def tint(l): return 2 if l<75 else 3 if l<140 else 4 if l<190 else 5
def modus(r):
  res={}
  for y in range(64):
      for x in range(64):
          if r[y,x] not in (3,4,5): continue
          xs=range(int(np.floor(X0+(x-OX)*fx)),int(np.ceil(X0+(x-OX+1)*fx))); ys=range(int(np.floor(Y0+(y-OY)*fy)),int(np.ceil(Y0+(y-OY+1)*fy)))
          c=Counter(tint(L[j,i]) for j in ys for i in xs if grp[j,i]=='k')
          if not c: continue
          top=c.most_common(); best=top[0][0]
          if len(top)>1 and top[1][1]==top[0][1]: continue
          if best==2: continue   # geen antraciet in de vulling erbij (lijnen blijven zoals ze zijn)
          if best!=r[y,x]: res.setdefault(zone(x,y),[]).append((x,y,'kdgw'[best-2]))
  return res
if __name__=='__main__':
  r=np.loadtxt('mug_r1.idx',dtype=int)
  for z,v in modus(r).items(): print(z,len(v),v)
