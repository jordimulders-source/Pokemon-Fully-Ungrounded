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
PAL=[(152,208,160),(30,18,32),(50,30,48),(90,62,82),(128,98,118),(178,148,170),(100,52,32),(152,82,44),
     (52,62,144),(98,116,214),(208,52,76),(122,82,112),(142,98,128),(165,122,152),(88,84,106),(134,130,152)]
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
# --- 1. vleugellijnen en strepen uit de lijnkaart (natief), alleen in vleugel/staart ---
yyn,xxn=np.mgrid[:H,:W]; VLEUGEL=(xxn>=int(os.environ.get('VX',92)))|(yyn<60)
fl=red(LIJN&VLEUGEL); fs=red(STREEP&VLEUGEL)
TL=float(os.environ.get('TL',0.13)); TS=float(os.environ.get('TS',0.16))
vast=np.zeros((TH,TW),bool)
for y in range(TH):
  for x in range(TW):
    if Z[y,x] in ('M','W','K','D') and fl[y,x]>=TL:
        f=S[y,x]; zet(y,x,1 if f<=2 else max(2,f-2) if f>=4 else 2,'1 vleugellijn uit model'); vast[y,x]=True
for y in range(TH):
  for x in range(TW):
    if Z[y,x] in ('M','W') and not vast[y,x] and fs[y,x]>=TS and fs[y,x]>fl[y,x]:
        zet(y,x,5,'1 lichte streep uit model'); vast[y,x]=True
# lijnen dunner: lijnpixel met lijnburen links én rechts óf boven én onder van een 2-dik blok -> houd de sterkste
# strepen: per pen hooguit één streep -> streeppixel die naast (4-buur) een sterkere streeppixel ligt dwars op de pen valt weg
for y in range(TH):
  for x in range(TW):
    if S[y,x]==5 and vast[y,x]:
        for dy,dx in N4:
            if ok(y+dy,x+dx) and S[y+dy,x+dx]==5 and fs[y+dy,x+dx]>fs[y,x] and ok(y-dy,x-dx) and S[y-dy,x-dx]!=5 and dy!=0:
                zet(y,x,B[y,x] if B[y,x]!=5 else 4,'1 streep 1 px per pen'); vast[y,x]=False; break
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
DONKER={'M':2,'W':2,'K':2,'D':2,'C':6,'F':8,'P':11,'T':14,'S':14}
rand=np.zeros((TH,TW),bool)
for y in range(TH):
  for x in range(TW):
    if fg[y,x] and any(not(ok(y+d,x+e) and fg[y+d,x+e]) for d,e in N4): rand[y,x]=True
for y in range(TH):
  for x in range(TW):
    if not rand[y,x] or Z[y,x]=='E': continue
    z=Z[y,x]
    if z=='C': zet(y,x,6,'4 buitenlijn'); continue
    bgd=[(d,e) for d,e in N8 if not(ok(y+d,x+e) and fg[y+d,x+e])]
    licht=sum(-d-e for d,e in bgd)>0 and x<TW*0.62 and y<TH*0.72
    if z=='K':
        zs=[Z[a,b] for a,b in [(y+d,x+e) for d,e in N8] if ok(a,b) and Z[a,b] not in '.KE']; z=max(set(zs),key=zs.count) if zs else 'M'
    zet(y,x,DONKER.get(z,2) if licht else 1,'4 buitenlijn')
# om-en-om weg langs de rand
SEL={2,6,8,11,14}
for _ in range(2):
  for y in range(TH):
    for x in range(TW):
      if not rand[y,x] or Z[y,x] in 'CE': continue
      rb=[S[y+d,x+e] for d,e in N8 if ok(y+d,x+e) and rand[y+d,x+e] and Z[y+d,x+e] not in 'CE']
      zw=rb.count(1); se=[w for w in rb if w in SEL]
      if S[y,x] in SEL and zw>=2 and not se: zet(y,x,1,'4 rand om-en-om')
      elif S[y,x]==1 and len(se)>=2 and zw==0: zet(y,x,max(set(se),key=se.count),'4 rand om-en-om')
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
