# Gaucho-Lombre r3: basis = r2 B (hoofd en mond A5 blijven). Alleen de twee ogen, naar de Lombre-artwork/anime/3D
# (referenties/): rond wit oog, bovenkant afgedekt door een rechte dikke zwarte ooglidlijn, zichtbaar wit = onderhelft,
# kleine zwarte pupil direct onder het lid. "Bozer" (Jordi) = lid loopt schuin af naar de snuit (links).
# Oogvakken: nabij x29-34 y25-28 (rand x35 = model, blijft), ver x21-22 y24-26. Buiten die vakken pixelgelijk aan r2 B.
import numpy as np; from PIL import Image
from gemeen import opslaan
B2=np.array(Image.open('../r2/lombre_gaucho_r2_B.png')).astype(int)
K,W,L,F=1,15,2,4   # zwart, wit, rood lijn (onderrand van het oog, binnenlijn), gezicht rood midden
def raster(rijen,x0,y0):
    d={}
    for j,r in enumerate(rijen):
        for i,c in enumerate(r.split()):
            d[(y0+j,x0+i)]={'K':K,'W':W,'L':L,'F':F}[c]
    return d
# ver oog (alle varianten): lid 2 px zwart, pupil rechts onder het lid (naar de kijker), wit eronder
VER=raster(['K K',
            'W K',
            'W W'],21,24)
NABIJ={
 # A: lid bijna vlak (1 trede naar de snuit), pupil midden onder het lid
 'A':raster(['F F K K K K',
             'L K W K W W',
             'L W W W W L',
             'F L W W L F'],29,25),
 # B: lid duidelijk schuin (3 treden naar de snuit), pupil direct onder het lid
 'B':raster(['F F F F K K',
             'F L K K W W',
             'L K W K W L',
             'F L W W L F'],29,25),
 # C: als A (bijna vlak), maar pupil vooraan tegen het lid (naar de snuit), zoals de linkerpupil op de artwork
 'C':raster(['F F K K K K',
             'L K K W W W',
             'L W W W W L',
             'F L W W L F'],29,25),
}
if __name__=='__main__':
    log=open('pixels.txt','w')
    for n,nab in NABIJ.items():
        o=B2.copy()
        for (y,x),k in {**VER,**nab}.items(): o[y,x]=k
        opslaan(o,'lombre_gaucho_r3_%s.png'%n)
        d=np.argwhere(o!=B2)
        buiten=[(x,y) for y,x in d if not((21<=x<=22 and 24<=y<=26) or (29<=x<=34 and 25<=y<=28))]
        print(n,'verschil met r2 B: %d px; buiten de oogvakken: %d; kleuren %d'%(len(d),len(buiten),len(set(o.ravel()))))
        for y,x in d: log.write('%s (%d,%d) %d->%d\n'%(n,x,y,B2[y,x],o[y,x]))
