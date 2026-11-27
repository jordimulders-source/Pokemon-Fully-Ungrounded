# Gezicht: (1) vlakken = gez_toon (mediaan per cel, zonder dunne lijnen); (2) ogen per cel gemeten (wit/iris/pupil);
# (3) Jordi's lijnen (oogkassen, neus, ∩-mond, wanglijnen) als 1-px lijn in tint 2 (modellijntint, niet zwart) langs
#     de modelpunten (gemeten op het natieve model, omgerekend met de vergroting uit hoodgroot.py). Elke pixel benoemd in log.
import sys; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image
a=np.asarray(Image.open('../natief_g1.png').convert('RGB')).astype(float); L=lum(a)
MY,MX=np.load('basis_map.npy'); T=np.load('gez_toon.npy'); zone=np.load('gezzone.npy'); gezn=np.load('../natief_g1_gez.npy')
o=np.load('romp.npy'); oud=o.copy(); log={}
def tel(k,n=1): log[k]=log.get(k,0)+n
def S(x,y): return ((62+1.2*(x-63)-MX)/3,(16+1.28*(y-22)-MY)/3)   # origineel natief -> sprite (float)
for y in range(64):
  for x in range(64):
    if T[y,x] and o[y,x]!=1:
      if o[y,x]!=T[y,x]: o[y,x]=T[y,x]; tel('vlak: mediaan per cel')
def cel(x,y): sx,sy=S(x,y); return int(np.floor(sy)),int(np.floor(sx))
def ras(p,q):
    (y0,x0),(y1,x1)=p,q; n=max(abs(y1-y0),abs(x1-x0)); 
    return [(int(round(y0+(y1-y0)*t/n)),int(round(x0+(x1-x0)*t/n))) for t in range(n+1)] if n else [p]
import re
def lees(f): return eval(re.sub(r'#.*','',open(f).read()))
# vlakjes < 3 px in het gezicht (zelfde regel als de romp): naar de meest voorkomende 4-buurtint
from clusters import vlakjes
for it in range(2):
  for v,comp in vlakjes(o):
    for (y,x) in comp:
      if not T[y,x] or v not in (2,3,4,13): continue
      c=[o[q] for q in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)) if T[q] and o[q] in (3,4,13) and o[q]!=v]
      if c: o[y,x]=np.bincount(c).argmax(); tel('vlakje gezicht -> buurtint')
pix={c:naam for naam,pts in lees(sys.argv[1]).items() for c in pts}
for c,v in lees(sys.argv[2]).items():
    if o[c]!=v: o[c]=v; tel('oog')
np.save('lijnpix.npy',np.array([[k[0],k[1]] for k in pix]))
for (y,x),naam in pix.items():
    if o[y,x]!=2: o[y,x]=2; tel('lijn '+naam)
# dubbele zwarte rand (buitenlijn + binnenlijn zonder kaprand ertussen) en losse zwarte in het gezicht -> gezichtslijntint 2:
# zwart in de gezichtszone waarvan alle 8 buren zwart of gezicht zijn (geen kap/achtergrond) en minstens 1 gezichtstint
GZ={2,3,4,13}
for y in range(1,63):
  for x in range(1,63):
    if o[y,x]!=1 or not zone[y,x] or (y,x) in lees(sys.argv[2]): continue
    b=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
    dub=any(o[y+dy,x+dx] in GZ-{2} and o[y-dy,x-dx]==1 for dy,dx in ((0,1),(0,-1),(1,0),(-1,0)))
    if (all(v in GZ|{1} for v in b) and any(v in GZ-{2} for v in b)) or dub: o[y,x]=2; tel('zwart binnen gezicht/dubbele rand -> 2')
np.save('gez.npy',o); print(log,'gewijzigd t.o.v. romp',int((o!=oud).sum()))
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-48)); im.save('gez.png',transparency=0)
