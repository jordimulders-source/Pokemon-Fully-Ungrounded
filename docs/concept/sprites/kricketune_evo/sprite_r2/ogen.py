# r2 oogvarianten (Jordi op r1: "let op de positie van het linker oog" / "die is niet natuurlijk").
# Basis = r1 hoofdversie; alleen het verre oog verandert. Stap 1: oogplek terug naar het model (kopomlijning x24 zwart, selout x25
# donkerrood zoals erboven, binnenin rood licht zoals de buren). Stap 2: Kricketune-oog (frame 1, of frame 2) binnen de kop, met rood
# tussen oog en kopomlijning. Bouwen: cd kricketune_evo && python3 sprite_r2/ogen.py
import sys, numpy as np; sys.path.insert(0,'gereedschap'); from gemeen import *; from PIL import Image
r1=laden('sprite_r1/kricketune_evo_r1.png'); KT=np.asarray(Image.open('../../../../graphics/pokemon/kricketune/anim_front.png')).astype(int)
KTM={4:1,5:2,6:12,7:6}
basis=r1.copy()
for y in range(13,18):
    basis[y,24]=1; basis[y,25]=7
    for x in range(26,30):
        if basis[y,x] in (1,2,6,12): basis[y,x]=10
basis[13,25]=7
def plak(o,ky0,ky1,kx0,kx1,dx,dy):
    for y in range(ky0,ky1):
        for x in range(kx0,kx1):
            if KT[y,x] in KTM: o[y+dy,x+dx]=KTM[KT[y,x]]
V={'A':('frame 1, 2 px naar binnen (x27-30), zelfde hoogte als r1',(20,24,24,28,3,-6)),
   'B':('frame 1, 2 px naar binnen, 1 px hoger (glans/pupil op de hoogte van het nabije oog)',(20,24,24,28,3,-7)),
   'C':('frame 2 (verre oog binnen de kop), 2 px naar binnen, pupil op de hoogte van het nabije oog',(81,86,25,29,2,-68))}
for n,(t,(ky0,ky1,kx0,kx1,dx,dy)) in V.items():
    o=basis.copy(); plak(o,ky0,ky1,kx0,kx1,dx,dy); opslaan(o,'sprite_r2/oog_%s.png'%n)
    d=(o!=r1); print(n,t,'| anders dan r1:',int(d.sum()),'px, buiten x24-31 y12-18:',int(d.sum()-d[12:19,24:32].sum()))
    toon(o,y0=11,y1=19,x0=22,x1=38)
