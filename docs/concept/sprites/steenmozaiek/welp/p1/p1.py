# Patroonronde p1: lijfpatronen van r11 als ingekleurde vlakken die de licht/schaduw van het lijf volgen.
# Basis = r11 met de oude lijfpatronen teruggezet naar het bruin eronder (basis.py).
# Materiaalkaart per variant (tekstraster): C creme, L lila, g groef (bruin een stap donkerder), '.' bruin laten.
# Tint per pixel volgt de bruintint eronder (het facet van het lijf):
#   lila : licht/mid (5,e,4) -> 8, donker (3) -> 7, diepst (2) -> 6
#   creme: licht/mid -> b, donker/diepst -> 9
#   schaduwrand (pixel waarvan de buur onder of rechts geen zelfde materiaal is): een stap donkerder (8->7, 7->6, b->9, 9->e)
# Alleen bruinvulling (3,4,5,e) of oude patroonpixels (6,7,8,b) mogen veranderen; lijnen (1,2) en silhouet nooit.
import numpy as np
from PIL import Image
R11F='../r11/welp_r11.png'
r11=np.array(Image.open(R11F)); B=np.load('basis.npy'); PAL=Image.open(R11F).getpalette()
MAG=np.isin(r11,[3,4,5,14,6,7,8,11])
def lvl(t): return 0 if t in (5,14) else 1 if t==4 else 2 if t==3 else 3
LILA=[8,8,7,6]; CREME=[11,11,9,9]
DONK={8:7,7:6,6:6,11:9,9:14,14:14}
GROEF={14:4,5:4,4:3,3:2,2:2}
KEEP=[(17,27,10,26),(52,57,49,56)]  # voorhoofdsband en staartband blijven r11, tenzij een variant ze overschrijft
def raster(s,x0,y0):
    m={}
    for j,row in enumerate(s.strip('\n').split('\n')):
        for i,ch in enumerate(row):
            if ch in 'CLgK': m[(x0+i,y0+j)]=ch
    return m
def kleur(mat,rand=True,keep=KEEP):
    a=B.copy(); k=np.zeros_like(MAG)
    for (y0,y1,x0,x1) in keep: k[y0:y1,x0:x1]=True
    a[k]=r11[k]
    ok=lambda x,y: 0<=x<64 and 0<=y<64 and MAG[y,x]
    for (x,y),m in mat.items():
        if not ok(x,y): continue
        L=lvl(B[y,x])
        if m=='g': a[y,x]=GROEF[B[y,x]]
        elif m=='K': a[y,x]=r11[y,x]
        else: a[y,x]=(LILA if m=='L' else CREME)[L]
    if rand:
        b=a.copy()
        for (x,y),m in mat.items():
            if m not in 'CL' or not ok(x,y): continue
            # schaduwrand alleen aan de buitenkant van het patroonvlak (buur onder/rechts is bruin of lijn)
            buiten=lambda p: (p not in mat or mat[p]=='.') or not ok(*p)
            if buiten((x,y+1)) or buiten((x+1,y)): b[y,x]=DONK[a[y,x]]
        a=b
    return a
def bewaar(a,naam):
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(PAL); im.save(naam+'.png',transparency=0)
    q=Image.open(naam+'.png').convert('RGBA'); bg=Image.new('RGBA',q.size,(255,255,255,255)); bg.alpha_composite(q)
    bg.resize((512,512),Image.NEAREST).save(naam+'_8x.png')
