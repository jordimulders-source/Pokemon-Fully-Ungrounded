# Gaucho-Lombre r4: basis = r3 A (lid van A blijft: bijna vlak, 1 trede). Jordi: "a is het beste maar de blik is niet naar driekwart".
# Alleen pupilplaats; het verre oog wordt 3 px breed (x21-23) zodat de pupil een plek binnen het wit kan hebben.
# Studie Gen 3 (anim_front_gba): Ludicolo = pupil midden in beide ogen (W-zwart-W), kijkt naar de kijker; Nuzleaf (halfgesloten
# lid, driekwart links) = pupil vooraan (naar de snuit) direct onder het lid; gaucho-Lotad G (Jordi's keuze) = nabij midden, ver stip rechts.
# Oogvakken: nabij x29-34 y25-28, ver x21-23 y24-26. Buiten die vakken pixelgelijk aan r3 A.
import numpy as np; from PIL import Image
from gemeen import opslaan
B=np.array(Image.open('../r3/lombre_gaucho_r3_A.png')).astype(int)
K,W,L,F=1,15,2,4
def raster(rijen,x0,y0):
    return {(y0+j,x0+i):{'K':K,'W':W,'L':L,'F':F}[c] for j,r in enumerate(rijen) for i,c in enumerate(r.split())}
def nabij(px):   # lid van r3 A; pupil op x=px in rij 26 (direct onder het lid), wit x31-34
    rij=['W']*4; rij[px-31]='K'
    return raster(['F F K K K K','L K '+' '.join(rij),'L W W W W L','F L W W L F'],29,25)
def ver(px):     # 3 breed: lid x21-23, pupil op x=px in rij 25, wit eromheen, ronde onderkant (L rechtsonder)
    rij=['W']*3; rij[px-21]='K'
    return raster(['K K K',' '.join(rij),'W W L'],21,24)
VAR={
 'A':(32,22,'nabij x32 (net vóór het midden, = r3 A), ver x22 (midden): beide licht vóór de sprite uit'),
 'B':(33,23,'nabij x33 (net achter het midden), ver x23 (rechts): beide naar de kijker (zoals Lotad G / Ludicolo)'),
 'C':(31,21,'nabij x31 (vooraan tegen het lid), ver x21 (links): beide naar voren, zoals Nuzleaf'),
}
if __name__=='__main__':
    log=open('pixels.txt','w')
    for n,(pn,pv,uitleg) in VAR.items():
        o=B.copy()
        for (y,x),k in {**ver(pv),**nabij(pn)}.items(): o[y,x]=k
        opslaan(o,'lombre_gaucho_r4_%s.png'%n)
        d=np.argwhere(o!=B)
        buiten=[(x,y) for y,x in d if not((21<=x<=23 and 24<=y<=26) or (29<=x<=34 and 25<=y<=28))]
        print(n,uitleg,'| verschil met r3 A: %d px; buiten de oogvakken: %d; kleuren %d'%(len(d),len(buiten),len(set(o.ravel()))))
        for y,x in d: log.write('%s (%d,%d) %d->%d\n'%(n,x,y,B[y,x],o[y,x]))
