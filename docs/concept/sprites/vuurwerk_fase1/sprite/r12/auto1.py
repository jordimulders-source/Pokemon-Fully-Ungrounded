# Kale meting-reductie van de handenzone (rij 15-20, kol 18-24 en 28-33); buitenlijn (grenst aan transparant) blijft r11.
import sys; sys.path.insert(0,'.'); sys.path.insert(0,'../r10')
from meet import meet; from txt import CH
import numpy as np; from PIL import Image
a=np.array(Image.open('../r11/sprite.png')); b=a.copy()
I={c:i for i,c in enumerate(CH)}
def zone(r,c): return 15<=r<=20 and (18<=c<=24 or 28<=c<=33)
for r in range(13,23):
  for c in range(17,37):
    if not zone(r,c) or a[r,c]==0: continue
    if any(a[r+dy,c+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): continue
    ln,be,e,L=meet(r,c)
    if ln>=0.35: v='d'
    elif be>=0.5: continue
    else: v='l' if L>=165 else 'm' if L>=130 else 's'
    b[r,c]=I[v]
np.save(sys.argv[1],b)
for r in range(13,23): print('%3d '%r+''.join(CH[v] for v in a[r,17:37])+'   '+''.join(CH[v] for v in b[r,17:37]))
