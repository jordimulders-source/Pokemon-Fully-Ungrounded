# Uku Pacha r4 afwerking: raster.txt -> uku_pacha_r4.png
#  - buitenlijn kleuren volgens Dragonfly Cave: zwart (K) alleen aan de schaduwkant (onder/rechts),
#    lichtkant = outline base in de donkerste eigen tint: lijf n (navy), koppen/vleugels D, geest l.
#  - koppen (handwerk in koppen.py) worden niet aangeraakt.
import numpy as np, raster2png, sys
R=[list(l) for l in raster2png.lees(sys.argv[1] if len(sys.argv)>1 else 'raster.txt')]
GH=np.load('GH.npy')
KOP=np.zeros((64,64),bool); KOP[2:28,0:23]=True; KOP[2:16,29:50]=True
def ins(x,y): return 0<=x<64 and 0<=y<64 and R[y][x]!='.'
for y in range(64):
  for x in range(64):
    if R[y][x]=='g': R[y][x]='s'
VLEUGEL=set('DB')
for y in range(64):
  for x in range(64):
    if R[y][x]=='.' or KOP[y,x]: continue
    if all(ins(x+a,y+b) for a,b in ((0,1),(0,-1),(1,0),(-1,0))): continue
    if GH[y,x]: R[y][x]='l'; continue
    nx=sum(a for a in (-1,0,1) for b in (-1,0,1) if (a or b) and not ins(x+a,y+b))
    ny=sum(b for a in (-1,0,1) for b in (-1,0,1) if (a or b) and not ins(x+a,y+b))
    schaduw = ny>0 or (ny==0 and nx>0)
    buren=[R[y+b][x+a] for a in (-1,0,1) for b in (-1,0,1) if ins(x+a,y+b)]
    vleugel=sum(c in VLEUGEL for c in buren)>=2
    kronkel = y>=43 and not vleugel   # r3: het model heeft rond de kronkels rondom een zwarte lijn
    R[y][x]='K' if (schaduw or kronkel) else ('D' if vleugel else 'n')
# ruis: 1-px tintvlekjes (geen 4-buur met dezelfde tint) -> meerderheid van de vlak-buren
BESCHERM={(9,17),(10,16),(10,17),(7,22),(7,23),(2,22),(35,6),(33,7)}  # oog, tanden, neusgat
def rand(x,y): return any(not ins(x+a,y+b) for a,b in ((0,1),(0,-1),(1,0),(-1,0)))
for it in range(3):
  for y in range(64):
    for x in range(64):
      c=R[y][x]
      if c in '.KnYPW' or (x,y) in BESCHERM or rand(x,y): continue
      n4=[R[y+b][x+a] for a,b in ((0,1),(0,-1),(1,0),(-1,0)) if ins(x+a,y+b)]
      if c in n4: continue
      vl=[v for v in n4 if v not in 'KnYPW.']
      if vl: R[y][x]=max(sorted(set(vl)),key=vl.count)
# losse lijnpunten (geen enkele lijnbuur, 8-buren) in een vlak = ruis van de verkleining -> vlaktoon
for y in range(64):
  for x in range(64):
    if R[y][x] not in 'Kn' or (x,y) in BESCHERM or rand(x,y) or KOP[y,x]: continue
    n8=[R[y+b][x+a] for a in (-1,0,1) for b in (-1,0,1) if (a or b) and ins(x+a,y+b)]
    if any(v in 'KnD' for v in n8): continue
    vl=[v for v in n8 if v not in 'KnYPW.']
    R[y][x]=max(sorted(set(vl)),key=vl.count)
# r3: 2x2-lijnklont bij de nekknik (25-26,19-20) naar 1 px trap; lijn blijft doorlopend (diagonaal)
for x,y,c in [(26,19,'s'),(25,20,'b')]:
    assert R[y][x]=='K'; R[y][x]=c
open('raster_af.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
im=raster2png.maak([''.join(r) for r in R]); im.save('uku_pacha_r4.png',transparency=0)
