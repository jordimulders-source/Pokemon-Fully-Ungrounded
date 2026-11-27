# r2 stap 2: gezicht = gemeten lijnkaart per modellijn + gemeten vlakken.
# Modellijnen = samenhangende stukken modelpixels L<80 in het gezicht (natief). Per lijn: spritecellen met >=2 pixels
# van die lijn, plus cellen met 1 pixel die anders een gat in die lijn laten; daarna 2x2-klonten gedund.
# Lijn tegen kap/mantel = 1 (zwart, zoals het model); binnenlijn = 2. Stukjes < 4 modelpixels vallen weg (onder spriteschaal).
# Vlak: per modelpixel (L>=80) klasse licht >=160 ->4, midden 115-160 ->3, schaduw <115 ->2; meerderheid per cel;
# vlakjes <3 px -> tweede modelkeuze uit het eigen blok (mits buurtint).
import sys; sys.path.insert(0,'.'); sys.path.insert(0,'../r1'); from gemeen import *; from PIL import Image
from clusters import vlakjes
a=np.asarray(Image.open('../natief.png').convert('RGB')).astype(float); L=lum(a)
o=np.load('kap.npy'); g=np.load('gezmasker.npy'); oud=o.copy()
OOG={(18,24),(18,25),(19,24),(19,25),(18,29),(18,30),(18,31),(19,29),(19,30),(19,31)}
def blok(y,x): return (slice(3*y-9,3*y-6),slice(3*x+3,3*x+6))
T=80
fm=np.zeros(L.shape,bool)
for y in range(64):
  for x in range(64):
    if g[y,x]: fm[blok(y,x)]=True
D=(L<T)&fm; lab=np.zeros(L.shape,int); k=0; comps=[]
for y,x in zip(*np.where(D)):
  if lab[y,x]: continue
  k+=1; st=[(y,x)]; lab[y,x]=k; c=[]
  while st:
    p=st.pop(); c.append(p)
    for dy in (-1,0,1):
      for dx in (-1,0,1):
        q=(p[0]+dy,p[1]+dx)
        if D[q] and not lab[q]: lab[q]=k; st.append(q)
  comps.append(c)
lijn=np.zeros((64,64),bool)
def cel(p): return ((p[0]+9)//3,(p[1]-3)//3)
for c in comps:
  if len(c)<4: continue
  cnt={}
  for p in c: cnt[cel(p)]=cnt.get(cel(p),0)+1
  S={q for q,v in cnt.items() if v>=2}
  for q,v in cnt.items():
    if v!=1 or q in S: continue
    nb=[s for s in S if abs(s[0]-q[0])<=1 and abs(s[1]-q[1])<=1]
    if any(abs(p[0]-r[0])>1 or abs(p[1]-r[1])>1 for p in nb for r in nb): S.add(q)
  for q in S:
    if g[q] and q not in OOG: lijn[q]=True
def verbonden_zonder(y,x):
  nb=[(y+dy,x+dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and lijn[y+dy,x+dx]]
  if len(nb)<2: return False
  seen={nb[0]}; st=[nb[0]]
  while st:
    c=st.pop()
    for q in nb:
      if q not in seen and abs(q[0]-c[0])<=1 and abs(q[1]-c[1])<=1: seen.add(q); st.append(q)
  return len(seen)==len(nb)
ndk=np.zeros((64,64),int)
for y in range(64):
  for x in range(64): ndk[y,x]=D[blok(y,x)].sum() if g[y,x] else 0
# dunnen tot 1 px (Zhang-Suen) zodat elke modellijn een spritelijn van 1 px wordt
def zs(m):
  m=m.copy().astype(int); ch=True
  while ch:
    ch=False
    for st in (0,1):
      weg=[]
      for y in range(1,63):
        for x in range(1,63):
          if not m[y,x]: continue
          P=[m[y-1,x],m[y-1,x+1],m[y,x+1],m[y+1,x+1],m[y+1,x],m[y+1,x-1],m[y,x-1],m[y-1,x-1]]
          B=sum(P); A=sum(P[i]==0 and P[(i+1)%8]==1 for i in range(8))
          if not(2<=B<=6 and A==1): continue
          if st==0 and P[0]*P[2]*P[4]==0 and P[2]*P[4]*P[6]==0: weg.append((y,x))
          if st==1 and P[0]*P[2]*P[6]==0 and P[0]*P[4]*P[6]==0: weg.append((y,x))
      for p in weg: m[p]=0; ch=True
  return m.astype(bool)
voor=int(lijn.sum()); lijn=zs(lijn); print('dunnen:',voor,'->',int(lijn.sum()))
def klasse(l): return 4 if l>=158 else (3 if l>=100 else 2)
hist={}
rand=lambda y,x: any(not g[y+dy,x+dx] and o[y+dy,x+dx]!=1 and (y+dy,x+dx) not in OOG for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
for y in range(64):
  for x in range(64):
    if not g[y,x] or (y,x) in OOG: continue
    b=L[blok(y,x)].ravel(); b=b[b>=T]
    h=np.bincount([klasse(v) for v in b],minlength=5) if len(b) else np.array([0,0,1,0,0]); hist[(y,x)]=h
    if lijn[y,x]:
      nb=[(y+dy,x+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
      if rand(y,x): o[y,x]=1                                   # contour tegen kap/mantel: zwart zoals het model
      elif any(o[q]==1 and q not in OOG and (not g[q] or lijn[q] and rand(*q)) for q in nb):
        lijn[y,x]=False; o[y,x]=h.argmax()                     # tweede pixel dikte van dezelfde contour -> vlak
      else: o[y,x]=2
    else: o[y,x]=h.argmax()
for it in range(2):
  for v,comp in vlakjes(o):
    if v not in (2,3,4): continue
    for (y,x) in comp:
      if not g[y,x] or lijn[y,x] or (y,x) in OOG: continue
      buur={o[y+dy,x+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if not lijn[y+dy,x+dx]}&{2,3,4}-{v}
      if buur: h=hist[(y,x)]; o[y,x]=max(buur,key=lambda k:h[k])
np.save('gezicht2.npy',o); np.save('gezlijn.npy',lijn)
print('modellijnen',k,'| lijnpixels',int(lijn.sum()),'| gezicht gewijzigd t.o.v. r1:',int(((o!=oud)&g).sum()),'van',int(g.sum()))
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-48)); p.save('gezicht2.png',transparency=0)
print('   '+''.join(str(x%10) for x in range(21,36)))
for y in range(13,30): print('%2d '%y+''.join(('L' if lijn[y,x] and o[y,x]==2 else '.123456789ABCDEF'[o[y,x]]) if g[y,x] else ('#' if o[y,x]==1 else ' ') for x in range(21,36)))
