from PIL import Image; import numpy as np
S=np.array(Image.open('sprite_r2/pitahaya_r2.png')); H=S>0
d=np.load('keuring_r2/model_per_px.npz'); mzw,mg,ml,mean=d['mzw'],d['mg'],d['mlum'],d['mean']
import sys; sys.path.insert(0,'sprite_r1'); from groepen import laad
a,lum,g=laad('sprite_r2/natief.png')
def edge(x,y): return any(not H[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1)))
face=lambda x,y: 18<=x<=34 and 22<=y<=34
lst=[]
for y in range(64):
  for x in range(64):
    if S[y,x]==1 and not edge(x,y) and not face(x,y) and mzw[y,x]<=3:
      r=3*(y+2); c=1+3*(x+1); gb=g[r:r+3,c:c+3]
      cnt={k:(gb==k).sum() for k in (2,3,4)}; k=max(cnt,key=cnt.get)
      tgt=2 if k in(2,3) else 8
      lst.append((x,y,int(mzw[y,x]),'roze' if tgt==2 else 'groen',tgt))
print(len(lst))
for t in lst: print(t)
T=S.copy()
for x,y,_,_,t in lst: T[y,x]=t
n=H.sum(); intd=sum(1 for y in range(64) for x in range(64) if T[y,x]==1 and not edge(x,y))
print('na: zwart %.1f%% binnen %.1f%%'%(100*(T==1).sum()/n,100*intd/n))
np.save('keuring_r2/dunlijn_T.npy',T)
