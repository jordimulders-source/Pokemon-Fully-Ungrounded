# r17 = r16 opgeschoond (eindkeurder, 16 nov). Alleen bestaande paletindexen; vormen uit r16 (= r14-koeienvanger) en het model.
# Bevroren (assert): alle groene indexen, zwarte gezichtslijnen van de grote kop (zwart binnen 2 px van groen in de kop), rij 0-19.
# Koeienvanger (x0-27, y45-58): (1) lijnen = zwarte componenten van r16 >= 3 px (V-randen, schuine naden, tandpunt), kleinere vallen weg;
#   (2) vulling: familie roest/grijs uit het model (aandeel roest in de voetafdruk), toon uit het gladde model (sigma 0,8 natief);
#   (3) roest < 3 px -> grijs; 1-px-eilandjes -> buurmodus in dezelfde familie; (4) Gen 3-facet: lichte rand onder de band/V, donker links van een spleet.
# Kop: losse zwarte pixels (geen zwarte 8-buur) en 1-px-eilandjes weg; bruin 8/9 opnieuw uit het grove model (sigma 3, alleen bruin):
#   onderste kwart -> 9 (schaduw rechts/onder en onder de plaat), rest 8; 7 (glans) blijft waar hij stond.
# Buitenlijn: ijzer aan transparant = zwart, behalve lichtkant (links/boven, rij < 40) = selout 9 (roest) / 12 (grijs).
import numpy as np
from PIL import Image
from collections import Counter, deque
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
im=Image.open(D+'sprite_r16/sprite.png'); r=np.array(im).astype(int); pal=im.getpalette()
N=np.array(Image.open(D+'model/natief.png').convert('RGB')).astype(float)
LUM=0.3*N[...,0]+0.59*N[...,1]+0.11*N[...,2]
GR={2,3,4,5,6,13}; FILL={7,8,9,10,11,12}; RUST={8,9}; GREY={7,10,11,12}; IJ={1}|FILL
F_=0.744
def ok(y,x): return 0<=y<64 and 0<=x<64
def nb8(a,y,x): return [a[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and ok(y+dy,x+dx)]
def rand(a,y,x): return x==0 or any(ok(y+dy,x+dx) and a[y+dy,x+dx]==0 for dy,dx in((0,1),(1,0),(0,-1),(-1,0)))
def comps(mask):
    lab=np.zeros(mask.shape,bool); out=[]
    for y,x in zip(*np.where(mask)):
        if lab[y,x]: continue
        st=[(y,x)]; lab[y,x]=True; c=[]
        while st:
            p=st.pop(); c.append(p)
            for dy in(-1,0,1):
                for dx in(-1,0,1):
                    Y,X=p[0]+dy,p[1]+dx
                    if ok(Y,X) and mask[Y,X] and not lab[Y,X]: lab[Y,X]=True; st.append((Y,X))
        out.append(c)
    return out
def foot(x,y,DY,SX=2):
    x0=9+(x-SX)/F_; x1=9+(x-SX+1)/F_; y0=6+(y-2-DY)/F_; y1=6+(y-1-DY)/F_
    for ny in range(int(np.floor(y0)),int(np.ceil(y1))):
        for nx in range(int(np.floor(x0)),int(np.ceil(x1))):
            w=(min(x1,nx+1)-max(x0,nx))*(min(y1,ny+1)-max(y0,ny))
            if w>0.02 and 0<=ny<99 and 0<=nx<99: yield w,ny,nx
IJZ=(N.min(2)<=215)&~(N[...,1]>N[...,0]+20)&(LUM>=70)
BRUIN=IJZ&((N[...,0]-N[...,2])>45)
def glad(M,sig):
    rr=int(np.ceil(3*sig)); k=np.exp(-np.arange(-rr,rr+1)**2/(2*sig*sig))
    cv=lambda a: np.apply_along_axis(lambda v:np.convolve(v,k,'same'),1,np.apply_along_axis(lambda v:np.convolve(v,k,'same'),0,a))
    return cv(LUM*M)/np.maximum(cv(M.astype(float)),1e-6)
def veld(Fd,M,x,y,DY):
    s=W=0
    for w,ny,nx in foot(x,y,DY):
        if M[ny,nx]: s+=w*Fd[ny,nx]; W+=w
    return s/W if W else None
def aandeel(M,x,y,DY):
    f=list(foot(x,y,DY)); W=sum(w for w,_,_ in f)
    return sum(w for w,ny,nx in f if M[ny,nx])/W if W else 0
a=r.copy()
groen=np.isin(r,list(GR))
gz=np.array([[groen[max(0,y-2):y+3,max(0,x-2):x+3].any() for x in range(64)] for y in range(64)])
rnd=np.array([[r[y,x] in IJ and rand(r,y,x) for x in range(64)] for y in range(64)])
def fm(y,x,fam=None):
    n=[v for v in nb8(a,y,x) if v in FILL and (fam is None or v in fam)]
    return Counter(n).most_common(1)[0][0] if n else None
# ---------- koeienvanger
KV=np.zeros((64,64),bool); KV[45:59,0:28]=True
g4=np.array([[any(ok(y+dy,x+dx) and r[y+dy,x+dx] in GR for dy,dx in((0,1),(1,0),(0,-1),(-1,0))) for x in range(64)] for y in range(64)])
kz=KV&np.isin(r,list(IJ))&~rnd&~((r==1)&g4)   # zwart dat het groen raakt (grijnsrand) blijft
for c in comps(kz&(r==1)):
    ext=any(ok(Y,X) and r[Y,X]==1 and not kz[Y,X] for y,x in c for Y in range(y-1,y+2) for X in range(x-1,x+2))
    if len(c)<3 and not ext:
        for y,x in c: a[y,x]=-1
MR=(N[...,0]-N[...,2]>45)&IJZ
GL=glad(IJZ,0.8)
kf=kz&(a!=1)
for y,x in zip(*np.where(kf)):
    l=veld(GL,IJZ,x,y,-1); l=100 if l is None else l
    if aandeel(MR,x,y,-1)>=0.40: a[y,x]=8 if l>105 else 9
    else: a[y,x]=10 if l>138 else (11 if l>88 else 12)
for c in comps(kf&np.isin(a,list(RUST))):
    if len(c)<3:
        for y,x in c: a[y,x]=-2
for y,x in zip(*np.where(a==-2)): a[y,x]=fm(y,x,GREY) or 11
for it in range(2):
    b=a.copy()
    for y,x in zip(*np.where(kf)):
        if nb8(a,y,x).count(a[y,x])==0: b[y,x]=fm(y,x,RUST if a[y,x] in RUST else GREY) or fm(y,x)
    a=b
b=a.copy()
for y,x in zip(*np.where(kf)):
    if a[y,x]==11 and a[y-1,x] in (1,8,9) and y<=50: b[y,x]=10
    elif a[y,x]==11 and ok(y,x+1) and a[y,x+1]==1 and y>=50: b[y,x]=12
a=b
# V-lijn onder de roestband: per kolom de rij met het grootste aandeel zwarte modelpixels (y45-49), gemeten op natief.png;
# erboven roest (band), eronder de lichte schuine bovenrand van de plaat.
VL={6:46,7:46,8:47,9:47,10:47,11:48,12:48,13:49,14:48,15:48,16:47,17:46,18:46,19:47,20:47,21:47,22:46,23:46,24:46}
for x,yl in VL.items():
    for y in range(45,yl+3):
        if not kz[y,x] or a[y,x] in GR: continue
        if y<yl: a[y,x]=9
        elif y==yl: a[y,x]=1
        elif y==yl+1:
            l=veld(GL,IJZ,x,y,-1) or 0
            if a[y,x] in GREY or a[y,x]==1: a[y,x]=10 if l>125 else (11 if a[y,x]==1 else a[y,x])
        elif y==yl+2 and a[y,x]==1 and (y+1>58 or a[y+1,x]!=1): a[y,x]=11
kop=np.zeros((64,64),bool); q=deque([(30,15)]); kop[30,15]=True
while q:
    y,x=q.popleft()
    for dy,dx in((0,1),(1,0),(0,-1),(-1,0)):
        Y,X=y+dy,x+dx
        if 20<=Y<=44 and ok(Y,X) and not kop[Y,X] and r[Y,X] in IJ: kop[Y,X]=True; q.append((Y,X))
gezicht=(r==1)&gz&kop&(np.arange(64)[:,None]>=26)
hz=kop&~gezicht&~rnd&~KV
for y,x in zip(*np.where(hz&(a==1))):
    if 1 not in nb8(a,y,x): a[y,x]=fm(y,x) or a[y,x]
GB=glad(BRUIN,3.0)
hb=hz&np.isin(a,[8,9])
v={(y,x):veld(GB,BRUIN,x,y,0) for y,x in zip(*np.where(hb))}
q25=np.percentile([t for t in v.values() if t is not None],25)
for (y,x),t in v.items():
    if t is not None: a[y,x]=9 if t<q25 else 8
for it in range(2):
    b=a.copy()
    for y,x in zip(*np.where(hz&np.isin(a,list(FILL)))):
        if nb8(a,y,x).count(a[y,x])==0: b[y,x]=fm(y,x,RUST if a[y,x] in RUST else GREY) or fm(y,x)
    a=b
# ---------- buitenlijn ijzer (kop + koeienvanger; lijf/wielen buiten beschouwing)
for y,x in zip(*np.where(rnd&(kop|KV))):
    if gezicht[y,x]: continue
    licht=(x>0 and a[y,x-1]==0 or (ok(y-1,x) and a[y-1,x]==0)) and y<40 and x<20
    if licht and a[y,x] in (1,8,9): a[y,x]=9
    elif licht and a[y,x] in GREY: a[y,x]=12
    elif not licht: a[y,x]=1
# ---------- bewijs bevroren
g=np.isin(r,list(GR))|np.isin(a,list(GR))
assert (a[g]==r[g]).all(),'groen gewijzigd'
assert (a[gezicht]==r[gezicht]).all(),'gezichtslijnen gewijzigd'
assert (a[:20]==r[:20]).all(),'rij 0-19 gewijzigd'
assert set(np.unique(a))<=set(np.unique(r)) and a.min()>=0,'nieuwe index'
print('gewijzigd: koeienvanger',int((a!=r)[KV].sum()),' kop',int((a!=r)[kop&~KV].sum()),' elders',int((a!=r)[~KV&~kop].sum()))
o=Image.fromarray(a.astype(np.uint8),'P'); o.putpalette(pal); o.info['transparency']=0
o.save(D+'sprite_r17/sprite.png',transparency=0)
o.resize((512,512),Image.NEAREST).save(D+'sprite_r17/sprite_8x.png',transparency=0)
with open(D+'sprite_r17/raster.txt','w') as f:
    for row in a: f.write(''.join('.' if q==0 else '%X'%q for q in row)+'\n')
