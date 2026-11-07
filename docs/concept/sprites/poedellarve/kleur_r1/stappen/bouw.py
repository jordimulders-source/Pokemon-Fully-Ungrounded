# bouw.py r1.txt raster.txt : tekstraster (handwerk, "y: x=pixels", spaties genegeerd) -> 64x64 raster; meldt silhouetfouten
import sys,numpy as np
from PIL import Image
S='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poedellarve/silhouet/silhouet.png'
a=np.array(Image.open(S))[:,:,3]>0
R=[['.']*64 for _ in range(64)]
for l in open(sys.argv[1]):
    if l.startswith('#') or not l.strip(): continue
    y,rest=l.split(':',1); y=int(y)
    toks=rest.split(); i=0; cur=None
    # stukken "x=pixels" (spaties binnen een stuk mogen)
    stuk=[]
    for t in toks:
        if '=' in t: stuk.append([int(t.split('=')[0]),t.split('=')[1]])
        else: stuk[-1][1]+=t
    for x0,s in stuk:
        for k,c in enumerate(s): R[y][x0+k]=c
fout=[(x,y) for y in range(64) for x in range(64) if (R[y][x]!='.')!=a[y,x]]
for y in range(64):
    xs=[x for x in range(64) if a[y,x]]; ys=[x for x in range(64) if R[y][x]!='.']
    if xs!=ys: print('rij',y,'sil',xs[:1],xs[-1:],len(xs),'raster',ys[:1],ys[-1:],len(ys))
print('silhouetfouten',len(fout))
open(sys.argv[2],'w').write('\n'.join(''.join(r) for r in R)+'\n')
