# Uku Pacha r5 borst: lichte voorkant van beide nekken opnieuw opgebouwd.
#  1. zone = spritepixels waarvan de voetafdruk op het natieve model >= 40% licht is (lum 150-240),
#     binnen x 13-45 / y 17-58, geen r3-lijn (K/n in r3), geen buitenrand, geen vleugel/kop.
#  2. r4-borstlijnstukjes (lijnpixels die r4 toevoegde, niet in r3) in de zone -> vlak.
#  3. vlak per pixel naar de modeltint van zijn plaat (oppervlak-gewogen mediaan van de lichte
#     cellen in de voetafdruk): >= 205 w, >= 172 p, anders l.
#  4. elke plaatgrens uit platen.py als doorlopende 1 px lijn op de gemeten plek; tint naar de
#     modelkleur van die lijn (s / d / n). In het medium vlak naast de band loopt de lijn door
#     (alleen waar daar geen lijn ligt); r4-lijnpixels die 1 px naast de nieuwe lijn lagen
#     (dezelfde lijn, verschoven of dubbel) gaan naar het vlak eromheen.
import numpy as np, zone, platen
R4=[list(l.rstrip('\n')) for l in open('../r4/raster_af.txt')][:64]
R3=[l.rstrip('\n') for l in open('../r3/raster_af.txt')][:64]
R=[r[:] for r in R4]
LIJN='Kn'
def ins(x,y): return 0<=x<64 and 0<=y<64 and R4[y][x]!='.'
def rand(x,y): return any(not ins(x+a,y+b) for a,b in ((0,1),(0,-1),(1,0),(-1,0)))
Z=np.zeros((64,64),bool)
for y in range(17,59):
  for x in range(13,46):
    if not ins(x,y) or rand(x,y) or R3[y][x] in 'DBhYPW' or R3[y][x] in LIJN: continue
    if zone.lichtfrac(x,y)>=0.4: Z[y,x]=True
def tint(x,y):
    t=zone.toon(x,y)
    if t is None: return None
    return 'w' if t>=205 else ('p' if t>=172 else 'l')
# 2+3: vlak
for y in range(64):
  for x in range(64):
    if Z[y,x]:
      t=tint(x,y)
      if t: R[y][x]=t
# 4: lijnen
NIEUW={}
for naam,pts,tl,tm in platen.LIJNEN:
    if naam in ('R-a','R-b','LA','LB'): continue    # medium voorkant: r3/r4-lijnen liggen al op de modelplek
    for (x,y) in platen.raster(pts,naam):
        if not ins(x,y) or rand(x,y) or R3[y][x] in 'DBhYPW': continue
        if Z[y,x]: NIEUW[(x,y)]=tl
        elif R[y][x] not in 'Kn' : NIEUW[(x,y)]=tm
        else: NIEUW[(x,y)]=R[y][x]   # ligt al een lijn: houden
# r4-lijnpixels buiten de zone die direct naast een nieuwe lijn liggen en niet in r3 stonden
# (zelfde lijn, 1 px verschoven) -> vlaktoon van de buren
weg=[]
for y in range(64):
  for x in range(64):
    if Z[y,x] or (x,y) in NIEUW: continue
    if R4[y][x] in 'nd' and R3[y][x]!=R4[y][x] and R3[y][x] not in 'Kn' and 13<=x<=45 and 17<=y<=58:
        if any((x+a,y+b) in NIEUW for a in (-1,0,1) for b in (-1,0,1)): weg.append((x,y))
for x,y in weg: R[y][x]=R3[y][x]
for (x,y),t in NIEUW.items(): R[y][x]=t
# r3-randlijn in D-tint op de rechterband: (30,28) is de bandrand (model (48,44) zwart) -> n;
# (30,29) ligt op L2 -> lijntint van L2
R[28][30]='n'; R[29][30]='s'
# R-b (rechternek voorkant, model (61,30)-(67,30)): r3/r4 hadden hem dubbel ((40,18) r4 erbij,
# (42,19) hoekpixel naast (41,19)/(42,18)); één doorlopende 1 px lijn: (38-39,18) (40-41,19) (42-44,18)
R[18][40]='b'; R[19][42]='b'
# 2x2-klonten: (26,42) is B in het medium vlak -> r3-tint d (zoals B daar in r3: (23-25,42) d);
# (8,58) dubbelde de buitenlijn (r4 n, r3 d); het modelstompje (16,88)-(17,89) blijft als (7,58)
R[42][26]='d'; R[58][8]='d'
# E: de r4-stompjes naast de lijn ((19,58) en (24,59), model daar medium 133) -> b
R[58][19]='b'; R[59][24]='b'
# rechterkronkel: (34-36,50) is in het model donker (lum 50-65) onder het lichte gaatje (rij 49);
# r4 had er b (lichte vlek 2 rijen hoog) -> d
for x in (34,35,36): R[50][x]='d'
# 5. tintvlakjes van 1-2 px in de zone (geen lijn) -> meerderheid van de vlakburen
for it in range(3):
  gezien=set()
  for y in range(64):
    for x in range(64):
      c=R[y][x]
      if not Z[y,x] or c not in 'wpl' or (x,y) in gezien or (x,y) in NIEUW: continue
      cl=[(x,y)]; st=[(x,y)]; gezien.add((x,y))
      while st:
        a_,b_=st.pop()
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
          u,v=a_+dx,b_+dy
          if 0<=u<64 and 0<=v<64 and (u,v) not in gezien and R[v][u]==c and Z[v,u]:
            gezien.add((u,v)); cl.append((u,v)); st.append((u,v))
      if len(cl)>2: continue
      rond=[R[v+dy][u+dx] for u,v in cl for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if (u+dx,v+dy) not in cl]
      vl=[t for t in rond if t in 'wplb']
      if vl:
        t=max(sorted(set(vl)),key=vl.count)
        for u,v in cl: R[v][u]=t
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
np.save('zone.npy',np.array([(x,y) for y in range(64) for x in range(64) if Z[y,x]]))
print('zone',int(Z.sum()),'nieuwe lijnpixels',len(NIEUW),'terug naar r3',weg)
