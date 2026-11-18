"""Icoonmaten per groep: vanilla Gen 1-3 (icon_gba.png) vs fanmade Gen 9 (icon.png).
python3 icoon_groepen.py"""
import os,re,sys,numpy as np
from PIL import Image
sys.path.insert(0,os.path.dirname(__file__)); import vorm_meet as V
G='graphics/pokemon'
def pal(p):
    L=open(p).read().split('\n'); n=int(L[2]); return np.array([[int(v) for v in L[3+k].split()[:3]] for k in range(n)]+[[0,0,0]]*(16-n))
gen={}; IPI={}
for g in range(1,10):
    t=open(f'src/data/pokemon/species_info/gen_{g}_families.h').read()
    for mm in re.finditer(r'\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},',t,re.S):
        sp=mm.group(1).lower(); gen[sp]=g
        v=re.search(r'iconPalIndex = (?:P_GBA_STYLE_SPECIES_ICONS \? \d : )?(\d)',mm.group(2))
        if v: IPI[sp]=int(v.group(1))
def metr(ix,P):
    f1=ix[:32]; f2=ix[32:64]; m=f1>0
    if not m.any(): return None
    lum=P.mean(1); ys,xs=np.nonzero(m)
    pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
    dk=lum[f1]<110; s=V.stats(f1,P)
    best=min(((np.roll(np.roll(f1,dy,0),dx,1)!=f2).sum() for dy in range(-2,3) for dx in range(-2,3)))/m.sum()
    return dict(h=ys.max()-ys.min()+1,w=xs.max()-xs.min()+1,bot=ys.max(),area=m.sum(),kleuren=len(np.unique(f1[m])),
                binnen=(dk&m&~edge).sum()/m.sum(),vlakken=s[1],gaten=s[2],f2=best,
                omlijn_donker=(dk&edge).sum()/edge.sum())
rows={'vanilla 1-3':[], 'in-game 1-3':[], 'fanmade gen 9':[]}
for sp in sorted(os.listdir(G)):
    d=f'{G}/{sp}'
    if os.path.exists(d+'/icon_gba.png'):
        im=Image.open(d+'/icon_gba.png'); r=metr(np.array(im),np.array(im.getpalette()[:48]).reshape(16,3))
        if r: rows['vanilla 1-3'].append(r)
    if gen.get(sp) in (1,2,3) and os.path.exists(d+'/icon.png'):
        r=metr(np.array(Image.open(d+'/icon.png')),pal('graphics/pokemon/icon_palettes/pal%d.pal'%IPI.get(sp,0)))
        if r: rows['in-game 1-3'].append(r)
    if gen.get(sp)==9 and os.path.exists(d+'/icon.png'):
        r=metr(np.array(Image.open(d+'/icon.png')),pal('graphics/pokemon/icon_palettes/pal%d.pal'%IPI.get(sp,0)))
        if r: rows['fanmade gen 9'].append(r)
keys=list(rows['vanilla 1-3'][0])
print('maat'.ljust(14),*[f'{k} (n={len(v)}) p10/med/p90'.ljust(26) for k,v in rows.items()])
for k in keys:
    print(k.ljust(14),*[('%.2f / %.2f / %.2f'%tuple(np.percentile([r[k] for r in v],[10,50,90]))).ljust(26) for v in rows.values()])
