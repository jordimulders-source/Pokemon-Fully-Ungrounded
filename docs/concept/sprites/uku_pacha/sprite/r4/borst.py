# Uku Pacha r4: borst/buik (lichte voorkant) van beide nekken opnieuw uit het model.
# Zone = spritepixels (rij 16-60, buiten koppen/geest/vleugels/buitenrand) waarvan het model in de
# voetafdruk overwegend lichte vlakklassen heeft (12-15). Daarin:
#  - lijnen: elke modellijncel (klasse 1-4) plus de dunne grijsblauwe dwarslijncellen tussen licht
#    (klasse 5-11 met >= 3 lichte buren, klasse 12 midden in wit) -> geprojecteerd en met zijn
#    8-buren verbonden (doorlopend 1 px), dubbele dikte gedund met de omgeving vast -> n
#  - vlak: oppervlak-gewogen meerderheid van de lichte modelklassen (12 b, 13 l, 14 p, 15 w):
#    heldere toongrenzen op de modelplek, geen gemiddelde middentonen.
# Zwarte spiraalpixels (K) uit kronkel_lijnen blijven staan.
import numpy as np, geom
cls=np.load('cls.npy'); GH=np.load('GH.npy')
R=[list(l.rstrip('\n')) for l in open('raster.txt')][:64]
xs=np.arange(100)[None,:]
GHN=np.isin(cls,[13,14,15])&(xs>=72)
light=np.isin(cls,[12,13,14,15])&~GHN   # licht vlak van de borst incl. basis c (bovenste borst rechternek is c)
cnt=np.zeros((100,100),int)
for dy in (-1,0,1):
  for dx in (-1,0,1):
    if dy or dx: cnt+=np.roll(np.roll(light,dy,0),dx,1)
LIJN=(np.isin(cls,[1,2,3,4])|((cls>=5)&(cls<=11)&(cnt>=4)))&(xs<72)
KOP=np.zeros((64,64),bool); KOP[2:28,0:23]=True; KOP[2:16,29:50]=True
def ins(x,y): return 0<=x<64 and 0<=y<64 and R[y][x]!='.'
def rand(x,y): return any(not ins(x+a,y+b) for a,b in ((0,1),(0,-1),(1,0),(-1,0)))
LET={12:'b',13:'l',14:'p',15:'w'}
Z=np.zeros((64,64),bool); VL={}
for y in range(16,61):
  for x in range(64):
    if not ins(x,y) or KOP[y,x] or GH[y,x] or rand(x,y) or R[y][x] in 'DBhYPW': continue
    x0,x1,y0,y1=geom.s2n(x,y); acc={}; tot=0
    for cy in range(int(y0),int(np.ceil(y1))):
      for cx in range(int(x0),int(np.ceil(x1))):
        a=(min(x1,cx+1)-max(x0,cx))*(min(y1,cy+1)-max(y0,cy)); k=cls[cy,cx]
        if a<=0 or k<0: continue
        tot+=a
        if k in LET and not GHN[cy,cx]: acc[k]=acc.get(k,0)+a
        elif 5<=k<=11 and not LIJN[cy,cx]: acc['donker']=acc.get('donker',0)+a
    licht=sum(v for k,v in acc.items() if k!='donker')
    if licht>=0.5*tot and licht>acc.get('donker',0):
        Z[y,x]=True; VL[(x,y)]=LET[max((k for k in acc if k!='donker'),key=acc.get)]
def proj(x,y):
    sx,sy=geom.n2s(x+0.5,y+0.5); return int(np.floor(sx)),int(np.floor(sy))
L=np.zeros((64,64),bool); FL=np.zeros((64,64),bool); HUIDIG=[False]
def zet(i,j):
    if 0<=i<64 and 0<=j<64 and Z[j,i]:
        if not L[j,i]: FL[j,i]=HUIDIG[0]
        elif not HUIDIG[0]: FL[j,i]=False
        L[j,i]=True
# per samenhangende modellijn (buren tot 2 cellen): cellen langs de hoofdas ordenen en als polylijn tekenen
DONKERL=np.isin(cls,[1,2,3,4])&LIJN
# flauwe plaatgrens in de lichte buik: een cel die >= 20 donkerder is dan twee tegenoverliggende
# lichte buren (L >= 190, op 1 of 2 cellen afstand); in het model zijn dat de lijntjes tussen de
# buikplaten (klasse 11-14, lum 110-190), die de klasse-indeling niet als lijn zag
LUMN=geom.N.mean(2)
FLAUW=np.zeros((100,100),bool)
for y in range(2,98):
  for x in range(2,98):
    if cls[y,x]<2 or cls[y,x]>14 or GHN[y,x] or x>=72 or DONKERL[y,x]: continue
    for dx,dy in ((1,0),(0,1),(1,1),(1,-1)):
      ok=False
      for d1 in (1,2):
        for d2 in (1,2):
          a1=LUMN[y+dy*d1,x+dx*d1]; a2=LUMN[y-dy*d2,x-dx*d2]
          if a1>=190 and a2>=190 and LUMN[y,x]<=min(a1,a2)-20 and not geom.BG[y+dy*d1,x+dx*d1] and not geom.BG[y-dy*d2,x-dx*d2]: ok=True
      if ok: FLAUW[y,x]=True; break
FLAUW|=LIJN&~DONKERL
# donkere modellijnen (klasse 1-4): elke cel met zijn 8-buren verbonden (zoals stap1 in r2); geen
# ordening, want ze hangen aan de omlijning vast en vormen grote vertakte stukken
HUIDIG[0]=False
for y in range(100):
  for x in range(100):
    if not DONKERL[y,x]: continue
    i0,j0=[int(v) for v in np.floor(geom.n2s(x+0.5,y+0.5))]; zet(i0,j0)
    for dy,dx in ((0,1),(1,0),(1,1),(1,-1)):
      yy,xx=y+dy,x+dx
      if 0<=yy<100 and 0<=xx<100 and DONKERL[yy,xx]:
        if dy and dx and (DONKERL[y,xx] or DONKERL[yy,x]): continue
        i1,j1=[int(v) for v in np.floor(geom.n2s(xx+0.5,yy+0.5))]; n=max(abs(i1-i0),abs(j1-j0))
        for t in range(1,n+1): zet(round(i0+(i1-i0)*t/n),round(j0+(j1-j0)*t/n))
# flauwe grijsblauwe dwarslijnen: het model tekent ze schuin met sprongetjes van 2 cellen; per stuk
# (buren tot 2 cellen, alleen flauw met flauw) langs de hoofdas geordend en als polylijn getekend
comp=np.full((100,100),-1); C=[]
for y in range(100):
  for x in range(100):
    if FLAUW[y,x] and comp[y,x]<0:
      st=[(x,y)]; cel=[]
      while st:
        a_,b_=st.pop()
        if 0<=a_<100 and 0<=b_<100 and FLAUW[b_,a_] and comp[b_,a_]<0:
          comp[b_,a_]=len(C); cel.append((a_,b_)); st+=[(a_+dx,b_+dy) for dx in range(-2,3) for dy in range(-2,3) if dx or dy]
      C.append(cel)
HUIDIG[0]=True
for cel in C:
    P=np.array([geom.n2s(x+0.5,y+0.5) for x,y in cel])
    if len(P)==1:
        zet(int(P[0,0]),int(P[0,1])); continue
    c=P-P.mean(0); u,s_,vt=np.linalg.svd(c,full_matrices=False); t=c@vt[0]
    P=P[np.argsort(t)]
    for k in range(len(P)):
        i0,j0=int(np.floor(P[k,0])),int(np.floor(P[k,1])); zet(i0,j0)
        if k+1<len(P):
            i1,j1=int(np.floor(P[k+1,0])),int(np.floor(P[k+1,1])); n=max(abs(i1-i0),abs(j1-j0))
            for tt in range(1,n+1): zet(round(i0+(i1-i0)*tt/n),round(j0+(j1-j0)*tt/n))
# plus: spritepixel is lijn als >= DREMPEL van zijn voetafdruk uit borstlijncellen bestaat
# (een modellijn van 1 cel valt anders tussen twee spritepixels in en breekt in streepjes)
DREMPEL=0.12
for y in range(64):
  for x in range(64):
    if not Z[y,x] or L[y,x]: continue
    x0,x1,y0,y1=geom.s2n(x,y); la=0
    for cy in range(int(y0),int(np.ceil(y1))):
      for cx in range(int(x0),int(np.ceil(x1))):
        a=(min(x1,cx+1)-max(x0,cx))*(min(y1,cy+1)-max(y0,cy))
        if a>0 and LIJN[cy,cx]: la+=a
    if la/((x1-x0)*(y1-y0))>=DREMPEL: L[y,x]=True
# dunnen: alles buiten de zone en de K-spiraal vast
vast=np.zeros((64,64),bool)
for y in range(64):
  for x in range(64):
    if ins(x,y) and (not Z[y,x] or R[y][x] in 'Kn'): vast[y,x]=True   # bestaande lijnen blijven (Jordi: alle lijnen blijven)
B=L|vast
def nb(j,i):
    o=[(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
    return [bool(B[j+a,i+b]) if 0<=j+a<64 and 0<=i+b<64 else False for a,b in o]
ch=True
while ch:
    ch=False
    for stap in (0,1):
        weg=[]
        for j,i in zip(*np.where(B&Z)):
            if vast[j,i]: continue
            p=nb(j,i); n=sum(p)
            if not 2<=n<=6: continue
            if sum((not p[k]) and p[(k+1)%8] for k in range(8))!=1: continue
            P2,P3,P4,P5,P6,P7,P8,P9=p
            if stap==0 and (P2 and P4 and P6 or P4 and P6 and P8): continue
            if stap==1 and (P2 and P4 and P8 or P2 and P6 and P8): continue
            weg.append((j,i))
        for j,i in weg: B[j,i]=False
        ch|=bool(weg)
nl=nv=0
for y in range(64):
  for x in range(64):
    if not Z[y,x] or R[y][x]=='K': continue
    if R[y][x]=='n': nl+=1; continue
    if B[y,x]:
        # lijntint naar de modelhelderheid van de lijncellen in de voetafdruk
        x0,x1,y0,y1=geom.s2n(x,y); vals=[LUMN[cy,cx] for cy in range(int(y0),int(np.ceil(y1))) for cx in range(int(x0),int(np.ceil(x1))) if FLAUW[cy,cx] or DONKERL[cy,cx]]
        v=min(vals) if vals else 0
        R[y][x]='n' if (not FL[y,x] or v<95) else ('d' if v<150 else 'l'); nl+=1
    else: R[y][x]=VL[(x,y)]; nv+=1
print('borstzone',int(Z.sum()),'px; lijn',nl,'vlak',nv)
open('raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
