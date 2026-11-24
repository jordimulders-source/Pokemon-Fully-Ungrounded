# Paneelrand: het model heeft binnen de zwarte omlijning een lichte/paarse rand (1 natieve px = 0,7 spritepx). Die valt bij de
# blokreductie weg tegen de omlijning. Regel: vulpixel (9/10) in een paneel, 4-buur van een omlijningspixel die aan transparant
# grenst, met randklasse-fractie in zijn blok >= 0,15 -> die randklasse (11 boven/licht, 7 onder/paars, 15 klein paneel).
import numpy as np, sys; from PIL import Image
o=np.load(sys.argv[1]).copy(); F=np.load(sys.argv[2]); UIT=sys.argv[3]
k=np.load('klassen2.npy'); Z=np.array(Image.open('zones.png')); s=(978-46)/64; H,W=o.shape
zs=np.zeros((H,W),int)
for j in range(H):
    for i in range(W):
        z=Z[int(143+(j+.5)*s),int(46+(i+.5)*s)]; zs[j,i]=z
nb=lambda j,i:[(j+dy,i+dx) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if 0<=j+dy<H and 0<=i+dx<W]
buiten=lambda j,i: o[j,i]==1 and any(o[q]==0 for q in nb(j,i)) or (o[j,i]==1 and (i in (0,W-1)))
ch=[]
for j in range(H):
    for i in range(W):
        if zs[j,i]==0 or o[j,i] not in (9,10): continue
        if not any(buiten(*q) for q in nb(j,i)): continue
        f=F[j,i]
        kand={11:f[11],7:f[7]+f[8]+f[6]} if zs[j,i]==2 else {15:f[15]}
        if zs[j,i]==2: kand[15]=f[15]
        best=max(kand,key=kand.get)
        if kand[best]>=0.15: o[j,i]=best; ch.append((i,j+7,best))
np.save(UIT,o); print('paneelrand:',len(ch),ch)
# nawerk: losse paarse randpixels (7) in het grote paneel zonder 8-buur 7/8 -> vulkleur 9 (anders zwart/paars om en om op de rand)
weg=[]
for j in range(H):
    for i in range(W):
        if zs[j,i]!=2 or o[j,i]!=7: continue
        n8=[o[j+dy,i+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=j+dy<H and 0<=i+dx<W]
        if not any(v in (7,8) for v in n8): o[j,i]=9; weg.append((i,j+7))
np.save(UIT,o); print('losse randpixels 7 -> 9:',weg)
