# r1 bouwen: kale reductie (kaal.txt) -> ruis weg -> buitenlijn (K schaduwkant, selout lichtkant) -> handreparaties (fixes.txt)
import numpy as np, re, sys; from pal import *
g=lees('kaal.txt').copy(); H,W=g.shape
N4=((1,0),(-1,0),(0,1),(0,-1)); N8=N4+((1,1),(1,-1),(-1,1),(-1,-1))
inb=lambda y,x: 0<=y<H and 0<=x<W
FAM={'W':'H','w':'H','v':'H','u':'H','c':'G','b':'G','a':'G','y':'Y','e':'Y','d':'Y','n':'D','K':'K','.':'.'}
f=np.vectorize(FAM.get)(g)
def ruis(g,lets,minsz=3,rondes=3):
  for _ in range(rondes):
    seen=np.zeros((H,W),bool); ch=0
    for y in range(H):
      for x in range(W):
        if seen[y,x] or g[y,x] not in lets: continue
        c=g[y,x]; st=[(y,x)]; seen[y,x]=1; cl=[]
        while st:
          p=st.pop(); cl.append(p)
          for dy,dx in N8:
            q=(p[0]+dy,p[1]+dx)
            if inb(*q) and not seen[q] and g[q]==c: seen[q]=1; st.append(q)
        if len(cl)<minsz:
          for p in cl:
            nb=[g[p[0]+dy,p[1]+dx] for dy,dx in N4 if inb(p[0]+dy,p[1]+dx) and g[p[0]+dy,p[1]+dx] not in ('.','K','n',c) and FAM[g[p[0]+dy,p[1]+dx]]==FAM[c]]
            if nb: g[p]=max(set(nb),key=nb.count); ch+=1
    if not ch: break
  return g
g=ruis(g,'Wwvucba')  # geel niet: snavel- en voethooglicht komen uit het model
schrijf('stap_ruis.txt',g)
# buitenlijn
SEL={'H':'u','G':'a','Y':'d','D':'K','K':'K'}
o=g.copy()
for y in range(H):
  for x in range(W):
    if g[y,x]=='.': continue
    op=[(dy,dx) for dy,dx in N4 if not inb(y+dy,x+dx) or g[y+dy,x+dx]=='.']
    if not op: continue
    licht=all(d in ((-1,0),(0,-1)) for d in op)
    o[y,x]=SEL[FAM[g[y,x]]] if licht else 'K'
g=o; schrijf('stap_lijn.txt',g)
for r in open('fixes.txt'):
  r=r.split('#')[0].strip()
  if not r: continue
  y,x,s=r.split(); y,x=int(y),int(x)
  for i,c in enumerate(s):
    if c!='_': g[y,x+i]=c
schrijf('rufflet_r1.txt',g)
