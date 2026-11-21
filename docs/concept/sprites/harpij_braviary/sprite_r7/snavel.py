# snavelvarianten op r6b; alleen snavelzone (rij 13-22, kolom 0-9, zonder oogmasker); 'v' = nieuw donker staal (88,104,126)
import numpy as np; from pal import *
B=lees('harpij_r6b.txt'); r3=lees('../sprite_r3/harpij_r3c.txt')
O=set(tuple(p) for p in np.load('../sprite_r4/oog_mask.npy')); V=set(tuple(p) for p in np.load('../sprite_r4/veer_mask.npy'))
ZONE={(y,x) for y in range(13,23) for x in range(0,10)}-O
def bouw(rows):
  g=B.copy()
  for y,x,s in rows:
    for i,c in enumerate(s):
      if c!='#': g[y,x+i]=c
  return g
# vorm gemeten op model_natief: bovenrand-boog (24,30)->(30,26), voorrand x=26 r29-33, haakpunt (34-35, x27-29), onderrand r33 x29-33 die naar het oog oploopt
# opbouw naar Braviary/Pidgeot: rustig lijf, lichte rug, donkere onderkant; scherpte alleen met haakpunt + kort oplopende onderrand (geen rechte streep)
V1=[(14,4,'sttv'),(15,3,'stvvvs'),(16,2,'stvvvvs'),(17,1,'suvvvvvs'),(18,1,'stvvvvssg'),(19,1,'stvssKKK'),(20,1,'.KsKKg'),(21,3,'K')]
V3=[(14,4,'.stv'),(15,3,'.stvvs'),(16,2,'.stvvvs'),(17,1,'.suvvvvs'),(18,1,'.stvvvssg'),(19,1,'.stvsKKK'),(20,1,'..KsKg'),(21,3,'.K')]
# V4: vorm V1, alleen bestaande tinten zoals Braviary in twee helften: bovenhelft t (rug u), onderhelft s (rug t)
V4=[(14,4,'sutt'),(15,3,'suttts'),(16,2,'suttts'+'s'),(17,1,'sussssss'),(18,1,'stssssssg'),(19,1,'stsssKKK'),(20,1,'.KsKKg'),(21,3,'K')]
# V2: snavelpixels uit r3c (s,t,u,W,K en leeg) in rij 14-21 kolom 0-8; kopkleuren van r3c niet
V2=[]
for y in range(14,22):
  for x in range(0,9):
    if (y,x) in O: continue
    c=r3[y,x]
    if c in 'sutWK.' and not (y>=20 and x>=5): V2.append((y,x,c))
v2=B.copy()
for y,x,c in V2: v2[y,x]=c
# aansluiting: r3c had de snavelonderkant bij (18,9)/(19,8); kop eronder aansluiten
v2[18,9]='g'; v2[20,6]='g'  # aansluiting: onder de r3-snavel kop i.p.v. de oude r6-onderlijn
res={'V1':bouw(V1),'V2':v2,'V3':bouw(V3),'V4':bouw(V4)}
for k,g in res.items():
  d=np.argwhere(g!=B); buiten=[tuple(p) for p in d if tuple(p) not in ZONE]
  schrijf(f'harpij_r7_{k}.txt',g)
  print(k,'gewijzigd',len(d),'buiten zone',buiten,'| oog ok',all(g[p]==B[p] for p in O),'| veren ok',all(g[p]==B[p] for p in V),'| kleuren',len(set(g.ravel())-{'.'}))
  for y in range(13,23): print('   %2d '%y+''.join(g[y][:13]))
