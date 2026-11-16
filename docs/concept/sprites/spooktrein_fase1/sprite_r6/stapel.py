# Ronde 5: de hoop als stapel losse objecten, met de hand als tekstraster per object (achter -> voor).
# Jordi r4: "zorg dat het netjes aansluit en dat het echt op een stapel lijkt en niet op een legpuzzel";
# aanvulling: "er mag dus overlap zijn, sommige stukken liggen op andere stukken".
# Schoorsteen en wiel komen ongewijzigd uit r4 (z64.npy-zones); grijze stapelpixels in de onderste schoorsteenzone
# (rij >= 38, die horen bij bijlplaat/klem) zijn vrij.
# 'o' = contour: onder/rechts open -> 'a' (zwart), anders lijnkleur van het materiaal (bruin 'b', grijs 'g').
import numpy as np
from objecten import OBJ
CH='.abcdefghijk'
r4=np.load('../sprite_r4/sprite.npy'); WZ,SZ,RZ,MZ=np.load('../sprite_r4/z64.npy')
yy,xx=np.mgrid[0:64,0:64]
grijs=np.isin(r4,[7,8,9,10])
FROZ=WZ|(SZ&~((yy>=38)&grijs))
o=np.zeros((64,64),int); lay=np.zeros((64,64),int)  # laag-id
fill=np.zeros((64,64),bool)
DONK={'f':'e','e':'d','d':'c','c':'b','b':'b','j':'i','i':'h','h':'g','g':'g'}
for li,(naam,x0,y0,mat,rows) in enumerate(OBJ,1):
    H=len(rows); W=max(len(r) for r in rows)
    G=[r.ljust(W,'.') for r in rows]
    inn=lambda r,c: 0<=r<H and 0<=c<W and G[r][c]!='.'
    lijn='g' if mat=='grijs' else 'b'
    for r in range(H):
        for c in range(W):
            ch=G[r][c]
            if ch=='.': continue
            y,x=y0+r,x0+c
            if ch=='o':
                ch='a' if (not inn(r+1,c) or not inn(r,c+1)) else lijn
                # schaduw onder het object op het object eronder
                if not inn(r+1,c) and y+1<64 and fill[y+1,x] and lay[y+1,x]!=li:
                    o[y+1,x]=CH.index(DONK[CH[o[y+1,x]]])
                fill[y,x]=False
            else: fill[y,x]=True
            o[y,x]=CH.index(ch); lay[y,x]=li
o[FROZ]=r4[FROZ]
np.save('raw.npy',o)
# achtergrond: kieren tussen de objecten (dicht omsloten, of smaller dan 3 px) worden donkere diepte ('b'),
# randpixels daarvan tegen de lucht 'a'.
def sh(m,dy,dx):
    r=np.zeros_like(m); ys=slice(max(dy,0),64+min(dy,0)); yd=slice(max(-dy,0),64+min(-dy,0))
    xs=slice(max(dx,0),64+min(dx,0)); xd=slice(max(-dx,0),64+min(-dx,0)); r[ys,xs]=m[yd,xd]; return r
def dil(m): return np.any([sh(m,dy,dx) for dy in (-1,0,1) for dx in (-1,0,1)],0)
def ero(m): return np.all([sh(m,dy,dx) for dy in (-1,0,1) for dx in (-1,0,1)],0)
U=o>0; C=ero(dil(U))
out=np.zeros((64,64),bool); out[0,:]=out[-1,:]=out[:,0]=out[:,-1]=True; out&=~C
while True:
    n=dil(out)&~C
    if (n==out).all(): break
    out=n
gap=~out&~U
o[gap]=2
U=o>0; edge=U&~ero(np.pad(U,1)[1:-1,1:-1]|False)
edge=U&~(sh(U,1,0)&sh(U,-1,0)&sh(U,0,1)&sh(U,0,-1))
o[edge&gap]=1
o[FROZ]=r4[FROZ]
np.save('raw.npy',o); print('kieren',gap.sum())
