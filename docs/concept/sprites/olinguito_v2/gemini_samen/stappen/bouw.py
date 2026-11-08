# raster.txt <- verf-spec ; png + controles
import sys,numpy as np
from PIL import Image
spec,out=sys.argv[1],sys.argv[2]
g=[['.']*64 for _ in range(64)]
for l in open(spec):
    if l.startswith('#') or not l.strip(): continue
    y,x,s=l.split()[:3]; y=int(y);x=int(x)
    for i,ch in enumerate(s):
        if ch!=' ': g[y][x+i]=ch
open(out.replace('.png','_raster.txt'),'w').write('\n'.join(''.join(r) for r in g)+'\n')
old=Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/olinguito_v2/af/olinguito.png')
a=np.array([[0 if c=='.' else int(c,16) for c in r] for r in g],'uint8')
im=Image.fromarray(a,'P'); im.putpalette(old.getpalette()[:48]); im.info['transparency']=0
im.save(out,transparency=0)
m=np.load('stappen/sil.npy')
print('px',(a>0).sum(),'sil',m.sum(),'buiten sil',((a>0)&~m).sum(),'sil niet gevuld',(m&(a==0)).sum())
