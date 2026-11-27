# r4 romp: per cel uit het hi-res model (r4/meet.py 60: F = aandeel zwart L<60, MED = mediane kleur zonder zwart)
# (1) zwarte binnenlijnen: cellen met F>=DREMPEL, uitgedund tot 1 px (Zhang-Suen) -> index 1
# (2) vlakken: dichtstbijzijnde rompkleur van MED; (3) opschonen: tintvlakjes <3 px en rafels (<=1 gelijke van 8 buren) -> meerderheid
# Gebruik: python3 r4/romp.py IN.npy UIT.npy
import sys; sys.path.insert(0,'r2'); from gemeen import *; from clusters import vlakjes
PAL3=list(PAL); PAL3[2]=(90,64,57); PAL3[7]=(194,132,134); PAL3[9]=(160,98,104); P3=np.array(PAL3,float)
o=np.load(sys.argv[1]); r=o.copy(); F=np.load('r4/F.npy'); FZ=np.load('r4/F_zwart.npy'); MED=np.load('r4/MED.npy'); hz=np.load('r4/hoofdzone.npy'); log={}
def zet(c,v,k):
  if o[c]!=v: o[c]=v; log[k]=log.get(k,0)+1
m=o>0; p=np.pad(m,1); rand=m&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
ROMPK=(2,6,7,8,9,10,11,12,14,15)
DONK={7:9,9:2,8:2,2:2,11:2,12:11,14:1,15:14,10:6,6:6}
romp=m&~rand&~hz
for y in range(64):
  for x in range(64):
    if not romp[y,x]: continue
    if y<27: romp[y,x]=False; continue
    if o[y,x] in (3,4,5,13) : romp[y,x]=False      # kap/kraag/gezicht blijven
romp[(o==1)&~rand&~hz&(np.arange(64)[:,None]>=27)]=True
# (1) lijnen
DR=float(sys.argv[3]) if len(sys.argv)>3 else .2
ZD=float(sys.argv[4]) if len(sys.argv)>4 else .18
L=(F>=DR)&romp
def zs(B):
  B=B.copy()
  while True:
    ch=False
    for st in (0,1):
      rm=[]
      for y in range(1,63):
        for x in range(1,63):
          if not B[y,x]: continue
          n=[B[y-1,x],B[y-1,x+1],B[y,x+1],B[y+1,x+1],B[y+1,x],B[y+1,x-1],B[y,x-1],B[y-1,x-1]]
          b=sum(n); a=sum((not n[i]) and n[(i+1)%8] for i in range(8))
          if 2<=b<=6 and a==1:
            if st==0 and not(n[0] and n[2] and n[4]) and not(n[2] and n[4] and n[6]): rm.append((y,x))
            if st==1 and not(n[0] and n[2] and n[6]) and not(n[0] and n[4] and n[6]): rm.append((y,x))
      for c in rm: B[c]=False
      ch|=bool(rm)
    if not ch: return B
L=zs(L)
# losse lijnstukjes < 2 cellen die niet aan een andere lijn of de buitenrand raken: weg
for y,x in zip(*np.where(L)):
  nb=[(y+dy,x+dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
  if not any(L[q] or rand[q] or o[q]==1 and not romp[q] for q in nb): L[y,x]=False
# (2) vlakken
for y,x in zip(*np.where(romp)):
  if L[y,x] and FZ[y,x]>=ZD: zet((y,x),1,'zwarte modellijn (dik, zwart in model)'); continue
  if L[y,x]:   # dunne bruine modellijn: donkerste eigen tint van het vlak eromheen
    md=MED[y,x]; t=ROMPK[int(np.argmin(((P3[list(ROMPK)]-md)**2).sum(1)))]
    zet((y,x),DONK.get(t,t),'dunne modellijn -> donkerste eigen tint'); continue
  md=MED[y,x]; t=ROMPK[int(np.argmin(((P3[list(ROMPK)]-md)**2).sum(1)))]
  zet((y,x),t,'vlak: modelkleur')
# (3) opschonen
N4=((1,0),(-1,0),(0,1),(0,-1)); N8=[(a,b) for a in (-1,0,1) for b in (-1,0,1) if a or b]
for it in range(3):
  for v,comp in vlakjes(o):
    for c in comp:
      if not romp[c] or L[c] or v in (10,6): continue
      nb=[o[c[0]+a,c[1]+b] for a,b in N4 if romp[c[0]+a,c[1]+b] and not L[c[0]+a,c[1]+b] and o[c[0]+a,c[1]+b]!=v]
      if nb: zet(c,max(set(nb),key=nb.count),'vlakje <3 px -> buurtint')
  o0=o.copy()
  for y,x in zip(*np.where(romp&~L)):
    v=o0[y,x]
    if v in (10,6): continue
    nb=[o0[y+a,x+b] for a,b in N8 if romp[y+a,x+b] and not L[y+a,x+b]]
    if len(nb)>=5 and nb.count(v)<=1:
      w=max(set(nb),key=nb.count)
      if nb.count(w)>=4: zet((y,x),w,'rafel -> meerderheid')
# zwarte stompjes: binnenlijn-componenten (8-samenhang) van <=2 cellen die niet aan de buitenrand raken -> buurtint
zw=(o==1)&romp; seen=np.zeros((64,64),bool)
for y,x in zip(*np.where(zw)):
  if seen[y,x]: continue
  st=[(y,x)]; seen[y,x]=1; comp=[]; raakt=False
  while st:
    q=st.pop(); comp.append(q)
    for a,b in N8:
      r_=(q[0]+a,q[1]+b)
      if rand[r_] and o[r_]==1: raakt=True
      if zw[r_] and not seen[r_]: seen[r_]=1; st.append(r_)
  if len(comp)<=2 and not raakt:
    for c in comp:
      nb=[o[c[0]+a,c[1]+b] for a,b in N4 if o[c[0]+a,c[1]+b]>1]
      if nb: zet(c,max(set(nb),key=nb.count),'zwart stompje <=2 cellen -> buurtint')
np.save(sys.argv[2],o)
from PIL import Image
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL3 for v in c]+[0]*(768-48)); im.save(sys.argv[2].replace('.npy','.png'),transparency=0)
for k,v in sorted(log.items()): print('%4d  %s'%(v,k))
print('romp: gewijzigd',int((o!=r).sum()))
