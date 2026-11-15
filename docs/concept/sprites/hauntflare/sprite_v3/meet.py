# Controles v2 (vanuit de repo-root): python3 docs/concept/sprites/hauntflare/sprite_v2/meet.py [png]
import sys; from PIL import Image; import numpy as np
from scipy import ndimage as nd
D='docs/concept/sprites/hauntflare/'; S=D+'sprite_v3/'
f=sys.argv[1] if len(sys.argv)>1 else S+'hauntflare_v3.png'
o=np.load(f) if f.endswith('.npy') else np.array(Image.open(f))
B=np.array(Image.open(D+'basis/basis_64.png'))[...,3]>0
GZ=np.load(S+'gezicht_masker.npy')
K4=[[0,1,0],[1,1,1],[0,1,0]]
op=o>0
print('silhouet t.o.v. basis: erbij',int((op&~B).sum()),list(zip(*np.where(op&~B)[::-1])),' eraf',int((B&~op).sum()))
print('kleuren incl. transparant:',len(np.unique(o)),'(indexen',sorted(int(v) for v in np.unique(o)),')')
rand=op&nd.binary_dilation(~op,K4)
LICHT={3,4,6,7,8,9,12,13,14,15}
print('lichte kleur op de buitenrand:',[(int(x),int(y),int(o[y,x])) for y,x in zip(*np.where(rand&np.isin(o,list(LICHT))))])
LIJN=[1,2,5,10]
print('buitenrand niet-lijnkleur:',int((rand&~np.isin(o,LIJN)).sum()))
# om-en-om: randpixel waarvan alle randburen een andere lijnkleur hebben
oe=[]
for y,x in zip(*np.where(rand)):
    nb=[o[y+a,x+b] for a in(-1,0,1) for b in(-1,0,1) if (a or b) and 0<=y+a<64 and 0<=x+b<64 and rand[y+a,x+b]]
    if nb and o[y,x] not in nb: oe.append((int(x),int(y)))
print('rand om-en-om (losse afwijkende randpixel):',oe)
# dubbele buitenlijn: zwarte binnenpixel 4-buur van zwarte randpixel, terwijl hij zelf ook vulling raakt aan de overkant
dub=[]
for y,x in zip(*np.where(op&~rand&(o==1)&~GZ)):
    for a,b in((1,0),(-1,0),(0,1),(0,-1)):
        if rand[y+a,x+b] and o[y+a,x+b]==1 and o[y-a,x-b] not in (0,1,2,10,5): dub.append((int(x),int(y)))
print('mogelijke dubbele buitenlijn (zwart achter zwarte rand):',len(set(dub)),sorted(set(dub)))
# losse tintvlakjes < 3 px (8-verbonden, per index), buiten gezicht en lijnen
kl=[]
for t in [3,4,6,7,8,9,11,12,13,15]:
    l,k=nd.label((o==t)&~GZ,np.ones((3,3)))
    for i in range(1,k+1):
        if (l==i).sum()<3:
            ys,xs=np.where(l==i); kl.append((int(xs[0]),int(ys[0]),t,int((l==i).sum())))
print('tintvlakjes < 3 px:',len(kl),kl)
