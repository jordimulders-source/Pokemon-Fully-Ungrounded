# Uku Pacha r5 scherper: een middentoon die als 1 px brede strook tussen een lichtere en een donkerdere
# vlaktoon ligt (tegenoverliggende 4-buren: links/rechts of boven/onder), is waas van de verkleining.
# Zo'n pixel krijgt de tint van de buur waarvan de helderheid het dichtst bij het model op die plek ligt
# (mediaan van de voetafdruk op het natieve model): een harde toongrens op de modelplek.
# Lijnen (K/n), ogen, tong, tanden, geest en de borstzone (net opgebouwd) worden niet aangeraakt.
import numpy as np, modmed, sys
R=[list(l.rstrip('\n')) for l in open(sys.argv[1])][:64]
GH=np.load('GH.npy')
LUM={'d':82,'s':105,'m':132,'b':145,'l':160,'p':193,'w':220,'D':76,'B':110,'h':164}
LIJF='dsmblpw'; KOPV='DBh'
RAMP={t:(LIJF if t in LIJF else KOPV) for t in LUM}
VAST=set()
for y in range(64):
  for x in range(64):
    if R[y][x] in 'YPW': VAST|={(x+a,y+b) for a in (-1,0,1) for b in (-1,0,1)}
VAST|={(9,17),(10,16),(10,17),(11,16),(11,17),(12,16),(7,22),(7,23),(2,22),(35,6),(33,7)}
ZONE=set(map(tuple,np.load('zone.npy').tolist())) if len(sys.argv)>3 else set()
def ins(x,y): return 0<=x<64 and 0<=y<64
gewijzigd=[]
for ronde in range(2):
  for y in range(64):
    for x in range(64):
      c=R[y][x]
      if c not in LUM or GH[y,x] or (x,y) in VAST or (x,y) in ZONE: continue
      # niet naast de buitenrand of de randlijn (anders wordt de omlijning dubbel)
      if any(not ins(x+a,y+b) or R[y+b][x+a]=='.' or (R[y+b][x+a] in 'Dn' and any(not ins(x+a+e,y+b+f) or R[y+b+f][x+a+e]=='.' for e in (-1,0,1) for f in (-1,0,1))) for a in (-1,0,1) for b in (-1,0,1)): continue
      for (a1,b1),(a2,b2) in (((-1,0),(1,0)),((0,-1),(0,1))):
        if not(ins(x+a1,y+b1) and ins(x+a2,y+b2)): continue
        u,v=R[y+b1][x+a1],R[y+b2][x+a2]
        if u not in LUM or v not in LUM: continue
        lo,hi=sorted((u,v),key=LUM.get)
        # alleen binnen één ladder (lijf d..w, kop/vleugel D-B-h); anders is het geen waas maar een grens
        if not all(t in RAMP[c] for t in (lo,hi)): continue
        if LUM[lo]<LUM[c]<LUM[hi]:
          m=modmed.med(x,y)
          t=lo if abs(m-LUM[lo])<abs(m-LUM[hi]) else hi
          # niet als het een los vlakje van 1 px zou maken: de nieuwe tint moet een 4-buur hebben
          # geen nieuw los vlakje: een 4-buur met de oude tint mag zijn laatste gelijke 4-buur niet verliezen
          def los(u,v):
            return R[v][u]==c and not any(0<=u+e<64 and 0<=v+f<64 and (u+e,v+f)!=(x,y) and R[v+f][u+e]==c for e,f in ((1,0),(-1,0),(0,1),(0,-1)))
          if any(los(x+e,y+f) for e,f in ((1,0),(-1,0),(0,1),(0,-1)) if ins(x+e,y+f)): continue
          R[y][x]=t; gewijzigd.append((x,y,c,t)); break
open(sys.argv[2],'w').write('\n'.join(''.join(r) for r in R)+'\n')
print(len(gewijzigd),'px scherper:',gewijzigd)
