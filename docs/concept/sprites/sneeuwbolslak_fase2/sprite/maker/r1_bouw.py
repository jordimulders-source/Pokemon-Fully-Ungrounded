# r1 = onderlaag.txt + alleen toegestane wijzigingen, elk met reden (coordinator/Jordi):
#  1 bol: handgetekende cirkel (bol_r1.txt) binnen de cirkel r10.6 + ijspunten (Jordi: "moet echt een bol blijven"; storm/barsten vereenvoudigd op modelplekken)
#  2 selout: buitenrand kop linksboven 'd' i.p.v. zwart (Gen 3: gekleurde selout aan de lichtkant)
#  3 ruis: tintvlakjes < 3 px (4-verbonden) en losse donkere pixels zonder lijnverband -> meerderheid van de buren
import numpy as np, json
SIL=np.load('sil56_rond.npy')
O=[list(l.rstrip('\n')) for l in open('maker/onderlaag.txt')]
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
# 4 blauw vlak bij de bek: de onderlaag mapte het verzadigde blauw van het model naar ijs (te donker paletblauw);
#   terug op de gemeten modelpixels (B-R >= 85, x14-19, y46-51), dichtstbijzijnde van u/v
exec(open('meet/px.py').read().split('if __name__')[0].replace("'sprite/r8","'r8"))
import sys; sys.path.insert(0,'maker'); from pal import PAL
BLAUW=set()
for y in range(46,52):
  for x in range(14,20):
    b,l=blok(x,y); m=b.reshape(-1,3).mean(0)
    if m[2]-m[0]>=85:
      k=min('uv',key=lambda k:((np.array(PAL[k])-m)**2).sum())
      BLAUW.add((x,y))
      if R[y][x]!=k: R[y][x]=k; reden[(x,y)]='blauw'
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
# reden alleen houden waar echt anders dan onderlaag
reden={p:r for p,r in reden.items() if R[p[1]][p[0]]!=O[p[1]][p[0]]}
open('maker/raster_r1.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
json.dump({f'{x},{y}':r for (x,y),r in reden.items()},open('maker/diff_r1.json','w'))
from collections import Counter
print('afwijkend van onderlaag:',sum(R[y][x]!=O[y][x] for y in range(64) for x in range(64)))
print(Counter(reden.values()))
