import sys,numpy as np
from PIL import Image
base,spec,out=sys.argv[1:4]
g=[list(l.rstrip('\n')) for l in open(base)]
for l in open(spec):
    if l.startswith('#') or not l.strip(): continue
    y,x,s=l.split()[:3]; y=int(y);x=int(x)
    for i,ch in enumerate(s): g[y][x+i]=ch
txt='\n'.join(''.join(r) for r in g)+'\n'
assert '?' not in txt, [ (y,r.index('?')) for y,r in enumerate(txt.split('\n')) if '?' in r]
open(out.replace('.png','_raster.txt'),'w').write(txt)
old=Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/olinguito_v2/af/olinguito.png')
a=np.array([[0 if c=='.' else int(c,16) for c in r] for r in g],'uint8')
im=Image.fromarray(a,'P'); im.putpalette(old.getpalette()[:48]); im.save(out,transparency=0)
print('px',(a>0).sum())
