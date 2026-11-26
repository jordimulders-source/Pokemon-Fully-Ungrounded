# Ronde 2: afwerking van manenvariant A (model r2/model_A2a.png: boog weg, lokpunten uit de keelfranje van r3b, geen dubbele kam).
# Volgorde: kale reductie (reduce.py, 64 rijen, cel 16) -> zones (zones.py) -> tinten uit de modelhelderheid per cel ->
# wit (strepen/V/vlekjes/lip) uit de witfractie per cel -> hoorns als band langs het modelskelet (hoorn.py) -> ontkorrelen ->
# binnenlijnen in de donkerste eigen tint -> buitenlijn zwart + selout lichtkant. Elke afwijking van de kale reductie gelogd per zone.
import sys, json, math, numpy as np
from collections import Counter
from PIL import Image
from reduce import fgmask, reduceer
from zones import pixzones, celstat, ZN
from hoorn import skelet
VAR=sys.argv[1] if len(sys.argv)>1 else 'A2a'; RN=sys.argv[2] if len(sys.argv)>2 else 'r2'
hx=lambda h: tuple(int(h[i:i+2],16) for i in (1,3,5))
PAL={'.':(0,0,0),'0':hx('#302418'),                                   # omlijning warm donker
     'L':hx('#F8D888'),'M':hx('#D8A850'),'D':hx('#A07030'),            # vacht goud (mat, warm)
     'l':hx('#D0A038'),'m':hx('#A87C24'),'d':hx('#6C4C14'),            # manen/keelfranje: donkerder goud
     'A':hx('#4A5A7B'),'3':hx('#7B8FAE'),'4':hx('#BCCBDD'),'W':hx('#FFFFFF'),   # staal (Steelix-tinten) + wit (slijprand/tekening)
     'R':hx('#E0A090'),'r':hx('#B06A58'),'K':hx('#5C4434')}           # oor roze, neus/hoef
ORDER=list(PAL); assert len(ORDER)<=16
Ld=lambda n:np.asarray(Image.open(n).convert('RGB'))
M0=Ld('../referenties/model_r3b.png'); A=Ld(f'r2/model_{VAR}.png'); fg=fgmask(M0)
x0,y0,p,H,W=91,0,16.0,64,51
C=np.load('model_pal.npy'); KL=reduceer(A,fg,C,y0,x0,p,H,W)       # kale reductie (modelkleuren), index 0 = lijn
Zp,lum=pixzones(A,fg); F,LF,AL,LM=celstat(Zp,lum,y0,x0,p,H,W)
lumC=(C*[.299,.587,.114]).sum(1)
def tint(z,l):
    if z=='vacht': return 'L' if l>=181 else 'M' if l>=140 else 'D'
    if z=='manen': return 'l' if l>=145 else 'm' if l>=118 else 'd'
    if z=='staal': return 'W' if l>=222 else '4' if l>=160 else '3' if l>=110 else 'A'
    if z=='wit': return 'W'
    if z=='roze': return 'R' if l>=125 else 'r'
    return 'K'
g=[['.']*W for _ in range(H)]; zone=[['']*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        if KL[y,x]<0: continue
        fr=F[y,x].copy(); fr[3]=0 if fr[3]<0.5 else fr[3]       # wit pas hieronder apart
        zi=int(fr.argmax()); z=ZN[zi]; zone[y][x]=z
        if KL[y,x]==0: g[y][x]='0'
        else: g[y][x]=tint(z,LM[y,x,zi])
kaal=[r[:] for r in g]                      # kaal gemapt: zelfde cellen als de kale reductie, alleen omgekleurd
log=[]
def put(zn,x,y,c,why):
    old=g[y][x]
    if old!=c: g[y][x]=c; log.append((zn,x,y,old,c,why))
def opaque(x,y): return 0<=x<W and 0<=y<H and g[y][x]!='.'
N4=((1,0),(-1,0),(0,1),(0,-1))
# --- wit uit het model: strepen (lijf, 1 px breed: per horizontale reeks de cel met de hoogste witfractie), V, wangvlekjes, lip ---
WF=F[...,3]
for y in range(H):
    x=0
    while x<W:
        if KL[y,x]>0 and WF[y,x]>=0.16 and y>=18:
            run=[x]
            while x+1<W and WF[y,x+1]>=0.16: x+=1; run.append(x)
            gezicht=run[0]<17 and y<31
            keep=[i for i in run if WF[y,i]>=0.3] if gezicht else [max(run,key=lambda i:WF[y,i])]
            for i in keep:
                if g[y][i]!='.': put('wit',i,y,'W','witte tekening uit het model (witfractie %.2f)'%WF[y,i])
        x+=1
# --- hoorns: band langs de modelmiddellijn, breedte 4 (voet) -> 3 -> punt ---
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
def breedte(s):
    if s<=0.55: return 4.0
    if s<=0.85: return 4.0-(s-0.55)/0.30*1.0
    return 3.0-(s-0.85)/0.15*1.5
SUB=8; off=(np.arange(SUB)+.5)/SUB; HOORN={}
for naam,v in SK.items():
    Q=glad(herbemonster(v['pts']),5,2); Aa=Q[:-1]; D=Q[1:]-Aa; L2=(D**2).sum(1); L2[L2==0]=1e-9
    S=np.r_[0,np.cumsum(np.sqrt(L2))]; S/=S[-1]; WS=np.array([breedte(s) for s in S]); M=set()
    for y in range(0,24):
        for x in range(0,W):
            if min(np.hypot(Q[:,0]-x-.5,Q[:,1]-y-.5))>3: continue
            Pp=np.c_[(x+off[None,:]).repeat(SUB,0).ravel(),(y+off[:,None]).repeat(SUB,1).ravel()]
            t=np.clip((((Pp[:,None,:]-Aa[None])*D[None]).sum(2))/L2[None],0,1)
            Cc=Aa[None]+t[...,None]*D[None]; d=np.hypot(*(Pp[:,None,:]-Cc).transpose(2,0,1))
            k=d.argmin(1); tt=t[np.arange(len(k)),k]; w=WS[k]*(1-tt)+WS[k+1]*tt
            if (d[np.arange(len(k)),k]<=w/2).mean()>=0.5: M.add((x,y))
    HOORN[naam]=(Q,M)
ALLE=HOORN['links'][1]|HOORN['rechts'][1]
def SL(x,y):
    # gemiddelde helderheid van de staalpixels van het model in de cel (lege cel: gemiddelde van de buurcellen)
    xa,xb=int(round(x0+x*p)),int(round(x0+(x+1)*p)); ya,yb=int(round(y0+y*p)),int(round(y0+(y+1)*p))
    m=Zp[ya:yb,xa:xb]==2
    if m.sum()>=20: return float(lum[ya:yb,xa:xb][m].mean())
    v=[LM[y+b,x+a,2] for a in(-1,0,1) for b in(-1,0,1) if 0<=y+b<H and 0<=x+a<W and F[y+b,x+a,2]>=0.1]
    return float(np.mean(v)) if v else 170.0
def STK(x,y):
    # staaltoon per cel uit de modelpixels: wit (lum>=235, slijprand/spiegelglans) -> W, licht (190-235) -> 4, grijs (<190) -> 3
    if not(0<=x<W and 0<=y<H): return None
    xa,xb=int(round(x0+x*p)),int(round(x0+(x+1)*p)); ya,yb=int(round(y0+y*p)),int(round(y0+(y+1)*p))
    m=Zp[ya:yb,xa:xb]==2
    if m.sum()<20: return None
    l=lum[ya:yb,xa:xb][m]; bc=[(l>=235).sum(),((l>=190)&(l<235)).sum(),(l<190).sum()]
    return 'W4 3'.replace(' ','')[int(np.argmax(bc))] if False else ['W','4','3'][int(np.argmax(bc))]
# oude hoornreductie buiten de nieuwe band weg (cellen met overwegend staal/lijn boven de kop)
for y in range(0,22):
    for x in range(W):
        if g[y][x]=='.' or (x,y) in ALLE: continue
        if F[y,x,2]>=0.2 and F[y,x,2]+LF[y,x]>=0.7 and F[y,x,0]+F[y,x,4]<0.3: put('hoorn',x,y,'.','oude hoornrest buiten de hoornband weg')
INN=[]
for naam,(Q,M) in HOORN.items():
    for (x,y) in M:
        if y>=15 and g[y][x]!='.' and F[y,x,2]+LF[y,x]<0.5: continue   # hoornvoet: kop/oor ligt ervoor waar het model daar geen hoorn heeft
        zone[y][x]='staal'
        if any((x+dx,y+dy) not in M for dx,dy in N4): put('hoorn',x,y,'0','hoornrand: lijn'); continue
        # binnen: modelhelderheid van het staal in de cel (wit = slijprand/glans in het model); geen staal in de cel -> buurcellen
        INN.append((naam,x,y))
for naam,x,y in INN:
    Q,M=HOORN[naam]
    d=np.hypot(Q[:,0]-(x+.5),Q[:,1]-(y+.5)); k=int(d.argmin()); dx,dy=Q[min(k+3,len(Q)-1)]-Q[max(k-3,0)]
    nn=math.hypot(dx,dy) or 1; nx_,ny_=dy/nn,-dx/nn            # normaal naar links van voet->punt
    q=(int(math.floor(x+.5+nx_)),int(math.floor(y+.5+ny_))); r_=(int(math.floor(x+.5-nx_)),int(math.floor(y+.5-ny_)))
    binnen=lambda t: t in M and all((t[0]+a,t[1]+b) in M for a,b in N4)
    own=SL(x,y); buren=[SL(*t) for t in (q,r_) if binnen(t)]
    if not buren: c='W' if own>=215 else '4'                     # 1 px binnen (taps): licht staal, wit waar het model wit is
    elif own>=max(buren): c='W' if own>=200 else '4'            # lichtste over de breedte = slijprand/spiegelglans (model)
    else: c='3'                                                  # donkere kant
    put('hoorn',x,y,c,'hoornbinnenkant: licht/donker over de breedte gemeten in het model (staalhelderheid %.0f)'%own)
# --- ontkorrelen: tintvlakjes <3 px in vacht/manen -> meest voorkomende buurtint in dezelfde zone ---
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
        nb=Counter(g[y+dy][x+dx] for x,y in cc for dx,dy in N4 if opaque(x+dx,y+dy) and g[y+dy][x+dx] in ('LMD' if v in 'LMD' else 'lmd') and g[y+dy][x+dx]!=v)
        if nb:
            for x,y in cc: put('ontkorrel',x,y,nb.most_common(1)[0][0],'tintvlakje <3 px naar buurtint')
# --- binnenlijnen: lijncel binnen het silhouet -> donkerste eigen tint (manen d, vacht D, staal A, roze r, donker K) ---
DARK={'vacht':'D','manen':'d','staal':'A','roze':'r','donker':'K','wit':'D'}
def buurzone(x,y):
    c=Counter(zone[y+b][x+a] for a in(-1,0,1) for b in(-1,0,1) if opaque(x+a,y+b) and g[y+b][x+a]!='0' and zone[y+b][x+a])
    return c.most_common(1)[0][0] if c else 'vacht'
OOG=(10,21,15,24)   # oogzone (lokaal x0,y0,x1,y1): lijnen blijven zwart (gesloten modeloog)
inner=[(x,y) for y in range(H) for x in range(W) if g[y][x]=='0' and all(opaque(x+a,y+b) for a in(-1,0,1) for b in(-1,0,1))
       and not (OOG[0]<=x<=OOG[2] and OOG[1]<=y<=OOG[3])]
for x,y in inner:
    z=buurzone(x,y)
    if z=='staal' and any(zone[y+b][x+a] in('vacht','manen','roze') for a,b in N4 if opaque(x+a,y+b)): z='staal'
    put('binnenlijn',x,y,DARK[z],'binnenlijn in donkerste eigen tint')
# --- poten volgens Kirlia (Jordi 26 nov, impala): tint in de lengte, midden bij het gewricht, licht op de scheen, midden onderaan;
#     linkerlijn donkere eigen tint, rechts zwart; verre poot een tintstap donkerder. Pootvulling = 1-2 px tussen lijnen, rij>=47.
LEG0=47
runs={}
for y in range(LEG0,H):
    x=0
    while x<W:
        if g[y][x] not in '.0' and zone[y][x]=='vacht':
            a=x
            while x+1<W and g[y][x+1] not in '.0': x+=1
            if x-a+1<=2: runs.setdefault(y,[]).append((a,x))
        x+=1
POTEN=[]   # koppel runs per rij aan poten (overlap/nabijheid met de rij erboven)
for y in sorted(runs):
    for a,b in runs[y]:
        for P in POTEN:
            py,pa,pb=P[-1]
            if py==y-1 and a<=pb+1 and b>=pa-1: P.append((y,a,b)); break
        else: POTEN.append([(y,a,b)])
POTEN=[P for P in POTEN if len(P)>=6]
for P in POTEN:
    ver=Counter(g[y][x] for y,a,b in P for x in range(a,b+1)).most_common(1)[0][0]=='D'   # verre poot: model donkerder
    n=len(P)
    for k,(y,a,b) in enumerate(P):
        s_=k/(n-1)
        t=('D' if s_<0.3 or s_>0.8 else 'M') if ver else ('M' if s_<0.3 or s_>0.8 else 'L')
        for x in range(a,b+1):
            if zone[y][x]=='vacht' and g[y][x] in 'LMD': put('poot',x,y,t,'Kirlia: tint in de lengte ('+('verre' if ver else 'nabije')+' poot)')
        if a-1>=0 and g[y][a-1]=='0': put('poot',a-1,y,'D' if not ver else 'D','Kirlia: linkerlijn donkere eigen tint')
hoef=[]
for y in range(56,H):
    for x in range(W):
        if g[y][x]!='.' and F[y,x,5]>=0.3: put('hoef',x,y,'K','hoef: donkere modeltint (neus/hoef)'); hoef.append((x,y))
# --- buitenlijn dicht + selout aan de lichtkant (rand wijst naar boven/linksboven) ---
for y in range(H):
    for x in range(W):
        if g[y][x] not in '.0K' and any(not opaque(x+a,y+b) for a,b in N4): put('lijn',x,y,'0','buitenlijn dicht')
SEL={'vacht':'D','manen':'d','staal':'3','roze':'r','donker':'K','wit':'D'}
for y in range(H):
    for x in range(W):
        if g[y][x]!='0': continue
        tv=[(a,b) for a in range(-2,3) for b in range(-2,3) if (a or b) and not opaque(x+a,y+b)]
        if not tv: continue
        nx_=sum(d[0] for d in tv); ny_=sum(d[1] for d in tv); nn=math.hypot(nx_,ny_) or 1
        if not (ny_/nn<-0.35 and nx_/nn<=0.3): continue
        z=zone[y][x] if zone[y][x] in SEL else buurzone(x,y)
        if z=='staal': put('lijn',x,y,'3','selout lichtkant (staal)'); continue
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
png(g,f'{RN}/kudu_{RN}.png'); png(kaal,f'{RN}/kaal_gemapt.png')
Image.open(f'{RN}/kudu_{RN}.png').convert('RGBA').resize((512,512),Image.NEAREST).save(f'{RN}/kudu_{RN}_8x.png')
json.dump({'grid':[''.join(r) for r in g],'kaal':[''.join(r) for r in kaal],'zone':[[z for z in r] for r in zone]},open(f'{RN}/grid.json','w'))
with open(f'{RN}/wijzigingen.txt','w') as f:
    for e in log: f.write('%s (%d,%d) %s->%s  %s\n'%e)
cnt=Counter(z for z,*_ in log)
used=set(c for r in g for c in r)
print(RN,VAR,'afwijkingen van kaal gemapt per stap:',dict(cnt),'totaal',len(log),'| kleuren',len(used),'(incl. transparant)')
if '-q' not in sys.argv: print('\n'.join('%2d '%j+''.join(r) for j,r in enumerate(g)))
# --- telling per zone t.o.v. de kale reductie (kaal gemapt = zelfde cellen, alleen omgekleurd naar het Gen 3-palet) ---
per=Counter(); stap=Counter()
for zn,x,y,o,c,why in log:
    z=zone[y][x] or 'weg'; per[z]+=1
eind=Counter(); 
for y in range(H):
    for x in range(W):
        if g[y][x]!=kaal[y][x]: eind[zone[y][x] or 'weg (transparant)']+=1
with open(f'{RN}/telling.txt','w') as f:
    f.write('Pixels anders dan de kale reductie (kaal gemapt), per zone (eindstand): %s, totaal %d van %d\n'%(dict(eind),sum(eind.values()),sum(c!='.' for r in g for c in r)))
    f.write('Per stap (incl. tussenstappen die later weer wijzigen): %s\n'%dict(Counter(z for z,*_ in log)))
print(open(f'{RN}/telling.txt').read())
