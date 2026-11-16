# r6 opschonen van de modelonderlaag (geen tekenwerk): specks -> buurkleur, omlijning sluiten, dubbele lijn weg, ogen r5.
import sys; sys.path.insert(0,'r6w'); sys.path.insert(0,'.')
import numpy as np
from p6 import CH,PAL,to_txt,from_txt,save
import gio
I={c:i for i,c in enumerate(CH)}
o=from_txt('r6w/m6.txt'); m=np.load('mask_r1.npy'); kd=np.load('r6w/kd.npy')
log=[]
N4=((1,0),(-1,0),(0,1),(0,-1)); N8=N4+((1,1),(1,-1),(-1,1),(-1,-1))
def nbrs(o,j,i,N=N8):
    return [o[j+a,i+b] for a,b in N if 0<=j+a<64 and 0<=i+b<64]
LIGHT=[I[c] for c in 'WLMD']; LS=LIGHT+[I['S']]
# 1. paarse/oog-specks in lichte (ijs)omgeving -> naadtint (het zijn modellijnen met paarsige mediaan)
for j in range(64):
  for i in range(64):
    if o[j,i]<0 or CH[o[j,i]] not in 'abcdGerCg': continue
    nb=[v for v in nbrs(o,j,i) if v>=0]
    if sum(v in LS for v in nb)>=6:
        o[j,i]=I['S'] if kd[j,i]>=1 or sum(v==I['S'] for v in nb)>=2 else max(set(nb),key=nb.count); log.append(('speck',i,j))
# 2. omlijning: randpixels van het masker
edge=np.zeros((64,64),bool)
for j in range(64):
  for i in range(64):
    if m[j,i] and any(not(0<=j+a<64 and 0<=i+b<64) or not m[j+a,i+b] for a,b in N4): edge[j,i]=True
# ijsrand = rand waar binnen 2 px een modellijn (S) in licht gebied ligt en geen paars; anders gas/spike
ice=np.load('r6w/ice.npy')  # indeling ijs/staart (alleen voor de kleur van de omlijning)
icedge=edge&ice
ice_y=None
for j,i in zip(*np.where(edge)):
    c=CH[o[j,i]]
    if icedge[j,i]:
        # lichtkant (boven/links) selout S, schaduwkant (onder) K; overgang op y>=47 en rechts van x>=30
        o[j,i]=I['K'] if (j>=47 or i>=30) else I['S']
    elif c in 'abK':
        o[j,i]=I['K']
    elif c in 'cd':
        o[j,i]=I['K']
    else:
        o[j,i]=I['L']  # gas: lichte zachte selout
# 3a. buitenste modellijn (+ lichte halo ertussen) binnen 2 px van de ijsrand -> vulling; naden die erop uitkwamen doortrekken
zone=np.zeros_like(edge)
for j,i in zip(*np.where(icedge)):
    for a,b in N4:
        y,x=j+a,i+b
        if not(0<=y<64 and 0<=x<64) or not m[y,x] or edge[y,x]: continue
        seq=[(y,x),(y+a,x+b),(y+2*a,x+2*b)]
        for k,(yy,xx) in enumerate(seq):
            if not(0<=yy<64 and 0<=xx<64) or edge[yy,xx] or not ice[yy,xx]: break
            c=CH[o[yy,xx]]
            if c=='S': zone[yy,xx]=True; break
            if c in 'WL' and k<=1 and any(0<=yy+t*a<64 and 0<=xx+t*b<64 and CH[o[yy+t*a,xx+t*b]]=='S' for t in (1,2)): zone[yy,xx]=True; continue
            break
o2=o.copy()
for j,i in zip(*np.where(zone)):
    f=[o[j+a,i+b] for a,b in N8 if 0<=j+a<64 and 0<=i+b<64 and not zone[j+a,i+b] and not edge[j+a,i+b] and o[j+a,i+b] in LIGHT]
    if f: o2[j,i]=max(set(f),key=f.count); log.append(('buitenlijn',i,j))
# naad die op de zone uitkwam: verbinden met de rand
for j,i in zip(*np.where(zone)):
    if o2[j,i]==I['S']: continue
    inner=[(j+a,i+b) for a,b in N4 if 0<=j+a<64 and 0<=i+b<64 and o2[j+a,i+b]==I['S'] and not zone[j+a,i+b] and not edge[j+a,i+b]]
    if inner and any(0<=j+a<64 and 0<=i+b<64 and icedge[j+a,i+b] for a,b in N4): o2[j,i]=I['S']; log.append(('naadverbinding',i,j))
o=o2
# 3. dubbele lijn: interne S direct naast de ijsrand, zonder eigen naad naar binnen -> vulkleur van de binnenburen
for _ in range(2):
  for j in range(64):
    for i in range(64):
      if o[j,i]!=I['S'] or edge[j,i]: continue
      if not any(0<=j+a<64 and 0<=i+b<64 and icedge[j+a,i+b] for a,b in N4): continue
      inner=[(j+a,i+b) for a,b in N4 if 0<=j+a<64 and 0<=i+b<64 and o[j+a,i+b]==I['S'] and not edge[j+a,i+b]]
      deep=[p for p in inner if not any(0<=p[0]+a<64 and 0<=p[1]+b<64 and icedge[p[0]+a,p[1]+b] for a,b in N4)]
      if deep: continue
      f=[v for v in nbrs(o,j,i) if v in LIGHT]
      if f: o[j,i]=max(set(f),key=f.count); log.append(('dubbel',i,j))
# 4. ogen: r5 (goedgekeurd), overige oogkleur -> buurvulling
r5=gio.from_txt('r5.txt')
eye5={(j,i):gio.CH[r5[j,i]] for j in range(28,40) for i in range(2,20) if r5[j,i]>=0 and gio.CH[r5[j,i]] in 'cCrg'}
for j in range(28,40):
  for i in range(2,20):
    if o[j,i]>=0 and CH[o[j,i]] in 'erCg' and (j,i) not in eye5:
        f=[v for v in nbrs(o,j,i) if v in LIGHT]; o[j,i]=max(set(f),key=f.count) if f else I['L']
MAP={'c':'e','C':'C','r':'r','g':'g'}
for (j,i),c in eye5.items(): o[j,i]=I[MAP[c]]
# 5. modellijnen in de staart (lichte blokken buiten het ijs) -> spike-omlijning K
for j in range(64):
  for i in range(64):
    if o[j,i]==I['S'] and not ice[j,i] and not edge[j,i]: o[j,i]=I['K']; log.append(('staartlijn',i,j))
# 6. dikke naden: 2x2-blok S -> pixel met de minste modellijn naar vulling
ch=True
while ch:
  ch=False
  for j in range(63):
    for i in range(63):
      b=[(j,i),(j,i+1),(j+1,i),(j+1,i+1)]
      if all(o[p]==I['S'] for p in b):
        cand=[p for p in b if not edge[p]]
        if not cand: continue
        p=min(cand,key=lambda p:kd[p])
        f=[o[p[0]+a,p[1]+c] for a,c in N8 if 0<=p[0]+a<64 and 0<=p[1]+c<64 and o[p[0]+a,p[1]+c] in LIGHT]
        if f: o[p]=max(set(f),key=f.count); ch=True; log.append(('dikte',p[1],p[0]))
# 7. losse pixels (geen 4-buur met dezelfde kleur, geen lijn/oog) -> meest voorkomende 4-buur
for _ in range(2):
  for j in range(64):
    for i in range(64):
      if o[j,i]<0 or edge[j,i] or CH[o[j,i]] in 'SKerCg': continue
      nb=[o[j+a,i+b] for a,b in N4 if 0<=j+a<64 and 0<=i+b<64]
      if o[j,i] in nb: continue
      f=[v for v in nb if v>=0 and CH[v] not in 'SKerCg']
      if f: o[j,i]=max(set(f),key=f.count); log.append(('los',i,j))
# 8. clusterfilter vulkleuren: 4-verbonden vlakjes < 3 px -> meest voorkomende 8-buur (geen lijn/oog)
FILL=[I[c] for c in 'WLMDabcdG']
for _ in range(3):
  seen=np.zeros((64,64),bool)
  for j in range(64):
    for i in range(64):
      if seen[j,i] or o[j,i] not in FILL or edge[j,i]: continue
      c=o[j,i]; st=[(j,i)]; seen[j,i]=True; comp=[]
      while st:
        a,b=st.pop(); comp.append((a,b))
        for da,db in N4:
          y,x=a+da,b+db
          if 0<=y<64 and 0<=x<64 and not seen[y,x] and o[y,x]==c: seen[y,x]=True; st.append((y,x))
      if len(comp)>=3: continue
      cs=set(comp)
      f=[o[a+da,b+db] for a,b in comp for da,db in N8 if 0<=a+da<64 and 0<=b+db<64 and (a+da,b+db) not in cs and o[a+da,b+db] in FILL]
      if not f: continue
      nc=max(set(f),key=f.count)
      for p in comp: o[p]=nc; log.append(('cluster',p[1],p[0]))
# 9. grens ijs/paars: ijs-naadpixels die aan paars/K van de staart grenzen -> K (schaduwkant, één lijnkleur op die rand);
#    K binnen het ijs (modelkruispunten) -> naadtint S
PUR=[I[c] for c in 'abcdK']
for j in range(64):
  for i in range(64):
    if not ice[j,i] or o[j,i] not in (I['S'],I['K']) or edge[j,i]: continue
    adj=any(0<=j+a<64 and 0<=i+b<64 and not ice[j+a,i+b] and o[j+a,i+b] in PUR for a,b in N4)
    nc=I['K'] if adj else I['S']
    if o[j,i]!=nc: o[j,i]=nc; log.append(('ijsgrens',i,j))
# 10. losse naadpixel (8-verbonden alleen, geen andere lijn ernaast) -> vulling
for j in range(64):
  for i in range(64):
    if o[j,i]!=I['S'] or edge[j,i]: continue
    if any(0<=j+a<64 and 0<=i+b<64 and o[j+a,i+b] in (I['S'],I['K']) for a,b in N8): continue
    f=[o[j+a,i+b] for a,b in N8 if 0<=j+a<64 and 0<=i+b<64 and o[j+a,i+b] in LIGHT]
    if f: o[j,i]=max(set(f),key=f.count); log.append(('losse naad',i,j))
np.save('r6w/edge.npy',edge); np.save('r6w/icedge.npy',icedge)
to_txt(o,'r6w/s6.txt'); save(o,'r6w/s6')
print(len(log))
