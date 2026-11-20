# Hoatzin r2: onderlaag (r1-reductie) -> gladde toonkaart uit het model -> vleugellijnen/strepen uit de lijnkaart
# -> randcontour gladstrijken -> doorlopende buitenlijn -> oog B. Alles via regels op modelmetingen; elke wijziging gelogd per zone.
import os, json, numpy as np; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); Ln=N.mean(2)
Zn=np.load('zones_nat.npy'); fgn=Zn!='.'; LIJN=np.load('lijn_nat.npy'); STREEP=np.load('streep_nat.npy')
Z=np.load('zone_t.npy'); TH,TW=Z.shape; X0=(64-TW)//2; Y0=64-TH
ys,xs=np.where(fgn); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1; s=(y1-y0)/TH
def Wm(n0,cnt,n):
    M=np.zeros((cnt,n))
    for j in range(cnt):
        a=n0+j*s; b=a+s
        for k in range(int(np.floor(a)),int(np.ceil(b))):
            if 0<=k<n: M[j,k]=max(0,min(b,k+1)-max(a,k))
    return M
Wx=Wm(x0,TW,200); Wy=Wm(y0,TH,200)
red=lambda m: Wy@m.astype(float)@Wx.T/(s*s)
H,W=Ln.shape
def boxmean(a,m,r):
    P=np.pad(a*m,r); Q=np.pad(m.astype(float),r); sm=np.zeros_like(a); c=np.zeros_like(a)
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            sm+=P[r+dy:r+dy+H,r+dx:r+dx+W]; c+=Q[r+dy:r+dy+H,r+dx:r+dx+W]
    return sm/np.maximum(c,1e-6)
PAL=[(152,208,160),(30,18,32),(64,42,60),(90,62,82),(128,98,118),(178,148,170),(100,52,32),(152,82,44),
     (52,62,144),(98,116,214),(208,52,76),(122,82,112),(142,98,128),(165,122,152),(70,66,90),(134,130,152)]
GRP={1:'K',2:'M',3:'M',4:'M',5:'M',6:'C',7:'C',8:'F',9:'F',10:'E',11:'P',12:'P',13:'P',14:'T',15:'T'}
# --- stap A = r1-onderlaag in paletkleuren (zelfde regel als r1) ---
A=np.load('../r1/stapA_r1.npy') if os.path.exists('../r1/stapA_r1.npy') else None
# --- gladde toonkaart: per zonegroep het modelgemiddelde in een venster r=4 (lijnen/strepen niet meegeteld), dan verkleind ---
grp_n={'M':np.isin(Zn,['M','W','K'])&np.isin(Zn,['M','W']),'D':Zn=='D','P':Zn=='P','T':np.isin(Zn,['T','S']),'F':Zn=='F','C':Zn=='C'}
toon={}
for g,m in grp_n.items():
    mm=m&~LIJN&~STREEP
    sm=boxmean(Ln,mm,4 if g in 'MPD' else 2)
    toon[g]=(Wy@(sm*mm)@Wx.T)/np.maximum(Wy@mm.astype(float)@Wx.T,1e-6)
def kies(z,l):
    if z in 'MW': return 2 if l<66 else 3 if l<94 else 4 if l<124 else 5
    if z=='D': return 2 if l<42 else 3
    if z=='C': return 6 if l<62 else 7
    if z=='F': return 8 if l<90 else 9
    if z=='E': return 10
    if z=='P': return 11 if l<98 else 12 if l<126 else 13
    if z in 'TS': return 14 if l<88 else 15
    if z=='K': return 1
    return 0
G={'M':'M','W':'M','D':'D','P':'P','T':'T','S':'T','F':'F','C':'C'}
S=np.zeros((TH,TW),int)
for y in range(TH):
  for x in range(TW):
    z=Z[y,x]
    if z=='.': continue
    if z=='K':   # modellijn-cel: toon van de omringende zone (de lijn komt terug via de lijnkaart of buitenlijn)
        zs=[Z[a,b] for a in range(max(0,y-1),min(TH,y+2)) for b in range(max(0,x-1),min(TW,x+2)) if Z[a,b] not in '.KE']
        z2=max(set(zs),key=zs.count) if zs else 'M'
        S[y,x]=kies(z2,toon[G[z2]][y,x]); continue
    S[y,x]=kies(z,toon[G[z]][y,x]) if z in G else kies(z,0)
B=S.copy()  # basis na toonkaart
log={}
def zet(y,x,v,regel):
    if S[y,x]!=v:
        log.setdefault(regel,{}); z=str(Z[y,x]); log[regel][z]=log[regel].get(z,0)+1; S[y,x]=v
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(i,j) for i in (-1,0,1) for j in (-1,0,1) if i or j]
def ok(y,x): return 0<=y<TH and 0<=x<TW
# --- 1. pennen uit het model (pennen.py): elke spritecel krijgt de pen met het grootste aandeel; pengrenzen = 1 px lijn
#        in de donkerste vleugeltint; per pen één toon (modelgemiddelde van de pen) en hooguit één lichte streep op de modelplek ---
PEN=np.load('pen_nat.npy'); npen=PEN.max()
yyn,xxn=np.mgrid[:H,:W]; VLEUGEL=((xxn>=92)|(yyn<60))
fs=red(STREEP&VLEUGEL)
aand=np.stack([red(PEN==i) for i in range(npen+1)])   # aandeel per pen per cel (0 = geen pen)
P=np.zeros((TH,TW),int)
for y in range(TH):
  for x in range(TW):
    if Z[y,x] in ('M','W','K','D') and aand[1:,y,x].sum()>=0.18:
        P[y,x]=1+int(np.argmax(aand[1:,y,x]))
# cellen tussen de pennen (scheidingslijnen in het model) naar de dichtstbijzijnde pen laten groeien, alleen binnen het vleugelgebied
vg=red(VLEUGEL&np.isin(Zn,['M','W','K','D']))
for _ in range(4):
    Q=P.copy()
    for y in range(TH):
      for x in range(TW):
        if not P[y,x] and Z[y,x] in ('M','W','K','D') and vg[y,x]>=0.5:
            nb=[P[y+d,x+e] for d,e in N4 if ok(y+d,x+e) and P[y+d,x+e]]
            if nb: Q[y,x]=max(set(nb),key=nb.count)
    P=Q
# pentoon: helderheid van de pen in het model (lijnen/strepen niet meegeteld)
PCT=float(os.environ.get('PCT',70))
pl={i:np.percentile(Ln[(PEN==i)&~STREEP],PCT) if ((PEN==i)&~STREEP).any() else 80 for i in range(1,npen+1)}
vast=np.zeros((TH,TW),bool)
# celtoon: mediaan van de modelpixels in de cel, zonder lijn- en streeppixels (meting, zoals px.py)
celtoon=np.zeros((TH,TW)); celgem=np.zeros((TH,TW))
for y in range(TH):
  for x in range(TW):
    a=y0+y*s; b=x0+x*s; sl=(slice(int(a),int(np.ceil(a+s))),slice(int(b),int(np.ceil(b+s))))
    m=fgn[sl]&~LIJN[sl]&~STREEP[sl]
    if m.any(): celtoon[y,x]=np.median(Ln[sl][m])
    mm=fgn[sl]
    if mm.any(): celgem[y,x]=Ln[sl][mm].mean()
for y in range(TH):
  for x in range(TW):
    if P[y,x]:
        v=kies('D' if Z[y,x]=='D' else 'M',celtoon[y,x] if celtoon[y,x]>0 else pl[P[y,x]])
        zet(y,x,v,'1 pen: eén toon per pen (modelgemiddelde)')
for y in range(TH):
  for x in range(TW):
    p=P[y,x]
    if not p: continue
    grens=False
    for d,e in ((0,1),(1,0)):
        if ok(y+d,x+e) and P[y+d,x+e] and P[y+d,x+e]!=p: grens=True
    if grens:
        f=S[y,x]
        if f<=2:
            if celgem[y,x]<38: zet(y,x,1,'1 pengrens in donkere pen (model < 38)'); vast[y,x]=True
        else: zet(y,x,2,'1 pengrens -> lijn (donkerste vleugeltint)'); vast[y,x]=True
# zwarte pengrensjes in donkere pennen alleen als doorlopend (>= 3 px, 8-verbonden), anders terug naar de pentint
seen=np.zeros((TH,TW),bool)
for y in range(TH):
  for x in range(TW):
    if S[y,x]==1 and vast[y,x] and P[y,x] and not seen[y,x]:
      st=[(y,x)];c=[];seen[y,x]=1
      while st:
        a_,b_=st.pop();c.append((a_,b_))
        for d,e in N8:
          q,r=a_+d,b_+e
          if ok(q,r) and S[q,r]==1 and vast[q,r] and P[q,r] and not seen[q,r]: seen[q,r]=1;st.append((q,r))
      if len(c)<3:
        for q,r in c: zet(q,r,2,'1 losse zwarte pengrens weg'); vast[q,r]=False
# streep per pen: rechte lijn gefit (PCA) op de lichte modelstreep van die pen, getekend tussen de uiterste modelpunten;
# alleen cellen van die pen, niet op een pengrens; korter dan MINL px aaneengesloten -> weglaten
MINL=int(os.environ.get('MINL',4))
def sp(yn,xn): return (yn-y0)/s, (xn-x0)/s
def lijnpunten(p0,p1):
    n=int(max(abs(p1[0]-p0[0]),abs(p1[1]-p0[1]))*2)+1
    return [(int(round(p0[0]+(p1[0]-p0[0])*k/n-0.5)),int(round(p0[1]+(p1[1]-p0[1])*k/n-0.5))) for k in range(n+1)]
for i in range(1,npen+1):
    yy_,xx_=np.where(STREEP&(PEN==i))
    if len(yy_)<6: continue
    pts=np.stack([yy_,xx_],1).astype(float)+0.5; c=pts.mean(0); u,sv,vt=np.linalg.svd(pts-c); d=vt[0]
    tt=(pts-c)@d; p0=sp(*(c+d*tt.min())); p1=sp(*(c+d*tt.max()))
    cel=[]
    for q in lijnpunten(p0,p1):
        if q not in cel: cel.append(q)
    cel=[(q,r) for q,r in cel if ok(q,r) and P[q,r]==i and not vast[q,r]]
    # langste aaneengesloten stuk (8-buren)
    best=[];cur=[]
    for k,q in enumerate(cel):
        if cur and max(abs(q[0]-cur[-1][0]),abs(q[1]-cur[-1][1]))>1: cur=[]
        cur.append(q)
        if len(cur)>len(best): best=list(cur)
    if len(best)<MINL: continue
    for q,r in best:
        zet(q,r,5 if S[q,r]>=3 else 4,'1 streep: één doorlopende lijn per pen (gefit op de modelstreep)'); vast[q,r]=True
# --- 1c. lichte voorrand van de voorste vleugel (voorrand.py): modelband op het raster, doorlopend gemaakt ---
BAND=np.load('voorrand_nat.npy'); by,bx=np.where(BAND)
order=np.argsort(by); cells=[]
for yn,xn in zip(by[order],bx[order]):
    q=(int((yn+0.5-y0)/s),int((xn+0.5-x0)/s))
    if q not in cells: cells.append(q)
fb=red(BAND)
keep=[q for q in cells if fb[q]>=float(os.environ.get('VB',0.10))]
# gaten dichten langs de band (volgorde op y)
keep=sorted(set(keep)); vol=set(keep)
for (a1,b1),(a2,b2) in zip(keep,keep[1:]):
    if abs(a2-a1)<=2 and abs(b2-b1)<=3:
        for q in lijnpunten((a1+0.5,b1+0.5),(a2+0.5,b2+0.5)): vol.add(q)
# per rij hooguit 1 px (dun): neem de cel met het grootste bandaandeel
rijen={}
for q in vol:
    if ok(*q) and S[q]>0: rijen.setdefault(q[0],[]).append(q)
VR=[]
for r_,qs in rijen.items():
    qs=sorted(qs,key=lambda q:q[1])
    # aaneengesloten groep met het grootste aandeel
    groepen=[[qs[0]]]
    for q in qs[1:]:
        if q[1]-groepen[-1][-1][1]<=1: groepen[-1].append(q)
        else: groepen.append([q])
    g=max(groepen,key=lambda g:sum(fb[q] for q in g)); VR+=g[:2]
for q in VR:
    zet(q[0],q[1],5,'1c voorrand vleugel (modelband)'); vast[q]=True
# --- 1d. nek: donkere modelstrepen als losse lijnen; ertussen de lichte modeltint (gemeten zonder de strepen) ---
NEK=np.isin(Zn,['M','K','W'])&(xxn>=52)&(xxn<=96)&(yyn>=60)&(yyn<=130)&~(PEN>0)
DK=NEK&(Ln<float(os.environ.get('NK',55)))
fn=red(NEK); fd=red(DK)
licht=NEK&~DK; tl=(Wy@(boxmean(Ln,licht,3)*licht)@Wx.T)/np.maximum(Wy@licht.astype(float)@Wx.T,1e-6)
ND=float(os.environ.get('ND',0.65))
for y in range(TH):
  for x in range(TW):
    if P[y,x] or vast[y,x] or Z[y,x] not in ('M','K','W') or fn[y,x]<0.5: continue
    d=fd[y,x]/fn[y,x]
    if d>=ND: zet(y,x,2,'1d nek: donkere modelstreep'); vast[y,x]=True
    else: zet(y,x,kies('M',tl[y,x]),'1d nek: lichte modeltint tussen de strepen')
for y in range(TH):
  for x in range(TW):
    if S[y,x]==2 and vast[y,x] and fn[y,x]>=0.5 and not P[y,x]:
        if not any(ok(y+d,x+e) and S[y+d,x+e] in (1,2) and vast[y+d,x+e] for d,e in N8):
            zet(y,x,kies('M',tl[y,x]),'1d nek: losse donkere stip weg'); vast[y,x]=False
# --- 1e. buik uit de modelmeting (keurder r3 punt 4/5): lichtvlek van het model (>= 128) = hooglicht, onder 101 = schaduw (nekoverlap boven, sikkel onder)
by_,bx_=np.where(Z=='P')
BH=float(os.environ.get('BH',122)); BS=float(os.environ.get('BS',100))
for y,x in zip(by_,bx_):
    v=toon['P'][y,x]
    zet(y,x,13 if v>=BH else 12 if v>=BS else 11,'1e buik: toon uit modelmeting')
# --- 1f. kuif: strengen uit het model; cellen waar het model vooral licht bruin is -> streng (7), donker -> tint erachter ---
CL=Zn=='C'; fcl=red(CL&(Ln>=float(os.environ.get('KL',62))))
fc=red(CL)
for y in range(TH):
  for x in range(TW):
    if Z[y,x]=='C' and fc[y,x]>0:
        zet(y,x,7 if fcl[y,x]/fc[y,x]>=0.5 else 6,'1f kuif: streng/tussenruimte uit model')
# kuif: lichte strengdelen (7) alleen als doorlopende lijn >= 3 px (8-verbonden), anders donkerbruin (keurder r3 punt 3)
seen=np.zeros((TH,TW),bool)
for y in range(TH):
  for x in range(TW):
    if S[y,x]==7 and not seen[y,x]:
      st=[(y,x)];c=[];seen[y,x]=1
      while st:
        a_,b_=st.pop();c.append((a_,b_))
        for d,e in N8:
          q,r=a_+d,b_+e
          if ok(q,r) and S[q,r]==7 and not seen[q,r]: seen[q,r]=1;st.append((q,r))
      if len(c)<3:
        for q,r in c: zet(q,r,6,'1f kuif: losse lichte spikkel -> donkerbruin')
# --- 1g. snavel uit het model (keurder r3 punt 2): snavelcellen = zone S/K in het snavelvak, buiten gezicht/oog;
#     toon per cel uit de modelmeting: rand en snavelspleet (p15 < 30) zwart, middentoon donkergrijs, >= 100 glans
SNAVEL=[]
for y in range(TH):
  for x in range(TW):
    cx_,cy_=x+X0,y+Y0
    if 6<=cx_<=12 and 21<=cy_<=28 and Z[y,x] in ('S','K') and S[y,x]>0:
        nb_f=any(ok(y+d,x+e) and Z[y+d,x+e] in ('F','E') for d,e in N4)
        if Z[y,x]=='K' and nb_f and cx_>=9: continue
        SNAVEL.append((y,x))
for y,x in SNAVEL:
    a=y0+y*s; b=x0+x*s; sl=(slice(int(a),int(np.ceil(a+s))),slice(int(b),int(np.ceil(b+s))))
    m=fgn[sl]; v=Ln[sl][m]
    rnd=any(not(ok(y+d,x+e) and S[y+d,x+e]>0) for d,e in N4)
    if rnd or v.mean()<45: w=1
    elif np.percentile(v,15)<30 and v.mean()<85: w=1
    elif v.mean()>=95: w=15
    else: w=14
    zet(y,x,w,'1g snavel uit modelmeting'); vast[y,x]=True
# --- 2. vlakken: clusters < 4 px (niet de vaste lijnen/strepen) nemen de buurtint van dezelfde groep ---
def clusters():
    seen=np.zeros_like(S,bool); out=[]
    for y in range(TH):
      for x in range(TW):
        v=S[y,x]
        if v>1 and not seen[y,x] and not vast[y,x]:
          st=[(y,x)];c=[];seen[y,x]=1
          while st:
            a,b=st.pop();c.append((a,b))
            for d,e in N4:
              p,q=a+d,b+e
              if ok(p,q) and S[p,q]==v and not seen[p,q] and not vast[p,q]: seen[p,q]=1;st.append((p,q))
          out.append((v,c))
    return out
for _ in range(4):
  for v,c in clusters():
    if len(c)>=4 or GRP.get(v) in ('C','E','F'): continue
    buur=[]
    for a,b in c:
        for p,q in [(a+d,b+e) for d,e in N4]:
            if ok(p,q) and S[p,q]>1 and S[p,q]!=v and not vast[p,q] and GRP.get(S[p,q])==GRP.get(v): buur.append(S[p,q])
    if buur:
        w=max(set(buur),key=buur.count)
        for a,b in c: zet(a,b,w,'2 vlakken: cluster <4 px -> buurtint')
# --- 3. contour: losse uitsteeksels weg (alleen waar de modelcel < 60 % gevuld is), inkepingen dicht (modelcel >= 35 %) ---
ff=red(fgn); fg=S>0
for _ in range(2):
  for y in range(TH):
    for x in range(TW):
      n=sum(1 for d,e in N4 if ok(y+d,x+e) and S[y+d,x+e]>0)
      if S[y,x]>0 and n<=1 and Z[y,x] not in 'CTSK' and ff[y,x]<0.6: zet(y,x,0,'3 contour: uitsteeksel weg')
      elif S[y,x]==0 and n>=3 and ff[y,x]>=0.35:
          nb=[S[y+d,x+e] for d,e in N4 if ok(y+d,x+e) and S[y+d,x+e]>1]
          zet(y,x,max(set(nb),key=nb.count) if nb else 1,'3 contour: inkeping dicht')
fg=S>0
# --- 4. buitenlijn: elke randpixel; lichtkant gekleurde selout (donkerste tint van de groep), schaduwkant zwart ---
DONKER={'M':2,'W':2,'K':2,'D':2,'C':6,'F':8,'P':3,'T':14,'S':1}
rand=np.zeros((TH,TW),bool)
for y in range(TH):
  for x in range(TW):
    if fg[y,x] and any(not(ok(y+d,x+e) and fg[y+d,x+e]) for d,e in N4): rand[y,x]=True
for y in range(TH):
  for x in range(TW):
    if not rand[y,x] or Z[y,x]=='E': continue
    z=Z[y,x]
    if z=='C': zet(y,x,6,'4 buitenlijn'); continue
    if z=='S' or (y,x) in SNAVEL: zet(y,x,1,'4 buitenlijn snavel zwart'); continue
    bgd=[(d,e) for d,e in N8 if not(ok(y+d,x+e) and fg[y+d,x+e])]
    licht=sum(-d-e for d,e in bgd)>0 and x<TW*0.62 and y<TH*0.72
    if z=='K':
        zs=[Z[a,b] for a,b in [(y+d,x+e) for d,e in N8] if ok(a,b) and Z[a,b] not in '.KE']; z=max(set(zs),key=zs.count) if zs else 'M'
    zet(y,x,DONKER.get(z,2) if licht else 1,'4 buitenlijn')
# om-en-om weg langs de rand
SEL={2,3,6,8,11,14}
for _ in range(2):
  for y in range(TH):
    for x in range(TW):
      if not rand[y,x] or Z[y,x] in 'CE': continue
      rb=[S[y+d,x+e] for d,e in N8 if ok(y+d,x+e) and rand[y+d,x+e] and Z[y+d,x+e] not in 'CE']
      zw=rb.count(1); se=[w for w in rb if w in SEL]
      if S[y,x] in SEL and zw>=2 and not se: zet(y,x,1,'4 rand om-en-om')
      elif S[y,x]==1 and len(se)>=2 and zw==0: zet(y,x,max(set(se),key=se.count),'4 rand om-en-om')
# --- 4b. donkere rand achter het blauwe gezicht (keurder r3 punt 6): niet-gezichtcellen die het blauw raken in het vak x13-17, y18-23
for y in range(TH):
  for x in range(TW):
    cx_,cy_=x+X0,y+Y0
    if 14<=cx_<=17 and 19<=cy_<=23 and S[y,x] not in (0,8,9,10,1) and Z[y,x] not in ('F','E'):
        if any(ok(y+d,x+e) and S[y+d,x+e] in (8,9) for d,e in N4): zet(y,x,1,'4b rand achter gezicht')
# --- 5. oog variant B (3x3 rond de donkerste modelpixel, onderhoeken donkerblauw) + glans linksboven (modeliris is daar lichter) ---
ey,ex=np.where(Z=='E'); C=np.load('col_t.npy'); i=np.argmin(C.mean(2)[ey,ex]); py,px=ey[i],ex[i]
for y,x in zip(ey,ex):
    if abs(y-py)>1 or abs(x-px)>1: zet(y,x,9,'5 oog')
for dy in (-1,0,1):
  for dx in (-1,0,1):
    zet(py+dy,px+dx,1 if not(dy or dx) else (8 if dy>0 and dx else 10),'5 oog')
if os.environ.get('GLANS','1')=='1': zet(py-1,px-1,15,'5 oog glans')
# --- opslaan ---
im=np.zeros((64,64),'uint8'); im[Y0:Y0+TH,X0:X0+TW]=S
p=Image.fromarray(im,'P'); p.putpalette([c for t in PAL for c in t]); p.save(os.environ.get('OUT','hoatzin.png'),transparency=0)
open('normal.pal','w').write('JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%c for c in PAL))
np.save('stapS.npy',S); json.dump(log,open('log.json','w'),indent=1)
for r,d in log.items(): print(r,d,sum(d.values()))
O=np.asarray(Image.open('onderlaag.png'))[...,3]>0
print('silhouet-diff t.o.v. onderlaag:',int(((im>0)!=O).sum()),'kleuren',len(np.unique(im)))
