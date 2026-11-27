# Ronde 3: afwerking van manen A3 (model r3/model_A3.png, zie manen_a3.py) met de benoemde reparaties uit de r2-keuring:
# 2 manen: hoofdstrengen = de lange zwarte modellijnen tussen de lokken (skelet, gemeten plek) -> 'd'; overige modellijnen in
#   de manen worden haartint; per cel 3 haartinten uit de modelhelderheid (tertielen van het haar, licht -> donker per streng)
# 3 flankstrepen: per witte modelstreep een doorlopende 1-px-lijn (per spritenrij de kolom van het streepmidden in het model)
# 4 hoorns: band langs de middellijn, 4 px (2 binnen) tot 85% van de lengte, daarna 3; binnenkant per pixel uit het model:
#   wit (slijprand/voorkant van de draai) / licht staal / donker staal (achterkant van de draai)
# 5 oog: variant (a) = oog van de impala (af, B3) 1-op-1, omgekleurd; varianten in oog.py
# 6 hoeven: zoals de impala (gemeten: 4-5 px breed, 2-3 rijen, donkere tint met zwart rechts/onder)
import sys, json, math, numpy as np
from collections import Counter
from PIL import Image
from scipy import ndimage as nd
from reduce import fgmask, reduceer
from zones import pixzones, celstat, ZN
from hoorn import skelet, thin
RN='r3'; OOGVAR=sys.argv[1] if len(sys.argv)>1 and sys.argv[1] in 'abc' else 'a'
hx=lambda h: tuple(int(h[i:i+2],16) for i in (1,3,5))
PAL={'.':(0,0,0),'0':hx('#302418'),
     'L':hx('#F8D888'),'M':hx('#D8A850'),'D':hx('#A07030'),
     'l':hx('#D0A038'),'m':hx('#A87C24'),'d':hx('#6C4C14'),
     'A':hx('#3C4864'),'3':hx('#62749A'),'4':hx('#B4C4D8'),'W':hx('#FFFFFF'),
     'R':hx('#E0A090'),'r':hx('#B06A58'),'K':hx('#5C4434')}
ORDER=list(PAL); assert len(ORDER)<=16
Ld=lambda n:np.asarray(Image.open(n).convert('RGB'))
M0=Ld('../referenties/model_r3b.png'); A=Ld('r3/model_A3.png'); fg=fgmask(M0)
x0,y0,p,H,W=91,0,16.0,64,51
C=np.load('model_pal.npy'); KL=reduceer(A,fg,C,y0,x0,p,H,W)
HAAR=np.load('r3/manen_A3.npy')
Zp,lum=pixzones(A,fg,HAAR); F,LF,AL,LM=celstat(Zp,lum,y0,x0,p,H,W)
def cel(x,y):
    return slice(int(round(y0+y*p)),int(round(y0+(y+1)*p))),slice(int(round(x0+x*p)),int(round(x0+(x+1)*p)))
# haartinten: percentielen 20/60 van de haarhelderheid (zonder lijnen) per cel
hl=[LM[y,x,1] for y in range(H) for x in range(W) if KL[y,x]>=0 and F[y,x,1]>=0.3]
T1,T2=np.percentile(hl,[20,60])     # d = donkerste 20% (schaduw), m, l; de hoofdstrengen zijn ook d
def tint(z,l):
    if z=='vacht': return 'L' if l>=181 else 'M' if l>=140 else 'D'
    if z=='manen': return 'l' if l>=T2 else 'm' if l>=T1 else 'd'
    if z=='staal': return 'W' if l>=222 else '4' if l>=160 else '3'
    if z=='wit': return 'W'
    if z=='roze': return 'R' if l>=125 else 'r'
    return 'K'
g=[['.']*W for _ in range(H)]; zone=[['']*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        if KL[y,x]<0: continue
        fr=F[y,x].copy(); fr[3]=0 if fr[3]<0.5 else fr[3]
        zi=int(fr.argmax()); z=ZN[zi]; zone[y][x]=z
        g[y][x]='0' if KL[y,x]==0 else tint(z,LM[y,x,zi])
kaal=[r[:] for r in g]
log=[]
def put(zn,x,y,c,why):
    old=g[y][x]
    if old!=c: g[y][x]=c; log.append((zn,x,y,old,c,why))
def opaque(x,y): return 0<=x<W and 0<=y<H and g[y][x]!='.'
N4=((1,0),(-1,0),(0,1),(0,-1))
# --- 2 manen: hoofdstrengen uit het model, de rest haartint ---
haar=nd.binary_closing(HAAR|(Zp==1),iterations=4)&fg
lab,n=nd.label(nd.binary_dilation(haar&(lum<80),iterations=1))
STRENG=set(); streng_info=[]
for k in range(1,n+1):
    m=lab==k
    if m.sum()<150: continue
    sk=thin(m.reshape(256,4,256,4).max((1,3)))
    if sk.sum()<20: continue                                   # alleen hoofdlijnen (skelet >= 80 modelpx)
    ys,xs=np.nonzero(sk); cells={(int((xx*4+2-x0)//p),int((yy*4+2-y0)//p)) for yy,xx in zip(ys,xs)}
    cells={c for c in cells if 0<=c[0]<W and 0<=c[1]<H and KL[c[1],c[0]]>=0}
    streng_info.append((int(sk.sum()),len(cells),cells))
# max 6 hoofdstrengen, langste eerst; een streng die voor >40% binnen 1 kolom naast een al gekozen streng loopt (dubbele lijn
# van origineel + verschoven kopie) valt af, zodat de strengen >=2 px uit elkaar liggen en als lokken lezen
streng_info.sort(key=lambda t:-t[0]); gekozen=[]
for L_,nc,cells in streng_info:
    if len(gekozen)>=6: break
    dicht=sum(1 for (cx,cy) in cells if any((cx+a,cy) in STRENG for a in (-1,1)) and (cx,cy) not in STRENG)
    if dicht>0.4*len(cells): continue
    gekozen.append((L_,nc)); STRENG|=cells
streng_info=gekozen
def HK(x,y):
    # haartoon per cel = meerderheid van de modelhaarpixels (zonder lijn): licht >=140 (192,156,36 / 180,144,36), midden 118-140
    # (156,120,24), donker <118 (144,108,24) -> l/m/d. Meerderheid i.p.v. gemiddelde: geen mengtinten (r2: "bruine ruisvlek")
    ys_,xs_=cel(x,y); m=(Zp[ys_,xs_]==1)
    if m.sum()<30: return None
    l=lum[ys_,xs_][m]; bc=[(l>=140).sum(),((l>=118)&(l<140)).sum(),(l<118).sum()]
    return 'lmd'[int(np.argmax(bc))]
for y in range(H):
    for x in range(W):
        if zone[y][x]!='manen' and not (g[y][x]=='0' and F[y,x,1]>=0.3): continue
        if (x,y) in STRENG and any(opaque(x+a,y+b) for a,b in N4): put('manen',x,y,'d','hoofdstreng: zwarte modellijn tussen de lokken -> d'); zone[y][x]='manen'; continue
        if g[y][x]=='0' and not all(opaque(x+a,y+b) for a in(-1,0,1) for b in(-1,0,1)): continue
        hk=HK(x,y)
        if hk: put('manen',x,y,hk,'haartint: meest voorkomende haartoon van het model in de cel (harde toongrenzen zoals het model)'); zone[y][x]='manen'
# lokken tussen de hoofdstrengen: per rij is elk stuk manen tussen twee strenglijnen een lok. Het model heeft daar fijne
# haartjes (smaller dan 2 spritepx; 1-op-1 gaf een zebra "dldld"); per lok de lichte kant uit het model (gem. haarhelderheid
# linkerhelft vs rechterhelft van het stuk in het model): lichte kant l, donkere kant m (randpixel naast de lijn), lijn d.
lokken=0
for y in range(H):
    xs_=[x for x in range(W) if zone[y][x]=='manen' and g[y][x] in 'lmd' and (x,y) not in STRENG]
    seg=[];cur=[]
    for x in xs_:
        if cur and x!=cur[-1]+1: seg.append(cur); cur=[]
        cur.append(x)
    if cur: seg.append(cur)
    for sgm in seg:
        if len(sgm)<2: continue
        if not any((x,y) in STRENG for x in (sgm[0]-1,sgm[-1]+1)): continue     # alleen stukken die aan een strenglijn grenzen
        h=len(sgm)//2
        def ml(cs):
            v=[]
            for x in cs:
                ys_,xs2=cel(x,y); m=Zp[ys_,xs2]==1
                if m.any(): v.append(lum[ys_,xs2][m].mean())
            return np.mean(v) if v else 0
        links_licht=ml(sgm[:h])>=ml(sgm[h:])
        for i,x in enumerate(sgm):
            rel=i/(len(sgm)-1)
            if not links_licht: rel=1-rel
            c='l' if rel<0.5 else 'm'
            put('manen',x,y,c,'lok: lichte kant uit het model l, donkere kant m'); lokken+=1
# --- wit: gezicht (V, wangvlekjes, lip) uit de witfractie; flankstrepen als doorlopende 1-px-lijnen ---
WF=F[...,3]
for y in range(18,31):
    for x in range(0,17):
        if KL[y,x]>0 and WF[y,x]>=0.3: put('wit',x,y,'W','witte tekening gezicht (witfractie %.2f)'%WF[y,x])
yy,xx=np.mgrid[:1024,:1024]
wit=fg&(lum>=200)&(A[...,2]>120)&(xx>=470)&(yy>=450)&(yy<760)     # crèmewitte strepen (lum>=200, blauw>120: geen lichte vacht)
lab,n=nd.label(nd.binary_dilation(wit,iterations=2))
STREPEN=[]
for k in range(1,n+1):
    ys,xs=np.nonzero((lab==k)&wit)
    if ys.max()-ys.min()<40: continue
    lijn=[]
    for r in range(int(ys.min()//p),int(ys.max()//p)+1):
        sel=(ys>=r*p)&(ys<(r+1)*p)
        if sel.sum()<3: continue
        lijn.append((int((xs[sel].mean()-x0)//p),r))
    STREPEN.append(lijn)
for lijn in STREPEN:
    for x,y in lijn:
        if g[y][x] not in '.0' or (opaque(x-1,y) and opaque(x+1,y) and opaque(x,y-1) and opaque(x,y+1)):
            if all(opaque(x+a,y+b) for a,b in N4): put('wit',x,y,'W','flankstreep: doorlopende lijn op het streepmidden van het model')
# vacht tussen de strepen: witte cellen uit r2-stijl (witfractie) die niet op een streep liggen -> vacht
OP=set(c for l in STREPEN for c in l)
for y in range(H):
    for x in range(17,W):
        if g[y][x]=='W' and zone[y][x]=='vacht' and (x,y) not in OP: put('wit',x,y,tint('vacht',LM[y,x,0] or 176),'wit naast de streep -> vacht')
# --- 4 hoorns ---
SK=skelet(Zp,x0,y0,p); json.dump(SK,open(f'{RN}/hoornskelet.json','w'))
def herbemonster(P,stap=0.2):
    P=np.array(P,float); L=np.r_[0,np.cumsum(np.hypot(*np.diff(P,axis=0).T))]
    s=np.r_[np.arange(0,L[-1],stap),L[-1]]; return np.c_[np.interp(s,L,P[:,0]),np.interp(s,L,P[:,1])]
def glad(Q,n,k):
    for _ in range(k):
        R=Q.copy()
        for i in range(1,len(Q)-1): a,b=max(0,i-n),min(len(Q),i+n+1); R[i]=Q[a:b].mean(0)
        Q=R
    return Q
def breedte(s): return 4.2 if s<=0.85 else 4.2-(s-0.85)/0.15*1.6
SUB=8; off=(np.arange(SUB)+.5)/SUB; HOORN={}
for naam,v in SK.items():
    Q=glad(herbemonster(v['pts']),5,2); Aa=Q[:-1]; D=Q[1:]-Aa; L2=(D**2).sum(1); L2[L2==0]=1e-9
    S=np.r_[0,np.cumsum(np.sqrt(L2))]; S/=S[-1]; WS=np.array([breedte(s) for s in S]); Mh=set()
    for y in range(0,24):
        for x in range(0,W):
            if min(np.hypot(Q[:,0]-x-.5,Q[:,1]-y-.5))>3: continue
            Pp=np.c_[(x+off[None,:]).repeat(SUB,0).ravel(),(y+off[:,None]).repeat(SUB,1).ravel()]
            t=np.clip((((Pp[:,None,:]-Aa[None])*D[None]).sum(2))/L2[None],0,1)
            Cc=Aa[None]+t[...,None]*D[None]; d=np.hypot(*(Pp[:,None,:]-Cc).transpose(2,0,1))
            k=d.argmin(1); tt=t[np.arange(len(k)),k]; w=WS[k]*(1-tt)+WS[k+1]*tt
            if (d[np.arange(len(k)),k]<=w/2).mean()>=0.5: Mh.add((x,y))
    HOORN[naam]=(Q,Mh)
ALLE=HOORN['links'][1]|HOORN['rechts'][1]
for y in range(0,22):
    for x in range(W):
        if g[y][x]=='.' or (x,y) in ALLE: continue
        if F[y,x,2]>=0.2 and F[y,x,2]+LF[y,x]>=0.7 and F[y,x,0]+F[y,x,4]<0.3: put('hoorn',x,y,'.','oude hoornrest buiten de hoornband weg')
def SL(x,y):
    ys_,xs_=cel(x,y); m=Zp[ys_,xs_]==2
    if m.sum()>=20: return float(lum[ys_,xs_][m].mean())
    v=[LM[y+b,x+a,2] for a in(-1,0,1) for b in(-1,0,1) if 0<=y+b<H and 0<=x+a<W and F[y+b,x+a,2]>=0.1]
    return float(np.mean(v)) if v else 170.0
def WITF(x,y):
    ys_,xs_=cel(x,y); m=Zp[ys_,xs_]==2
    return float((lum[ys_,xs_][m]>=222).mean()) if m.sum()>=10 else 0.0
INN=[]
for naam,(Q,Mh) in HOORN.items():
    for (x,y) in Mh:
        if y>=15 and g[y][x]!='.' and F[y,x,2]+LF[y,x]<0.5: continue
        zone[y][x]='staal'
        if any((x+dx,y+dy) not in Mh for dx,dy in N4): put('hoorn',x,y,'0','hoornrand: lijn'); continue
        INN.append((naam,x,y))
for naam,x,y in INN:
    Q,Mh=HOORN[naam]
    d=np.hypot(Q[:,0]-(x+.5),Q[:,1]-(y+.5)); k=int(d.argmin()); dx,dy=Q[min(k+3,len(Q)-1)]-Q[max(k-3,0)]
    nn=math.hypot(dx,dy) or 1; nx_,ny_=dy/nn,-dx/nn
    q=(int(math.floor(x+.5+nx_)),int(math.floor(y+.5+ny_))); r_=(int(math.floor(x+.5-nx_)),int(math.floor(y+.5-ny_)))
    binnen=lambda t: t in Mh and all((t[0]+a,t[1]+b) in Mh for a,b in N4)
    own=SL(x,y); bur=[SL(*t) for t in (q,r_) if binnen(t)]; wf=WITF(x,y)
    if bur:   # 2 px binnen: lichtste over de breedte = voorkant/slijprand (W als het model daar wit heeft), andere = achterkant
        if own>=max(bur): c='W' if wf>=0.2 else '4'
        else: c='3' if own<200 else '4'
    else: c='W' if wf>=0.5 else '4' if own>=175 else '3'
    put('hoorn',x,y,c,'hoorn: modelhelderheid %.0f, wit %.0f%% (voorkant/slijprand W, licht 4, achterkant 3)'%(own,wf*100))
# slijprand: elke binnenkant die over de breedte geen W heeft maar wel een lichtere kant, krijgt W op de lichtste pixel
# --- ontkorrelen (niet op strengen, strepen, oog) ---
def comps():
    seen=set(); res=[]
    for y in range(H):
        for x in range(W):
            if (x,y) in seen or g[y][x] in '.0W': continue
            v=g[y][x]; st=[(x,y)]; seen.add((x,y)); cc=[]
            while st:
                cx,cy=st.pop(); cc.append((cx,cy))
                for dx,dy in N4:
                    nx,ny=cx+dx,cy+dy
                    if 0<=nx<W and 0<=ny<H and (nx,ny) not in seen and g[ny][nx]==v: seen.add((nx,ny)); st.append((nx,ny))
            res.append((v,cc))
    return res
for _ in range(3):
    for v,cc in comps():
        if len(cc)>=3 or v not in 'LMDlmd': continue
        if v=='d' and any(c in STRENG for c in cc): continue
        grp='LMD' if v in 'LMD' else 'lmd'
        nb=Counter(g[y+dy][x+dx] for x,y in cc for dx,dy in N4 if opaque(x+dx,y+dy) and g[y+dy][x+dx] in grp and g[y+dy][x+dx]!=v and not (g[y+dy][x+dx]=='d' and (x+dx,y+dy) in STRENG))
        if nb:
            for x,y in cc: put('ontkorrel',x,y,nb.most_common(1)[0][0],'tintvlakje <3 px naar buurtint')
# --- binnenlijnen (buiten de manen) ---
DARK={'vacht':'D','manen':'d','staal':'A','roze':'r','donker':'K','wit':'D'}
def buurzone(x,y):
    c=Counter(zone[y+b][x+a] for a in(-1,0,1) for b in(-1,0,1) if opaque(x+a,y+b) and g[y+b][x+a]!='0' and zone[y+b][x+a])
    return c.most_common(1)[0][0] if c else 'vacht'
OOG=(9,20,15,25)
for y in range(H):
    for x in range(W):
        if g[y][x]=='0' and all(opaque(x+a,y+b) for a in(-1,0,1) for b in(-1,0,1)) and not (OOG[0]<=x<=OOG[2] and OOG[1]<=y<=OOG[3]):
            put('binnenlijn',x,y,DARK[buurzone(x,y)],'binnenlijn in donkerste eigen tint')
# --- 5 oog (variant a/b/c, oog.py) ---
import oog
for x,y,c,why in oog.variant(OOGVAR): put('oog',x,y,c,why)
# --- poten (Kirlia) ---
runs={}
for y in range(47,H):
    x=0
    while x<W:
        if g[y][x] not in '.0' and zone[y][x]=='vacht':
            a=x
            while x+1<W and g[y][x+1] not in '.0': x+=1
            if x-a+1<=2: runs.setdefault(y,[]).append((a,x))
        x+=1
POTEN=[]
for y in sorted(runs):
    for a,b in runs[y]:
        for P in POTEN:
            py,pa,pb=P[-1]
            if py==y-1 and a<=pb+1 and b>=pa-1: P.append((y,a,b)); break
        else: POTEN.append([(y,a,b)])
POTEN=[P for P in POTEN if len(P)>=6]
for P in POTEN:
    ver=Counter(g[y][x] for y,a,b in P for x in range(a,b+1)).most_common(1)[0][0]=='D'
    n=len(P)
    for k,(y,a,b) in enumerate(P):
        s_=k/(n-1)
        t=('D' if s_<0.3 or s_>0.8 else 'M') if ver else ('M' if s_<0.3 or s_>0.8 else 'L')
        for x in range(a,b+1):
            if zone[y][x]=='vacht' and g[y][x] in 'LMD': put('poot',x,y,t,'Kirlia: tint in de lengte')
        if a-1>=0 and g[y][a-1]=='0': put('poot',a-1,y,'D','Kirlia: linkerlijn donkere eigen tint')
# --- 6 hoeven zoals de impala (gemeten: 4-5 px breed tegen poot 3, 2-3 rijen, donkerste tint met zwart rechts/onder): per poot (component onder rij 50) de onderste 2 rijen, 1 px breder naar rechts ---
HOEF=[]
lab_,n_=nd.label(np.array([[g[y][x]!='.' and y>=50 for x in range(W)] for y in range(H)]))
for k in range(1,n_+1):
    ys,xs=np.nonzero(lab_==k)
    if ys.max()<58: continue
    yb=ys.max()
    for y in (yb-1,yb):
        xr=xs[ys==y]
        if not len(xr): continue
        for x in range(xr.min(),xr.max()+2):
            if x<W: HOEF.append((x,y))
for x,y in HOEF:
    rechts=not opaque(x+1,y) or (x+1,y) not in HOEF
    onder=y+1>=H or (x,y+1) not in HOEF
    if g[y][x]=='.': g[y][x]='0'; zone[y][x]='donker'; log.append(('hoef',x,y,'.','0','hoef 1 px breder dan de poot (impala: hoef 4-5 px, poot 3)'))
    put('hoef',x,y,'0' if (rechts or onder) else 'K','hoef zoals de impala: binnen donker, rechts/onder zwart'); zone[y][x]='donker'
# --- buitenlijn + selout ---
for y in range(H):
    for x in range(W):
        if g[y][x] not in '.0K' and any(not opaque(x+a,y+b) for a,b in N4): put('lijn',x,y,'0','buitenlijn dicht')
SEL={'vacht':'D','manen':'d','staal':'3','roze':'r','donker':'K','wit':'D'}
for y in range(H):
    for x in range(W):
        if g[y][x]!='0' or (x,y) in HOEF: continue
        tv=[(a,b) for a in range(-2,3) for b in range(-2,3) if (a or b) and not opaque(x+a,y+b)]
        if not tv: continue
        nx_=sum(d[0] for d in tv); ny_=sum(d[1] for d in tv); nn=math.hypot(nx_,ny_) or 1
        if not (ny_/nn<-0.35 and nx_/nn<=0.3): continue
        z=zone[y][x] if zone[y][x] in SEL else buurzone(x,y)
        if z=='staal': put('lijn',x,y,'A','selout lichtkant (staal, donkerste staaltint)'); continue
        if not any(opaque(x+a,y+b) and g[y+b][x+a] not in '0' for a,b in ((1,0),(0,1),(1,1),(-1,1))): continue
        put('lijn',x,y,SEL.get(z,'D'),'selout lichtkant')
# --- uitvoer ---
OX=(64-W)//2; OY=64-H
def png(G,pad):
    img=np.zeros((64,64),'uint8')
    for y in range(H):
        for x in range(W): img[OY+y,OX+x]=ORDER.index(G[y][x])
    pal=[v for k in ORDER for v in PAL[k]]; pal+=[0]*(48-len(pal))
    im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(pad,transparency=0)
naam=f'kudu_{RN}' if OOGVAR=='a' else f'kudu_{RN}_oog{OOGVAR}'
png(g,f'{RN}/{naam}.png'); png(kaal,f'{RN}/kaal_gemapt.png')
Image.open(f'{RN}/{naam}.png').convert('RGBA').resize((512,512),Image.NEAREST).save(f'{RN}/{naam}_8x.png')
if OOGVAR=='a':
    json.dump({'grid':[''.join(r) for r in g],'kaal':[''.join(r) for r in kaal]},open(f'{RN}/grid.json','w'))
    with open(f'{RN}/wijzigingen.txt','w') as f:
        for e in log: f.write('%s (%d,%d) %s->%s  %s\n'%e)
    eind=Counter()
    for y in range(H):
        for x in range(W):
            if g[y][x]!=kaal[y][x]: eind[zone[y][x] or 'weg (transparant)']+=1
    with open(f'{RN}/telling.txt','w') as f:
        f.write('Pixels anders dan de kale reductie van model A3 (kaal gemapt), per zone: %s, totaal %d van %d\n'%(dict(eind),sum(eind.values()),sum(c!='.' for r in g for c in r)))
        f.write('Per stap: %s\n'%dict(Counter(z for z,*_ in log)))
        f.write('Hoofdstrengen (skeletlengte /4 modelpx, cellen): %s\n'%streng_info)
        f.write('Flankstrepen: %d, rijen per streep %s\n'%(len(STREPEN),[len(l) for l in STREPEN]))
        f.write('Haartinten: grenzen p20/p60 %.0f / %.0f\n'%(T1,T2))
    print(open(f'{RN}/telling.txt').read())
print('kleuren',len(set(c for r in g for c in r)))
if '-v' in sys.argv: print('\n'.join('%2d '%j+''.join(r) for j,r in enumerate(g)))
