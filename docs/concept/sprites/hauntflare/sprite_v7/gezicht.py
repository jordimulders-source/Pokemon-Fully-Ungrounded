# v7-gezicht: linkeroog = gespiegeld rechteroog van v6, verkort door kolommen te schrappen;
# mond = v6-mond (Haunters mondpixels) verschoven en verkort. Niets getekend.
import numpy as np
from PIL import Image
import os
D=os.path.dirname(os.path.abspath(__file__)); H=os.path.dirname(D)
V6=Image.open(H+'/sprite_v6/hauntflare_v6.png'); PAL=V6.getpalette()
a6=np.array(V6).astype(int); st1=np.load(H+'/sprite_v2/stap1_kleur.npy').astype(int)
msk=np.load(H+'/sprite_v2/gezicht_masker.npy')
# gezichtspixels van v6: masker + door v6 zwart gemaakte mondlijn
F=np.zeros((64,64),bool)
for y in range(20,39):
    for x in range(17,40):
        if msk[y,x] or (a6[y,x]!=st1[y,x] and a6[y,x] in (1,2,10,14)): F[y,x]=True
def blok(x0,x1,y0,y1):  # waarden, None = niet van het gezicht
    return [[(a6[y,x] if F[y,x] else None) for x in range(x0,x1+1)] for y in range(y0,y1+1)]
RECHTEROOG=blok(27,38,23,29)        # x27-38, y23-29
LINKEROOG_OUD=(17,26,20,29)
MOND=(21,39,30,37)
def mondblok():
    x0,x1,y0,y1=MOND; g=[]
    for y in range(y0,y1+1):
        xs=[x for x in range(x0,x1+1) if F[y,x]]
        rij=[]
        for x in range(x0,x1+1):
            if F[y,x]: rij.append(a6[y,x])
            else:
                # tand = bolpixel binnen de mondomtrek (rij- en kolomgrenzen)
                ys=[yy for yy in range(y0,y1+1) if F[yy,x]]
                binnen = xs and min(xs)<x<max(xs) and ys and min(ys)<y<max(ys)
                rij.append(('T',a6[y,x]) if binnen else None)
        g.append(rij)
    return g
def basis():
    a=a6.copy()
    for y in range(64):
        for x in range(64):
            if F[y,x] and not (27<=x<=38 and 23<=y<=29): a[y,x]=st1[y,x]     # vrijgekomen bolpixels uit stap1 (rechteroog blijft)
    return a
def plak(a,g,x0,y0,tand_kleur='mee'):
    for j,rij in enumerate(g):
        for i,v in enumerate(rij):
            if v is None: continue
            x,y=x0+i,y0+j
            if isinstance(v,tuple): a[y,x]= v[1] if tand_kleur=='mee' else (a[y,x] if a[y,x] in (7,8,9) else v[1])
            else: a[y,x]=v
def spiegel(g): return [list(reversed(r)) for r in g]
def schrap_kol(g,ks): return [[v for i,v in enumerate(r) if i not in ks] for r in g]
def schrap_rij(g,ks): return [r for j,r in enumerate(g) if j not in ks]
def kolom_schuif(g,schuif):   # schuif[i] = rijen omlaag (+) voor kolom i
    h=len(g)+max(0,max(schuif))-min(0,min(schuif)); w=len(g[0]); off=-min(0,min(schuif))
    n=[[None]*w for _ in range(h)]
    for j,r in enumerate(g):
        for i,v in enumerate(r):
            if v is not None: n[j+schuif[i]+off][i]=v
    return n,off
def toon(g):
    return '\n'.join(''.join('.' if v is None else ('t' if isinstance(v,tuple) else '%x'%v) for v in r) for r in g)
def bewaar(a,naam):
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(PAL); im.save(naam,transparency=0)
    return Image.open(naam)
if __name__=='__main__':
    print(toon(RECHTEROOG)); print(); print(toon(spiegel(RECHTEROOG))); print(); print(toon(mondblok()))
