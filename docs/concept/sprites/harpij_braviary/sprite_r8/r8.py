# r8 = r7_V2 + mond subtieler (naar Pidgeot Gen 3: korte bekscheur in een donkere randtint, geen zwarte lijn) + eindkeuring r6
import numpy as np; from pal import *
B=lees('harpij_r7_V2.txt'); r3b=lees('../sprite_r3/harpij_r3b.txt'); r3c=lees('../sprite_r3/harpij_r3c.txt'); r6b=lees('../sprite_r6/harpij_r6b.txt')
V=[tuple(p) for p in np.load('../sprite_r4/veer_mask.npy')]; O=[tuple(p) for p in np.load('../sprite_r4/oog_mask.npy')]
EIND=[(10,11,'h'),(12,7,'h'),(12,10,'h'),(44,11,'K'),(46,12,'K'),(47,16,'K')]
MOND={'min':[(18,5,'s'),(17,7,'s')],                                   # bekscheur in het midden: zwart -> s; haaktik (19,4) en eind bij de kop (17,8) blijven
      'meer':[(18,5,'s'),(17,7,'s'),(17,8,'s'),(19,4,'s')]}            # hele binnenlijn s; scherpte alleen nog in de haakomlijning
for k,m in MOND.items():
  g=B.copy(); P=[]
  for y,x,c in m+EIND:
    assert (y,x) not in V and (y,x) not in O
    if g[y,x]!=c: P.append((y,x)); g[y,x]=c
  schrijf(f'harpij_r8_{k}.txt',g)
  ok=all(g[p]==r3b[p] for p in V) and all(g[p]==r3c[p] for p in O)
  kuif=all(g[y,x]==r6b[y,x] for y in range(0,12) for x in range(38) if r6b[y,x] not in 'ghi')
  buiten=[tuple(p) for p in np.argwhere(g!=B) if tuple(p) not in [(a,b) for a,b,_ in m+EIND]]
  print(k,'buiten de punten:',buiten,'| snavelkleuren',sorted(set(g[13:22,0:9].ravel())-set(B[13:22,0:9].ravel())),'gewijzigd t.o.v. V2:',int((g!=B).sum()),'(mond',len([p for p in P if p[0]<22]),'+ eindkeuring',len([p for p in P if p[0]>=22 or p in [(10,11),(12,7),(12,10)]]),') bevroren veren+oog',ok,'| kuif B gelijk',kuif)
