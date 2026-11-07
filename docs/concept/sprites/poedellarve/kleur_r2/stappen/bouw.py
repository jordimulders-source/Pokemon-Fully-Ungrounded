# bouw.py r.txt raster.txt : tekstraster (handwerk, "y: x=pixels", spaties genegeerd) -> 64x64 raster; meldt elke alpha-afwijking van het silhouet
import sys,numpy as np
from PIL import Image
S='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poedellarve/silhouet/silhouet.png'
a=np.array(Image.open(S))[:,:,3]>0
R=[['.']*64 for _ in range(64)]
for l in open(sys.argv[1]):
    if l.startswith('#') or not l.strip(): continue
    y,rest=l.split(':',1); y=int(y); stuk=[]
    for t in rest.split():
        if '=' in t: stuk.append([int(t.split('=')[0]),t.split('=')[1]])
        else: stuk[-1][1]+=t
    for x0,s in stuk:
        for k,c in enumerate(s): R[y][x0+k]=c
extra=[(x,y) for y in range(64) for x in range(64) if R[y][x]!='.' and not a[y,x]]
mist=[(x,y) for y in range(64) for x in range(64) if R[y][x]=='.' and a[y,x]]
print('alpha-afwijking: erbij',extra,'eraf',mist)
open(sys.argv[2],'w').write('\n'.join(''.join(r) for r in R)+'\n')
