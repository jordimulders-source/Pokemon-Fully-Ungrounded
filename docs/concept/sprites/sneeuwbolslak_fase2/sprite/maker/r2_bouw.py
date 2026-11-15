# r2 = r1 + benoemde reparaties coordinator ronde 2 (vanuit sprite/):
#  1 modellijnen (meet/lijnkaart.txt 'L') buiten de bol: 'd' (binnenlijn), rond de rode ring '#'
#  2 bol: chaos/bevroren textuur terug uit onderlaag56 op de modelplekken, opgeschoond tot clusters >= 3; barst volgens lijnkaart
#  3 kruisvorm kop/bol: (22,36) is in het model licht -> c
import numpy as np, json
from collections import Counter
SIL=np.load('sil56_rond.npy')
R=[list(l.rstrip('\n')) for l in open('maker/raster_r1.txt')]
O=[l.rstrip('\n') for l in open('onderlaag56.txt')]
L=[l.rstrip('\n') for l in open('meet/lijnkaart.txt')]
R1=[r[:] for r in R]; reden={}
yy,xx=np.mgrid[0:64,0:64]
CIRK=((xx-31.5)**2+(yy-31.0)**2)<=10.6**2
def rand(x,y): return any(not SIL[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
# --- 2 bol ---
BINNEN=CIRK.copy()
for y in range(64):
  for x in range(64):
    if CIRK[y,x] and (R[y][x] in 'd#' or any(not CIRK[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))): BINNEN[y,x]=False
BAR=[(34,28),(36,28),(32,30),(34,30),(36,31),(32,32),(37,38),(36,25),(35,26),(35,27),(35,28),(34,29),(33,30),(32,31),(31,32),(30,33),(36,29),(36,30),(37,31),(37,32),(37,33),(36,34),(36,35),(36,36),(37,37)]
GLANS=[(27,26),(28,26),(26,27),(27,27),(25,28),(26,28)]
VAST=set(BAR)|set(GLANS)
M={'e':'w','w':'w','c':'e','b':'b','v':'b','a':'a','u':'a','d':'a','#':'a','s':'c','r':'c','t':'c'}
for y in range(64):
  for x in range(64):
    if BINNEN[y,x] and (x,y) not in VAST:
      R[y][x]=M[O[y][x]]
for (x,y) in BAR: R[y][x]='#'
for (x,y) in GLANS: R[y][x]='w'
# rechter schaduwsikkel (Gen 3, licht linksboven): binnenste pixel tegen de rechteromlijning >= a/b
for y in range(23,40):
  xs=[x for x in range(64) if BINNEN[y,x]]
  if xs:
    x=max(xs)
    if R[y][x] in 'ewc': R[y][x]='b'
# opschonen bol: tintclusters < 3 (glans uitgezonderd) -> meerderheid buren binnen de bol
def comp(x,y,c):
  st=[(x,y)]; s={(x,y)}
  while st:
    a,b=st.pop()
    for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
      p=(a+da,b+db)
      if BINNEN[p[1],p[0]] and p not in s and R[p[1]][p[0]]==c: s.add(p); st.append(p)
  return s
for it in range(6):
  ch=0
  for y in range(64):
    for x in range(64):
      if BINNEN[y,x] and (x,y) not in VAST and R[y][x] in 'abce' and len(comp(x,y,R[y][x]))<3:
        nb=[R[y+dy][x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)) if BINNEN[y+dy,x+dx] and R[y+dy][x+dx] in 'abcew' and R[y+dy][x+dx]!=R[y][x]]
        if nb:
          v,n=np.unique([k if k!='w' else 'e' for k in nb],return_counts=True); R[y][x]=v[n.argmax()]; ch+=1
  if not ch: break
# w buiten de glans: alleen houden als cluster >= 3 (sneeuwvlokken), anders e
for y in range(64):
  for x in range(64):
    if BINNEN[y,x] and R[y][x]=='w' and (x,y) not in VAST and len(comp(x,y,'w'))<3: R[y][x]='e'
# --- 1 modellijnen buiten de bol ---
RING=set((x,y) for y in range(38,46) for x in range(22,41))
for y in range(64):
  for x in range(64):
    if L[y][x]=='L' and SIL[y,x] and not CIRK[y,x] and R[y][x] not in 'd#' and not rand(x,y):
      # niet dubbel tegen de buitenrand
      if any(R[y+dy][x+dx]=='#' and rand(x+dx,y+dy) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))) and not (x,y) in RING: continue
      near_red=any(R[y+dy][x+dx] in 'rst' for dy in (-1,0,1) for dx in (-1,0,1))
      R[y][x]='#' if near_red else 'd'
# ring: linkerpunt (26-27,41) aansluiten op de ring
R[42][27]='s'
# --- 4 opschonen: tintvlakjes < 3 px -> meerderheid van buren uit dezelfde groep (glans w uitgezonderd)
G={**{k:'ijs' for k in 'abcew'},'u':'bl','v':'bl','r':'rd','s':'rd','t':'rd'}
def comp4(x,y,c):
  st=[(x,y)]; s={(x,y)}
  while st:
    a,b=st.pop()
    for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
      p=(a+da,b+db)
      if 0<=p[0]<64 and 0<=p[1]<64 and p not in s and R[p[1]][p[0]]==c: s.add(p); st.append(p)
  return s
for it in range(6):
  ch=0
  for y in range(1,63):
    for x in range(1,63):
      c=R[y][x]
      if c in 'abceuvrs' and (x,y)!=(22,36) and len(comp4(x,y,c))<3:
        nb=[R[y+dy][x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)) if G.get(R[y+dy][x+dx])==G[c] and R[y+dy][x+dx]!=c]
        if nb:
          v,n=np.unique(nb,return_counts=True); R[y][x]=v[n.argmax()]; ch+=1
  if not ch: break
# losse donkere pixels
for y in range(1,63):
  for x in range(1,63):
    if R[y][x] in 'd#' and not rand(x,y) and not any(R[y+dy][x+dx] in 'd#' for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx):
      nb=[R[y+dy][x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if R[y+dy][x+dx] in 'abce']
      v,n=np.unique(nb,return_counts=True); R[y][x]=v[n.argmax()]
# handreparaties na het opschonen
for (x,y),c in {(5,47):'e',(19,49):'u',(17,50):'u',(18,50):'u',(24,39):'d',(23,40):'d',(52,26):'d'}.items(): R[y][x]=c
# --- 3 kruisvorm ---
R[36][22]='c'
open('maker/raster_r2.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
d=sum(R[y][x]!=R1[y][x] for y in range(64) for x in range(64)); print('gewijzigd t.o.v. r1:',d)
