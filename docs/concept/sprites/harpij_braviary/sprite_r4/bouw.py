# r4 bouwen: kale reductie (lijn.npy) -> tonen per zone (stap_tonen.txt) -> ruis weg -> buitenlijn -> r3-veren + r3b-oog -> handreparaties (fixes.txt)
import numpy as np; from pal import *
g=lees('stap_tonen.txt').copy(); z=lees('zones.txt'); H,W=g.shape
N4=((1,0),(-1,0),(0,1),(0,-1)); N8=N4+((1,1),(1,-1),(-1,1),(-1,-1))
def inb(y,x): return 0<=y<H and 0<=x<W
# 1. ruis: clusters (8-buren, zelfde letter) kleiner dan 3 px binnen vleugel/kop/wit/kraag -> meerderheid van de 4-buren in dezelfde zone
def ruis(g,zones,minsz=3,rondes=3):
  for _ in range(rondes):
    seen=np.zeros((H,W),bool); ch=0
    for y in range(H):
      for x in range(W):
        if seen[y,x] or g[y,x]=='.' or z[y,x] not in zones: continue
        c=g[y,x]; st=[(y,x)]; seen[y,x]=1; cl=[]
        while st:
          p=st.pop(); cl.append(p)
          for dy,dx in N8:
            q=(p[0]+dy,p[1]+dx)
            if inb(*q) and not seen[q] and g[q]==c and z[q]==z[y,x]: seen[q]=1; st.append(q)
        if len(cl)<minsz:
          for p in cl:
            nb=[g[p[0]+dy,p[1]+dx] for dy,dx in N8 if inb(p[0]+dy,p[1]+dx) and g[p[0]+dy,p[1]+dx] not in ('.',c) and z[p[0]+dy,p[1]+dx]==z[p]]
            if nb: g[p]=max(set(nb),key=nb.count); ch+=1
    if not ch: break
  return g
g=ruis(g,'whbn')
# 2. buitenlijn 1 px: randpixel (4-buur transparant) -> K aan de schaduwkant, selout (donkerste tint van de zone) aan de lichtkant (alleen boven/links open)
SEL={'k':'a','w':'a','h':'g','b':'h','s':'s','p':'s','n':'K'}
o=g.copy()
for y in range(H):
  for x in range(W):
    if g[y,x]=='.': continue
    op=[(dy,dx) for dy,dx in N4 if not inb(y+dy,x+dx) or g[y+dy,x+dx]=='.']
    if not op: continue
    licht=all(d in ((-1,0),(0,-1)) for d in op)
    o[y,x]=SEL.get(z[y,x],'K') if licht and g[y,x]!='K' else 'K'
g=o
schrijf('stap_lijn.txt',g)
# 3. bevroren uit r3: twee meest rechtse kuifveren; oog variant b
r3=lees('../sprite_r3/harpij_r3b.txt')
VEER=[(y,x) for y in range(6,9) for x in range(21,28)]+[(9,x) for x in range(20,28)]+[(10,x) for x in range(22,28)]+[(y,x) for y in range(11,14) for x in range(21,28)]+[(12,20)]
OOG=[(14,x) for x in range(8,13)]+[(y,x) for y in range(15,17) for x in range(9,13)]+[(17,x) for x in range(9,12)]
r3c=lees('../sprite_r3/harpij_r3c.txt')  # oog c (Jordi: "oog c")
for p in VEER: g[p]=r3[p]
for p in OOG: g[p]=r3c[p]
np.save('veer_mask.npy',np.array(VEER)); np.save('oog_mask.npy',np.array(OOG))
schrijf('stap_r3.txt',g)
# 4. handreparaties: regels "y x letters  # reden" (letters vanaf x naar rechts)
import re
for r in open('fixes.txt'):
  r=r.split('#')[0].strip()
  if not r: continue
  y,x,s=r.split(); y,x=int(y),int(x)
  for i,c in enumerate(s): g[y,x+i]=c
schrijf('harpij_r4.txt',g)
