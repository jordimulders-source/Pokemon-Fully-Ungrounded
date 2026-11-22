# Bewijs r9: silhouet-verschil t.o.v. r8-P1 (alleen linker armaanzet), kop 0 verschil, creme ledematen/strepen 0 verschil.
import numpy as np; from PIL import Image
from gen import stuk
def rgba(f): return np.asarray(Image.open(f).convert('RGBA')).astype(int)
r8=rgba('../sprite_r8/astro_P1.png'); a8=r8[...,3]>0
for v in range(1,6):
    im=Image.open('astro_V%d.png'%v); n=len(im.getpalette())//3 if False else len(set(np.asarray(im).ravel()))
    x=rgba('astro_V%d.png'%v); a=x[...,3]>0
    sd=np.argwhere(a!=a8)
    kop=(np.abs(x[:26]-r8[:26]).sum(-1)>0).sum()          # rijen 0-25: kop + bovenkant hand
    rest=np.array([[not stuk[j,i] and not (26<=j<=30 and 24<=i<=30) for i in range(64)] for j in range(64)])
    d=(np.abs(x-r8).sum(-1)>0)&rest
    sel=sum(1 for j,i in np.argwhere(d) if any(stuk[j+p,i+q] for p,q in ((0,1),(1,0),(0,-1),(-1,0))))
    ander=d.sum()-sel                                      # alles buiten tuniek, tuniek-buitenlijn en armaanzet
    print('V%d: %d kleuren (incl. transparant) | silhouet-verschil %d px: %s | kop rijen 0-25: %d px | selout op tuniekrand: %d px | verder: %d px'
          %(v,n,len(sd),[(int(c),int(r)) for r,c in sd],kop,sel,ander))

# silhouetbewijs als plaatje: zwart = r8 en r9, rood = alleen r9 (erbij), blauw = alleen r8 (eraf)
x=rgba('astro_V1.png'); a=x[...,3]>0; S=12; Y0,Y1,X0,X1=20,38,14,46
out=Image.new('RGB',((X1-X0)*S,(Y1-Y0)*S),(240,240,236)); px=out.load()
for j in range(Y0,Y1):
    for i in range(X0,X1):
        c=(60,60,60) if a[j,i] and a8[j,i] else (220,40,40) if a[j,i] else (40,80,220) if a8[j,i] else (240,240,236)
        for p in range(S):
            for q in range(S): px[(i-X0)*S+q,(j-Y0)*S+p]=c if (p and q) else (200,200,200)
out.save('silhouet_diff.png')
