# r1 = onderlaag.txt + alleen toegestane wijzigingen, elk met reden (coordinator/Jordi):
#  1 bol: handgetekende cirkel (bol_r1.txt) binnen de cirkel r10.6 + ijspunten (Jordi: "moet echt een bol blijven"; storm/barsten vereenvoudigd op modelplekken)
#  2 selout: buitenrand kop linksboven 'd' i.p.v. zwart (Gen 3: gekleurde selout aan de lichtkant)
#  3 ruis: tintvlakjes < 3 px (4-verbonden) en losse donkere pixels zonder lijnverband -> meerderheid van de buren
import numpy as np, json
SIL=np.load('sil56_rond.npy')
O=[list(l.rstrip('\n')) for l in open('onderlaag56.txt')]
R=[r[:] for r in O]; reden={}
yy,xx=np.mgrid[0:64,0:64]
BOL=(((xx-31.5)**2+(yy-31.0)**2)<=10.6**2) | ((yy<=23)&(xx>=21)&(xx<=40)&SIL)
B={}
for l in open('maker/bol_r1.txt'):
  y,t=l.split(); y=int(y)
  for i,ch in enumerate(t): B[(21+i,y)]=ch
for (x,y),ch in B.items():
  if ch!='.' and BOL[y,x] and R[y][x]!=ch: R[y][x]=ch; reden[(x,y)]='bol'
# 2 selout kop: buitenrandpixels van de kop (x<=20, y<=47) die naar boven/links aan transparant grenzen
for y in range(64):
  for x in range(21):
    if SIL[y,x] and y<=47 and R[y][x]=='#':
      if (y>0 and not SIL[y-1,x]) or (x>0 and not SIL[y,x-1]): R[y][x]='d'; reden[(x,y)]='selout'
# 4 kleurgroep blauw alleen in het bekvlak (x13-20, y45-52, zoals model); daarbuiten is u/v een verkeerd gekwantiseerde
#   lijn of schaduw: u -> d (als het in een lijnreeks ligt: buur d/#/u horizontaal) anders a; v -> b
BLAUW=set((x,y) for y in range(45,53) for x in range(13,21) if R[y][x] in 'uv')
for y in range(64):
  for x in range(64):
    if (x,y) in BLAUW or BOL[y,x]: continue
    c=R[y][x]
    if c=='u':
      lijn=sum(R[y][x+d] in 'u#d' for d in (-1,1))==2
      R[y][x]='d' if lijn else 'a'; reden[(x,y)]='blauw->ijs/lijn'
    elif c=='v': R[y][x]='b'; reden[(x,y)]='blauw->ijs/lijn'
# 2b selout bol linksboven (lichtkant): buitenrand x<=31, y<=31 die aan transparant grenst
for y in range(19,32):
  for x in range(21,32):
    if SIL[y,x] and R[y][x]=='#' and ((not SIL[y-1,x]) or (not SIL[y,x-1])): R[y][x]='d'; reden[(x,y)]='bol'
# 3 ruis
GROEP={**{k:'ijs' for k in 'abce'},'u':'blauw','v':'blauw','r':'rood','s':'rood','t':'rood','w':'glans'}
def comp(R,x,y,pred):
  st=[(x,y)]; seen={(x,y)}
  while st:
    a,b=st.pop()
    for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
      p=(a+da,b+db)
      if 0<=p[0]<64 and 0<=p[1]<64 and p not in seen and pred(R[p[1]][p[0]]): seen.add(p); st.append(p)
  return seen
for it in range(4):
  ch=0
  for y in range(64):
    for x in range(64):
      if not SIL[y,x] or BOL[y,x] or (x,y) in BLAUW: continue
      c=R[y][x]
      nb=[R[y+dy][x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y+dy<64 and 0<=x+dx<64]
      if c in 'abceuvrst':
        # groepscluster (blauw als geheel) en tintcluster
        g=GROEP[c]
        cg=comp(R,x,y,lambda k:GROEP.get(k)==g)
        ct=comp(R,x,y,lambda k:k==c)
        if len(cg)<3: pool=[k for k in nb if k in 'abce']
        elif len(ct)<3: pool=[k for k in nb if GROEP.get(k)==g and k!=c]
        else: continue
        if pool:
          v,n=np.unique(pool,return_counts=True); R[y][x]=v[n.argmax()]; reden[(x,y)]='ruis'; ch+=1
      elif c=='d' and not any(not SIL[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))):
        if not any(R[y+dy][x+dx] in 'd#' for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))):
          pool=[k for k in nb if k in 'abce']
          if pool: v,n=np.unique(pool,return_counts=True); R[y][x]=v[n.argmax()]; reden[(x,y)]='ruis'; ch+=1
  if not ch: break
# 5 handreparaties (elk met reden)
HAND=[((22,36),'#','ruis'),((22,39),'#','ruis'),
 ((18,46),'v','blauw vlak gesloten'),((17,47),'v','blauw vlak gesloten'),((18,47),'v','blauw vlak gesloten'),((19,47),'u','blauw vlak gesloten'),
 ((17,48),'u','blauw vlak gesloten'),((18,48),'u','blauw vlak gesloten'),((19,48),'u','blauw vlak gesloten'),
 ((15,49),'u','blauw vlak gesloten'),((16,49),'u','blauw vlak gesloten'),((17,49),'u','blauw vlak gesloten'),((18,49),'u','blauw vlak gesloten'),
 ((15,50),'u','blauw vlak gesloten'),((16,50),'u','blauw vlak gesloten'),((18,51),'a','ruis'),((20,51),'b','ruis'),
 ((36,41),'r','ring schaduw (model donker)'),((37,41),'r','ring schaduw (model donker)'),((37,42),'r','ring schaduw (model donker)')]
HAND+=[((x,43),'r','ring schaduw (model donker)') for x in range(27,33) if R[43][x]=='s']
for (x,y),c,r in HAND:
  if R[y][x]!=c: R[y][x]=c; reden[(x,y)]=r
# losse donkere pixels zonder lijnverband -> meerderheid buren
for y in range(1,63):
  for x in range(1,63):
    if R[y][x] in 'd#' and all(SIL[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))) and not BOL[y,x] \
       and not any(R[y+dy][x+dx] in 'd#' for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx):
      pool=[R[y+dy][x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if R[y+dy][x+dx] in 'abce']
      v,n=np.unique(pool,return_counts=True); R[y][x]=v[n.argmax()]; reden[(x,y)]='ruis'
# reden alleen houden waar echt anders dan onderlaag
reden={p:r for p,r in reden.items() if R[p[1]][p[0]]!=O[p[1]][p[0]]}
open('maker/raster_r1.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
json.dump({f'{x},{y}':r for (x,y),r in reden.items()},open('maker/diff_r1.json','w'))
from collections import Counter
print('afwijkend van onderlaag:',sum(R[y][x]!=O[y][x] for y in range(64) for x in range(64)))
print(Counter(reden.values()))
