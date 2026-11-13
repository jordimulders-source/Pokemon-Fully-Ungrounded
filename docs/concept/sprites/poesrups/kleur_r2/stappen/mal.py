# mal.py: meetmal (geen sprite): per rij "y: x0=..." met e=randpixel van het silhouet, binnen = mediaanklasse van het modelblok (klas2);
# hoofdletter L = binnenpixel waar het model voor >=25% donkere lijn is. Dient als onderlegger bij het handwerk in r1.txt.
import numpy as np, sys, os
from PIL import Image
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from bg import masker, P
c=np.asarray(Image.open(P+'referenties/model_gekozen.png').convert('RGB')).astype(float); L=c.mean(2); g=masker()
a=np.array(Image.open(P+'silhouet/silhouet.png'))[:,:,3]>0
x0,y0,s=69,240,16.648
for y in range(64):
  xs=[x for x in range(64) if a[y,x]]
  if not xs: continue
  r=''
  for x in range(xs[0],xs[-1]+1):
    if not a[y,x]: r+=' '; continue
    sl=(slice(int(y0+(y-29)*s),int(y0+(y-28)*s)),slice(int(x0+(x-5)*s),int(x0+(x-4)*s))); f=~g[sl]; v=L[sl][f]
    edge=any(not a[y+dy,x+dx] for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
    m=np.median(v); d=(v<120).mean()
    ch='A' if m>=228 else '7' if m>=212 else '6' if m>=186 else '5' if m>=162 else '4' if m>=130 else '3' if m>=90 else '2'
    r+= ('E' if d>=.4 else 'e') if edge else ('L' if d>=.25 else ch)
  print(f'{y}: {xs[0]}={r}')
