# r3: reparaties uit de keuring van r2 (r2/keuring/rapport.md, punten 1-10), bovenop r2. Hieronder de r2-beschrijving;
# r3-wijzigingen staan bij de stappen gemarkeerd met 'r3'.
# r2: benoemde reparaties op r1 (opdracht Claude na vergelijking met model/Stantler/maatstaf). Alles uit het model:
# 1 drieslag + volume: per cel de meerderheids-toonklasse van het model (cel-shading -> harde grenzen; celklas.py);
#   binnen de flank de relatieve helderheid van alleen de flankpixels (kaal_flum: <p20 = N, >p85 = H), dus volume
#   alleen waar het model lichter/donkerder is (schouder, bil, onder de kaak, buiklijn). Nieuwe tint H (hooglicht flank).
# 2 hoorns: doorlopende band langs de middellijn van de modelhoorn (hoornskelet.json): 2 px staal (taps naar de punt)
#   + 1 px lijn; lichte strook aan de lichtkant (normaal naar boven/links), donkere reflectie aan de andere kant;
#   witte glinster waar het model op die plek wit is.
# 3 kuif uit de modelzones (toonklassen D/S/M), lijn hoorn/kuif uit de zonegrens; binnenoor uit de modelklassen.
# 4 selout op alle randen die naar boven/links wijzen (donkerste eigen tint), zwart naar rechts/onder.
# 5 strepen 1 px van de buitenlijn af; 6 plukjes uit het model (aandeel zwart in de cel); 7 oogpixels uit r1 bevroren.
import numpy as np, sys, json, math
from collections import Counter
from PIL import Image
RN='r9'
hx=lambda h: tuple(int(h[i:i+2],16) for i in (1,3,5))
PAL={'.':(0,0,0),'0':hx('#1C1A22'),     # r3: vacht ±30 helderheid per stap en neutraler grijs; staal koel blauw + harde witte glans
     'D':hx('#3E434E'),'S':hx('#5B616C'),'M':hx('#787F8A'),'N':hx('#969DA8'),'L':hx('#B5BBC4'),'H':hx('#D5DAE0'),'W':hx('#F5F7F9'),
     '1':hx('#1C2436'),'A':hx('#283040'),'3':hx('#424B5B'),'4':hx('#8D96A6'),'5':hx('#D3D9E3')}   # r5: staal B-R 16-25, diepere reflectie, contrast
ORDER=list(PAL)
Z=np.load('kaal_zone.npy'); H,W=Z.shape
LF=np.load('kaal_lf.npy'); CEL=np.load('kaal_cel.npy'); FL=np.load('kaal_flum.npy'); SF=np.load('kaal_sf.npy'); DK=np.load('kaal_dk.npy')
NLA=np.load('kaal_nla.npy'); LUM=(NLA*[.299,.587,.114]).sum(2)
km=json.load(open('kaal_meta.json'))
ZN={0:'vacht',1:'staal',2:'kuif',3:'oog',4:'neus',5:'lijn'}
flank=(Z==0)&(LF<.5)&np.isin(CEL,[3,4])
P20,P85=np.percentile(FL[flank],[20,85])
g=[['.']*W for _ in range(H)]; zone=[['']*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        if Z[y,x]<0: continue
        z=ZN[Z[y,x]]; zone[y][x]=z
        if LF[y,x]>=0.5 or z=='lijn': g[y][x]='0'; continue
        c=CEL[y,x]
        if z=='staal': g[y][x]='1' if LUM[y,x]<80 else 'D' if LUM[y,x]<115 else '3' if LUM[y,x]<150 else '4' if LUM[y,x]<190 else '5' if LUM[y,x]<225 else 'W'
        elif z=='kuif': g[y][x]='DSMNNN'[c]
        elif z=='neus': g[y][x]='D' if c<=1 else 'N'
        elif c in (3,4) and z=='vacht': g[y][x]='N' if FL[y,x]<P20 else 'H' if FL[y,x]>P85 else 'L'
        else: g[y][x]='DSMNLW'[c]
kaal=[r[:] for r in g]          # "kaal gemapt": basis voor de telling
log=[]
def put(zn,x,y,c,why):
    old=g[y][x]
    if old!=c: g[y][x]=c; log.append((zn,x,y,old,c,why))
# r3: silhouet uit de modeldekking per cel (kaal_alpha) met een strengere drempel op plekken waar 0,45 de modelvorm afvlakt
AL=np.load('kaal_alpha.npy')
for y in range(35,46):                     # punt 5: bolle bilcurve (achterrand bil, rijen 35-45)
    xs=[x for x in range(33,40) if g[y][x]!='.']
    if xs and AL[y,max(xs)]<0.85: put('bilcurve',max(xs),y,'.','bilrand: modeldekking <85% -> buiten (bolle curve uit het model)')
for y in range(22,32):                     # punt 9: plukjes in de manen (modeldekking <75% -> inkeping)
    xs=[x for x in range(17,24) if g[y][x]!='.']
    if xs and AL[y,max(xs)]<0.75: put('manen',max(xs),y,'.','manenrand: modeldekking <75% -> inkeping (plukje uit het model)')
if AL[17,0]>=0.4 and g[17][0]=='.':        # punt 4: spitse oorpunt links (modeldekking 43%)
    zone[17][0]='vacht'; put('oor',0,17,'S','oorpunt uit het model (dekking 43%)')
for y in range(55,59):                     # punt 7: tussenruimte verre achterhoef / nabije voorpoot
    if g[y][25]!='.' and AL[y,25]<0.9: put('hoef',25,y,'.','tussenruimte hoef/voorpoot (modeldekking <90%)')
# r3 punt 4: oren - toon uit de helderheid van het meerderheidssegment in het model (licht buitenvlak, donkere binnenkant)
segm=np.load('seg.npz')['a']; amod=np.asarray(Image.open('../referenties/model_r5.png').convert('RGB')).astype(float); lm=(amod*[.299,.587,.114]).sum(2)
def celseg(i,j):
    xa,xb=int(round(km['x0']+i*km['p'])),int(round(km['x0']+(i+1)*km['p'])); ya,yb=int(round(km['y0']+j*km['p'])),int(round(km['y0']+(j+1)*km['p']))
    return segm[ya:yb,xa:xb],lm[ya:yb,xa:xb]
for (bx0,by0,bx1,by1) in ((0,16,6,22),(16,17,23,21)):
    for y in range(by0,by1+1):
        for x in range(bx0,bx1+1):
            if g[y][x] in '.0' or zone[y][x]!='vacht': continue
            sg,ll=celseg(x,y); ok=sg>=0
            if not ok.any(): continue
            ids,c=np.unique(sg[ok],return_counts=True); k=ids[c.argmax()]
            if k==685 and bx0==0: continue
            l=ll[ok&(sg==k)].mean()
            put('oor',x,y,'S' if l<135 else 'M' if l<165 else 'N' if l<190 else 'L','oortint uit de modelhelderheid van het oorsegment')
# r3 punt 6: staart - tinten uit het staartvlak van het model (grijze bovenkant, witte onderkant/punt)
for y in range(28,35):
    for x in range(33,40):
        if g[y][x] in '.0': continue
        sg,ll=celseg(x,y); m=sg==912
        if m.mean()<0.2: continue
        l=ll[m].mean(); wf=(ll[m]>235).mean()
        put('staart',x,y,'W' if wf>=0.35 else 'S' if l<115 else 'M' if l<150 else 'N' if l<200 else 'L','staarttint uit het model')
def opaque(x,y): return 0<=x<W and 0<=y<H and g[y][x]!='.'
r1=json.load(open('r1/grid.json'))['grid']
OOGPX=[(x,y) for y in range(21,26) for x in range(9,14) if r1[y][x] in '0D']   # eigenlijke oogpixels (lokaal) uit r1
OOG=(8,20,15,26); NEUS=(2,26,6,29)
def inbox(b,x,y): return b[0]<=x<=b[2] and b[1]<=y<=b[3]
# --- bilstrepen weg (zoals r1): cel opnieuw uit het model zonder de streeppixels ---
a=np.asarray(Image.open('../referenties/model_r5.png').convert('RGB')).astype(float)
seg=np.load('seg.npz')['a']; x0,y0,p=km['x0'],km['y0'],km['p']
lumm=(a*[.299,.587,.114]).sum(2)
for y in range(H):
    for x in range(W):
        if g[y][x]!='0': continue
        xa,xb=int(round(x0+x*p)),int(round(x0+(x+1)*p)); ya,yb=int(round(y0+y*p)),int(round(y0+(y+1)*p))
        if not (640<=(xa+xb)/2<=775 and 545<=(ya+yb)/2<=700): continue
        ok=(seg[ya:yb,xa:xb]==685)
        if not ok.any() or any(not opaque(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): continue
        l=lumm[ya:yb,xa:xb][ok]; l=l[(l>=170)&(l<226)]
        t='L' if not len(l) else 'N' if l.mean()<P20 else 'H' if l.mean()>P85 else 'L'
        put('strepen_weg',x,y,t,'bilstreep weg -> flanktint uit het model naast de streep')
# --- plukjes boven de achterhoeven: cellen in de plukvakken met >=45% zwart in het model -> zwart (ook buiten het silhouet) ---
for (bx0,by0,bx1,by1) in ((785,820,845,900),(630,810,690,890)):     # modelvakken: nabije en verre achterpoot
    for y in range(H):
        for x in range(W):
            cx,cy=x0+(x+.5)*p,y0+(y+.5)*p
            if bx0<=cx<=bx1 and by0<=cy<=by1 and DK[y,x]>=0.45:
                if g[y][x]=='.': zone[y][x]='vacht'
                put('plukjes',x,y,'0','plukje uit het model (aandeel zwart in de cel)')
PLUK=set((x,y) for zn,x,y,*_ in log if zn=='plukjes')
# --- ontkorrelen <3 px (vacht/kuif; niet oog/neus/hoorns) ---
def comps():
    seen=set(); res=[]
    for y in range(H):
        for x in range(W):
            if (x,y) in seen or g[y][x] in '.0': continue
            v=g[y][x]; st=[(x,y)]; seen.add((x,y)); cc=[]
            while st:
                cx,cy=st.pop(); cc.append((cx,cy))
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=cx+dx,cy+dy
                    if 0<=nx<W and 0<=ny<H and (nx,ny) not in seen and g[ny][nx]==v: seen.add((nx,ny)); st.append((nx,ny))
            res.append((v,cc))
    return res
for _ in range(3):
    for v,cc in comps():
        if len(cc)>=3 or any(inbox(OOG,x,y) or inbox(NEUS,x,y) or zone[y][x]=='staal' for x,y in cc): continue
        if any(inbox((0,16,6,22),x,y) or inbox((16,17,23,21),x,y) or inbox((33,28,39,34),x,y) for x,y in cc): continue   # r3: oren/staart (modeldetail, niet wegpoetsen)
        nb=Counter(g[y+dy][x+dx] for x,y in cc for dx,dy in((1,0),(-1,0),(0,1),(0,-1))
                   if 0<=x+dx<W and 0<=y+dy<H and g[y+dy][x+dx] not in '.0' and zone[y+dy][x+dx]!='staal' and g[y+dy][x+dx]!=v)
        if nb:
            for x,y in cc: put('ontkorrel',x,y,nb.most_common(1)[0][0],'tintvlakje <3 px naar buurtint')
# --- binnenlijnen ---
def buurzone(x,y):
    c=Counter(zone[y+dy][x+dx] for dx in(-1,0,1) for dy in(-1,0,1) if opaque(x+dx,y+dy) and g[y+dy][x+dx]!='0' and zone[y+dy][x+dx] not in('lijn',''))
    return c.most_common(1)[0][0] if c else 'vacht'
DARK={'vacht':'D','kuif':'1','staal':'1','oog':'0','neus':'0'}
inner=[(x,y) for y in range(H) for x in range(W) if g[y][x]=='0' and not inbox(OOG,x,y) and not inbox(NEUS,x,y) and (x,y) not in PLUK
       and all(opaque(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)))]
for x,y in inner: put('binnenlijn',x,y,DARK[buurzone(x,y)],'binnenlijn in donkerste eigen tint')
# --- r4: hoorns als gladde, taps toelopende streek langs de (extra gladgemaakte) modelmiddellijn ---
# Breedte (incl. 1 px lijn per kant): model-hw per punt, naar boven afgerond: onderste 60% van de hoorn 4 px (2 px staal + lijn),
# daarna taps naar 3 px (1 px staal) en de punt alleen lijn. Pixel hoort bij de hoorn bij >=50% dekking (16x16 subpixels),
# dus geen wiebelende band; rand = hoornpixel met een 4-buur buiten de hoorn.
SK=json.load(open('hoornskelet.json'))
def herbemonster(P,stap=0.2):
    P=np.array(P,float); L=np.r_[0,np.cumsum(np.hypot(*np.diff(P,axis=0).T))]
    s=np.arange(0,L[-1],stap); s=np.r_[s,L[-1]]
    return np.c_[np.interp(s,L,P[:,0]),np.interp(s,L,P[:,1])]
def glad(Q,n,keer):
    Q=Q.copy()
    for _ in range(keer):
        R=Q.copy()
        for k in range(1,len(Q)-1):
            a,b=max(0,k-n),min(len(Q),k+n+1); R[k]=Q[a:b].mean(0)
        Q=R
    return Q
def breedte(s):           # s = 0 voet .. 1 punt ; volle breedte incl. lijn in px
    if s<=0.60: return 4.0
    if s<=0.84: return 4.0-(s-0.60)/0.24*1.0
    return 3.0-(s-0.84)/0.16*1.9
HOORN={}
# r4: punt verlengd tot de gemeten top van het modelhoornvlak (links 8,5/1,2 en lijn 8,0/0,4; rechts 30,4/0,5) -- de verdunning stopte eerder
PUNT={'links':[[8.75,1.3],[8.45,0.75]],'rechts':[[30.35,0.5]]}
SUB=8; off=(np.arange(SUB)+.5)/SUB
for naam in ('links','rechts'):
    PT=SK[naam]['pts']+PUNT[naam]
    Q=glad(herbemonster(PT),5,2)
    A=Q[:-1]; B=Q[1:]; D=B-A; L2=(D**2).sum(1); L2[L2==0]=1e-9
    S=np.r_[0,np.cumsum(np.sqrt(L2))]; S/=S[-1]
    WS=np.array([breedte(s) for s in S])
    xs=np.arange(0,36); ys=np.arange(0,20)
    cov={}
    for y in ys:
        for x in xs:
            px=(x+off[None,:]).repeat(SUB,0).ravel(); py=(y+off[:,None]).repeat(SUB,1).ravel()
            Pp=np.c_[px,py]
            t=np.clip((((Pp[:,None,:]-A[None])*D[None]).sum(2))/L2[None],0,1)
            C=A[None]+t[...,None]*D[None]; d=np.hypot(*(Pp[:,None,:]-C).transpose(2,0,1))
            k=d.argmin(1); w=WS[k]*(1-t[np.arange(len(k)),k])+WS[k+1]*t[np.arange(len(k)),k]
            c=(d[np.arange(len(k)),k]<=w/2).mean()
            if c>0: cov[(x,y)]=c
    HOORN[naam]=(Q,{xy for xy,c in cov.items() if c>=0.5})
def vrij(naam,x,y):
    if not (0<=x<W and 0<=y<H): return False
    return Z[y,x]<0 or Z[y,x] in (1,5) or SF[y,x]>=0.15 or (naam=='rechts' and Z[y,x]!=2)
ALLE=set()
# trapjes regelmatig maken (pixel-art lijnregels: geen heen-en-weer, geleidelijk veranderende staplengtes), per pixel op het masker
TRAP={'rechts':{'weg':[(18,11),(27,13)],'erbij':[(19,15),(25,3),(25,4),(25,5)]},   # r5 (keuring r4 #7): model wijkt op rij 3-5 1 px naar links uit (begin S) -> (25,3-5) erbij; bovenrand 3-5-3-1-1; onderrand 1-2-3-4-2-1
      'links':{'weg':[(4,16)],'erbij':[(5,7),(10,2)]}}                       # buitenbocht 1-2-2 i.p.v. 1-1-3; (10,2): geen 2x2 lijnblokje in de punt
for naam in ('links','rechts'):
    Q,M=HOORN[naam]; M={xy for xy in M if vrij(naam,*xy)}
    for xy in TRAP[naam]['weg']: M.discard(xy); log.append(('hoorntrap',xy[0],xy[1],'masker','uit','trapje regelmatig (pixel-art lijnregel)'))
    for xy in TRAP[naam]['erbij']: M.add(xy); log.append(('hoorntrap',xy[0],xy[1],'masker','in','trapje regelmatig (pixel-art lijnregel)'))
    HOORN[naam]=(Q,M); ALLE|=M
# oude hoornresten weg: alles van de oude hoornreductie (zone staal/lijn boven de kop) buiten de nieuwe hoorns, van de rand naar binnen
for _ in range(6):
    for y in range(H):
        for x in range(W):
            if g[y][x]=='.' or (x,y) in ALLE: continue
            if not any(not opaque(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): continue
            if (Z[y,x] in (1,5) and y<17) or (Z[y,x]==0 and SF[y,x]>0.05 and y<16):
                put('hoorn',x,y,'.','oude hoornrest buiten de nieuwe hoorn weg')
GLIM={}
# kleuren: rand = lijn (wordt hieronder selout 'A' aan de lichtkant, zwart aan de schaduwkant); binnen: lichtkant glans, andere kant reflectie
for naam in ('links','rechts'):
    Q,M=HOORN[naam]
    for (x,y) in M:
        zone[y][x]='staal'
        rand=any((x+dx,y+dy) not in M for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
        if rand: put('hoorn',x,y,'0','hoornrand: lijn'); continue
        d=np.hypot(Q[:,0]-(x+.5),Q[:,1]-(y+.5)); k=int(d.argmin()); k2=min(k+3,len(Q)-1); k1=max(k-3,0)
        dx,dy=Q[k2]-Q[k1]; nx_,ny_=dy,-dx       # lichtkant = links van de looprichting voet->punt (= buitenbocht/bovenkant, licht linksboven)
        nn=math.hypot(nx_,ny_) or 1; nx_,ny_=nx_/nn,ny_/nn
        def diepte(sx,sy):     # aantal binnenpixels tussen deze pixel en de rand in richting (sx,sy)
            seen={(x,y)}; n=0
            for st in range(1,12):
                q=(int(math.floor(x+.5+sx*st*.35)),int(math.floor(y+.5+sy*st*.35)))
                if q in seen: continue
                seen.add(q)
                if q not in M or any((q[0]+a,q[1]+b) not in M for a,b in((1,0),(-1,0),(0,1),(0,-1))): return n
                n+=1
            return n
        dl,dd=diepte(nx_,ny_),diepte(-nx_,-ny_)
        c='5' if dl==0 else '3' if dd==0 else '4'
        xa,xb=int(round(x0+x*p)),int(round(x0+(x+1)*p)); ya,yb=int(round(y0+y*p)),int(round(y0+(y+1)*p))
        hm=np.isin(seg[ya:yb,xa:xb],[14,49]); glim=hm.any() and (lumm[ya:yb,xa:xb][hm]>235).mean()>0.30
        GLIM[(x,y)]=glim
        put('hoorn',x,y,c,'hoorn binnen: lichtkant 5 (glans), schaduwkant 3 (reflectie), midden 4')

# --- buitenlijn + selout (randen die naar boven/links wijzen) ---
for y in range(H):
    for x in range(W):
        if g[y][x]=='.' or (x,y) in OOGPX: continue
        if any(not opaque(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) and g[y][x]!='0':
            put('lijn',x,y,'0','buitenlijn dicht')
SELV={'kuif':'1','staal':'A'}
for y in range(H):
    for x in range(W):
        if g[y][x]!='0' or (x,y) in PLUK or inbox(NEUS,x,y): continue
        if all(opaque(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): continue
        tv=[(dx,dy) for dx in range(-2,3) for dy in range(-2,3) if (dx or dy) and not opaque(x+dx,y+dy)]
        nx_=sum(d[0] for d in tv); ny_=sum(d[1] for d in tv); nn=(nx_**2+ny_**2)**.5 or 1
        if (nx_+ny_)/nn > -0.25: continue                       # wijst naar rechts/onder -> zwart
        if not any(opaque(x+dx,y+dy) and g[y+dy][x+dx]!='0' for dx,dy in((1,0),(0,1),(1,1),(-1,0),(0,-1))) and zone[y][x]!='staal': continue
        z=zone[y][x] if zone[y][x] in ('staal','vacht','kuif') else buurzone(x,y)
        if z=='kuif': continue      # donkere manen/kuif: lijn blijft zwart (selout '1' zou om en om met zwart staan)
        put('lijn',x,y,SELV.get(z,'D'),'selout lichtkant (donkerste eigen tint)')
# --- r3 punt 8: voorkant kop (lokaal x2-6, y20-26) en de oorpunt links (x0-1, y16-18) is lichtkant: buitenlijn daar selout D, zwart alleen onder neus/kin ---
for y in list(range(16,19))+list(range(20,27)):
    for x in (range(0,2) if y<19 else range(2,7)):
        if g[y][x]=='0' and not opaque(x-1,y) and (x,y) not in OOGPX: put('lijn',x,y,'D','selout voorkant kop (lichtkant)')
# --- zwarte pixels die na de hoornband binnen het silhouet liggen (geen transparante 8-buur) -> binnenlijn, donkerste eigen tint ---
for y in range(H):
    for x in range(W):
        if g[y][x]!='0' or (x,y) in PLUK or inbox(NEUS,x,y) or inbox(OOG,x,y): continue
        vier=all(opaque(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
        los=not any(g[y+dy][x+dx]=='0' for dx in(-1,0,1) for dy in(-1,0,1) if (dx or dy) and opaque(x+dx,y+dy))
        if all(opaque(x+dx,y+dy) for dx in(-1,0,1) for dy in(-1,0,1)) or (vier and los):
            z=zone[y][x] if zone[y][x] in ('staal','vacht','kuif') else buurzone(x,y)
            put('binnenlijn',x,y,{'staal':'1','kuif':'1'}.get(z,'D'),'binnenlijn (na hoornband) in donkerste eigen tint')
# --- Jordi's strepen (bovenlaag, 1 px van de buitenlijn af) en het r1-oog ---
def rand_x(y):   # buitenste zwarte lijnpixel rechts in rij y (lijf)
    xs=[x for x in range(W) if g[y][x]=='0' and not opaque(x+1,y)]
    return max(xs) if xs else None
extra=[]
for y in range(36,43):
    rx=rand_x(y)
    if rx: extra.append(('streep_dij',rx-2,y))
json.dump(extra,open(f'extra_{RN}.json','w'))
for zn,x,y in extra: put(zn,x,y,'0','Jordi: zwarte streep langs de achterrand van de dij (1 px van de lijn af, volgt de bilcurve)')
for zn,x,y in extra:
    if g[y][x+1] in 'LH': put('dijschaduw',x+1,y,'N','pixel tussen dijstreep en buitenlijn -> schaduwtint dij (keuring punt 5)')
for x,y in OOGPX: put('oog',x,y,r1[y][x],'oogpixel uit r1 (bevroren)')
# staartstreep: middellijn van de staart, alleen pixels die niet aan een lijn of de rand raken
STAART=[(36,31),(36,32)]
for x,y in STAART:
    assert all(opaque(x+dx,y+dy) and (g[y+dy][x+dx]!='0' or (x+dx,y+dy) in STAART) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))), (x,y)
for x,y in STAART:
    put('streep_staart',x,y,'0','Jordi: zwarte streep midden in de staart (raakt de buitenlijn niet)')
extra+= [('streep_staart',x,y) for x,y in STAART]
json.dump(extra,open(f'extra_{RN}.json','w'))
# --- r4 nawerk (per pixel, naar het model) ---
# kuif (keuring Claude punt 3): binnentint per cel uit de modelhelderheid van alleen het kuifvlak (seg 446):
#   >=150 N, 120-150 M, 95-120 S, <95 D -> lichte plukken linksboven, donkere strengen rechtsonder zoals in het model
for y in range(12,20):
    for x in range(6,13):
        if zone[y][x]!='kuif' and not (x,y)==(11,18): continue
        if g[y][x] in '.01A' : continue
        xa,xb=int(round(x0+x*p)),int(round(x0+(x+1)*p)); ya,yb=int(round(y0+y*p)),int(round(y0+(y+1)*p))
        k=seg[ya:yb,xa:xb]==446
        if k.mean()<0.3: continue
        l=lumm[ya:yb,xa:xb][k].mean()
        put('kuif',x,y,'N' if l>=150 else 'M' if l>=120 else 'S' if l>=95 else 'D','kuiftint uit de modelhelderheid van het kuifvlak')
# kuifrand boven (lichtkant, grenst aan transparant): selout D zoals de rest van de vacht; zwart blijft rechts/onder
for x,y in ((8,14),(9,13),(10,12),(11,12),(12,13),(13,13)):
    if g[y][x]=='0' and not opaque(x,y-1): put('lijn',x,y,'D','selout bovenrand kuif (lichtkant)')

put('lijn',2,14,'A','selout lichtkant hoorn doorlopend (niet om en om met zwart)')
put('lijn',9,1,'0','punt linkerhoorn: schaduwkant (rechts) zwart')
put('hoorn',3,10,'5','lichte strook in de bocht doorlopend (buurpixel van de lichtkantlijn)')
put('kuif',11,13,'D','zwarte pixel binnen de kuifbovenkant (plukscheiding in het model, helderheid 57) -> binnenlijn in donkerste eigen tint D')
put('kuif',10,16,'S','donkere plukstreng doorlopend (model 133, grens M/S; plukscheiding in het model)')
put('lijn',7,14,'0','gaatje tussen hoorn en kuif dicht: model is daar lijn (helderheid 85)')
put('kuif',11,18,'D','losse staalpixel (oude hoornreductie) in de kuif -> kuiftint uit het model (helderheid 85)')
put('oor',5,17,'D','losse zwarte pixel (sprite 15,18) -> oorlijn uit het model (helderheid 77, lijn+hoornvoet), zelfde tint als de oorlijn links')
# glans: harde witte strook op de lichtkant waar het model op de hoorn wit glanst; alleen aaneengesloten (>=2 px) stukken
kand=[(x,y) for (x,y),v in GLIM.items() if v and g[y][x]=='5']
ks=set(kand)
for x,y in kand:
    if any((x+dx,y+dy) in ks for dx in(-1,0,1) for dy in(-1,0,1) if dx or dy): put('glans',x,y,'W','witte glans uit het model (lichtkant, aaneengesloten)')
# --- r5: reparaties keuring r4 (sprite/r4/keuring/rapport.md), lokale coordinaten (64x64 = +10,+1) ---
# punt 2: binnenlijnen (vorm over vorm) bij de hoornvoeten -> donkerste staaltint A (zwart alleen op de buitenrand)
for x,y in ((6,14),(6,15),(7,15),(6,16),(6,17),(6,18),(12,16),(12,17),(12,18),(12,19),(13,14),(13,15),(13,19),(14,19),(15,17),(15,18),(16,16),(16,17),(17,17)):
    if g[y][x] in '01' and all(opaque(x+dx,y+dy) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): put('binnenlijn',x,y,'A','keuring r4 #2: binnenlijn hoornvoet -> donkerste staaltint A')
# punt 3: staart in twee toonzones uit het model (staartvlak seg 912: links 101-124 midden, rechts 150-182 licht, witte franje rechtsonder)
for (x,y),c in {(37,30):'L',(37,31):'L',(37,32):'L',(37,33):'W',(34,32):'M',(35,32):'M',(35,33):'M',(36,33):'M',(36,34):'M'}.items():
    put('staart',x,y,c,'keuring r4 #3: staarttoonzone uit het model (midden links, licht rechts, witte franje rechtsonder)')
# punt 4: lichte band H op de flank -> flanktint L (model 200-208 egaal); schouderpunt van de rugband taps N (model 157-184)
for y in range(35,42):
    for x in range(18,22):
        if g[y][x]=='H': put('flank',x,y,'L','keuring r4 #4: banding weg, flanktint uit het model')
for x,y in ((18,35),(18,36),(19,36)): put('flank',x,y,'N','keuring r4 #4: tapse schouderpunt van de rugband (model 157-184)')
# punt 5: ruis kuif -> donker S/D met de ene lichte streng N (modelrij 16); oor: lichte rand L, binnenvlak M, geen losse N
for y in range(12,21):
    for x in range(6,13):
        if zone[y][x]=='kuif' and g[y][x]=='M': put('kuif',x,y,'S','keuring r4 #5: kuif donker (S/D) met een lichte streng N')
for (x,y),c in {(5,18):'M',(18,18):'M',(17,19):'L',(20,19):'L',(18,21):'M',(22,18):'L'}.items():
    put('oor',x,y,c,'keuring r4 #5: losse oorpixel naar de toonzone ernaast (rand L / binnenvlak M)')
# punt 6: zwart binnen de poten -> D (middentoon/pluklijn in het model)
for x,y in ((29,53),(30,53),(41,54),(40,56),(38,58)):
    if g[y][x]=='0': put('poot',x,y,'D','keuring r4 #6: zwart binnen de poot -> D')
# --- r6: manen op de achterkant van de hals (Jordi: "loopt de kuif/maan genoeg door op de hals?"), per cel uit het model ---
# Gemeten per cel (lokaal): maanvlak = modelpixels 60-128 helderheid (maan 85-125), lijn = <60, achtergrond.
# maan (>=50% maanvlak) -> S (model 86-101), lichtere streng M (model 98-110, middenrechts zoals in het model);
# linkerlijn maan/hals (zwarte modellijn, binnenlijn) -> D; buitenrand: lijn waar de modellijn >=40-50% van de cel is (plukpunten).
MAAN={ (16,24):'D',(17,24):'S',(18,24):'S',
       (16,25):'D',(17,25):'S',(18,25):'M',
       (16,26):'D',(17,26):'S',(18,26):'M',(19,26):'0',
       (17,27):'D',(18,27):'M',
       (17,28):'D',(18,28):'S',(19,28):'M',(20,28):'0',
       (18,29):'D',(19,29):'S',(20,29):'0',
       (18,30):'D',(19,30):'S',(20,30):'S',(22,30):'0',
       (18,31):'D',(19,31):'S',(20,31):'S',(21,31):'S',(22,31):'S',(23,31):'0'}
for (x,y),c in MAAN.items(): put('manen',x,y,c,'r6 manen uit het model (vlak/streng/lijn/plukpunt)')
# --- r7: rechte lijnen alleen waar het model golft (Jordi 26 nov), gemeten op de modelcontour (1024 px, rij-/kolommidden) ---
# lokale coordinaten (64x64 = +10,+1); metingen in r7/log.txt
R7={ (11,49):'.',   # poot voor-ver: linkerrand 21|22|21|22-zigzag; model 21,7/21,6/21,5 (rij 49-51) -> rand op x22 (rij 49-53 in 64x64)
     (12,49):'D',   #   nieuwe randpixel links = selout (lichtkant)
     (30,55):'.',   # poot achter-ver: model rechterrand 39,6 (rij 56) -> pixel 40 heeft 10% dekking
     (29,31):'D',(30,31):'D',(31,31):'D',   # rug: bult in het model (rand 32,7-32,8 bij x39-41 tegen 33,2-33,3 ernaast) -> rugrand 1 px omhoog
     (29,32):'S',(30,32):'S',(31,32):'S',   #   oude randpixels -> bandtint eronder
     (21,34):'L',(22,34):'L',(23,34):'L'}   # rugband onderrand: model zakt hier naar 35,6 (x31-33) tegen 36,1-36,2 ernaast -> grens 1 px omhoog
for (x,y),c in R7.items(): put('r7',x,y,c,'r7: contour op de gemeten modelcurve (golf)')
# --- r8: golven uit het model zichtbaar maken (Jordi 26 nov; regel coordinator r8) ---
# Elke rechte silhouetrun >= 4 px (niet hoorns, niet oogzone): modelrand (rand voorgrondvlak op 1024 px, gemeten op het rij-/kolommidden
# van elke runpixel) t.o.v. de rechte lijn door de eindpunten. Afwijking >= 0,2 px: op het hoogste punt 1 px stap in die richting
# (bolling = 1 px naar buiten, deuk = 1 px naar binnen) over het stuk waar de afwijking >= max(0,2; helft van de piek) is, minstens 2 px,
# eindpixels van de run blijven staan. Vlakken schuiven mee (lijnkleur gaat mee naar de nieuwe rand, oude rand krijgt de tint erbinnen).
FG8=~((np.load('witlab.npz')['a']==-2)|(np.load('witlab.npz')['a']==1))
def rand8(x,y,dx,dy):
    # positie van de modelrand langs de normaal (dx,dy) door het midden van pixel (x,y), in px t.o.v. de buitengrens van die pixel (+ = naar buiten)
    cx,cy=x+.5,y+.5; best=None
    for k in range(-60,61):
        t=k/30.0; X=x0+(cx+dx*t)*p; Y=y0+(cy+dy*t)*p; X2=x0+(cx+dx*(t+1/30))*p; Y2=y0+(cy+dy*(t+1/30))*p
        if not (0<=int(X2)<1024 and 0<=int(Y2)<1024 and 0<=int(X)<1024 and 0<=int(Y)<1024): continue
        if FG8[int(Y),int(X)] and not FG8[int(Y2),int(X2)]:
            pos=t+1/60-0.5
            if best is None or abs(pos)<abs(best): best=pos
    return best
STAAL8=set('345AW')
def is_hoorn(x,y): return y<=17 and (zone[y][x]=='staal')
OOG8=(8,20,15,26)
RUNS8=[]
for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
    vert = dx!=0
    for a in range(W if vert else H):
        b=0; L=H if vert else W
        while b<L:
            x,y=(a,b) if vert else (b,a)
            if opaque(x,y) and not opaque(x+dx,y+dy):
                c=b
                while c+1<L:
                    xx,yy=(a,c+1) if vert else (c+1,a)
                    if opaque(xx,yy) and not opaque(xx+dx,yy+dy): c+=1
                    else: break
                if c-b+1>=4: RUNS8.append((dx,dy,a,b,c))
                b=c+1
            else: b+=1
plan8={}; log8=[]
for dx,dy,a,b,c in RUNS8:
    cells=[(a,t) if dx else (t,a) for t in range(b,c+1)]
    naam=f"{'V' if dx else 'H'}{'+' if dx+dy>0 else '-'} {'x' if dx else 'y'}={a+(10 if dx else 1)} {b+(1 if dx else 10)}-{c+(1 if dx else 10)} ({c-b+1} px)"
    if any(is_hoorn(x,y) or inbox(OOG8,x,y) for x,y in cells): log8.append(naam+': hoorn/oog, overgeslagen'); continue
    if dy==1 and a>=58: log8.append(naam+': hoefzool (grondlijn), overgeslagen'); continue
    if all(x+10<=27 and 30<=y+1<=46 for x,y in cells): log8.append(naam+': witte borst links (Jordi: was al goed), overgeslagen'); continue
    e=[rand8(x,y,dx,dy) for x,y in cells]
    while len(cells)>=4 and e and e[0] is None: cells=cells[1:]; e=e[1:]          # eindpixel zonder modelrand (bv. oorpunt) eraf
    while len(cells)>=4 and e and e[-1] is None: cells=cells[:-1]; e=e[:-1]
    if len(cells)<4: log8.append(naam+': na inkorten < 4 px, overgeslagen'); continue
    if any(v is None for v in e): log8.append(naam+': modelrand niet overal gevonden, overgeslagen'); continue
    n=len(e); ch=[e[0]+(e[-1]-e[0])*i/(n-1) for i in range(n)]; dev=[e[i]-ch[i] for i in range(n)]
    mx,mn=max(dev[1:-1]),min(dev[1:-1])
    s='%s: model %s, afwijking +%.2f/%.2f'%(naam,' '.join('%.2f'%v for v in e),mx,mn)
    if max(mx,-mn)<0.2: log8.append(s+' -> recht laten'); continue
    sg=1 if mx>=-mn else -1; pk=max(range(1,n-1),key=lambda i: sg*dev[i]); th=max(0.2,0.5*sg*dev[pk])
    S=[pk]; i=pk
    while i-1>=1 and sg*dev[i-1]>=th: i-=1; S.insert(0,i)
    i=pk
    while i+1<=n-2 and sg*dev[i+1]>=th: i+=1; S.append(i)
    if len(S)<2:
        cand=[j for j in (pk-1,pk+1) if 1<=j<=n-2]
        if cand: S.append(max(cand,key=lambda j: sg*dev[j])); S.sort()
    for i in S: plan8.setdefault(cells[i],[]).append((sg,dx,dy,naam))
    log8.append(s+' -> %s 1 px op %s'%('bolling: naar buiten' if sg>0 else 'deuk: naar binnen',', '.join('(%d,%d)'%(cells[i][0]+10,cells[i][1]+1) for i in S)))
for (x,y),acts in plan8.items():
    if len(acts)>1: log8.append('(%d,%d): meerdere runs (hoek), overgeslagen'%(x+10,y+1)); continue
    sg,dx,dy,naam=acts[0]; lijn=g[y][x]
    if sg>0:
        ox,oy=x+dx,y+dy
        if not (0<=ox<W and 0<=oy<H) or opaque(ox,oy): continue
        binnen=g[y-dy][x-dx] if opaque(x-dx,y-dy) else lijn
        if lijn=='0' and binnen=='0': binnen='0'   # hoef: massief zwart blijft zwart
        elif binnen in '0A1': binnen=Counter(g[y+j][x+i] for i in(-1,0,1) for j in(-1,0,1) if opaque(x+i,y+j) and g[y+j][x+i] not in '0A1D').most_common(1)[0][0]
        zone[oy][ox]=zone[y][x]; put('r8',ox,oy,lijn,'r8 bolling uit het model: rand 1 px naar buiten'); put('r8',x,y,binnen,'r8: oude rand -> tint van het vlak erbinnen')
    else:
        ix,iy=x-dx,y-dy
        if not opaque(ix,iy) or not opaque(ix-dx,iy-dy) or not opaque(ix-2*dx,iy-2*dy): log8.append('(%d,%d): te smal voor een deuk, overgeslagen'%(x+10,y+1)); continue
        put('r8',x,y,'.','r8 deuk uit het model: rand 1 px naar binnen'); put('r8',ix,iy,lijn,'r8: nieuwe rand krijgt de lijnkleur')
json.dump(log8,open('r9/runs8.json','w'),indent=0)
# --- r9: binnenkant (Jordi 26 nov: "pak de binnenkant ook aan, links bij het witte stuk vacht was al goed") ---
# Zelfde regel als r8, nu op tintgrenzen binnen het silhouet. Modeltoongrens per pixel: helderheidsprofiel van het model (1024 px,
# 5x5 gemiddeld, zwarte lijnpixels <60 eruit) langs de normaal door het pixelmidden; grens = waar het profiel de helft tussen de
# modelhelderheid van beide spritecellen kruist (dichtst bij de pixelgrens). Afwijking t.o.v. de koorde >= 0,2 px -> 1 px stap.
# Niet: buitenrand (pixels met transparante 4-buur), lijntinten 0/A/1, hoorns, oogzone, strepen, witte borst/buik links (64x64 x<=27, y30-46).
LM9=lumm; LMm=np.where(LM9<60,np.nan,LM9)
def celmean9(x,y):
    xa,xb=int(round(x0+x*p)),int(round(x0+(x+1)*p)); ya,yb=int(round(y0+y*p)),int(round(y0+(y+1)*p))
    v=LMm[ya:yb,xa:xb]; return float(np.nanmean(v)) if np.isfinite(v).any() else None
def prof9(x,y,dx,dy,thr):
    ts=np.arange(-1.0,2.01,1/15); vals=[]
    for t in ts:
        X=int(x0+(x+.5+dx*t)*p); Y=int(y0+(y+.5+dy*t)*p)
        v=LMm[max(0,Y-2):Y+3,max(0,X-2):X+3]; vals.append(np.nanmean(v) if np.isfinite(v).any() else np.nan)
    vals=np.array(vals); ok=np.isfinite(vals)
    if ok.sum()<10: return None
    vals=np.interp(ts,ts[ok],vals[ok]); s=np.sign(vals-thr); cr=[(ts[i]+ts[i+1])/2 for i in range(len(ts)-1) if s[i]!=s[i+1] and s[i]!=0]
    if not cr: return None
    c=min(cr,key=lambda t: abs(t-0.5)); return c-0.5 if abs(c-0.5)<=1.2 else None
LIJN9=set('0A1')
EXTRA9=set((x,y) for zn,x,y in extra)
def mag9(x,y):
    return (0<=x<W and 0<=y<H and opaque(x,y) and g[y][x] not in LIJN9 and zone[y][x]!='staal' and not inbox(OOG8,x,y)
            and (x,y) not in EXTRA9 and not (x+10<=27 and 30<=y+1<=46) and all(opaque(x+i,y+j) for i,j in((1,0),(-1,0),(0,1),(0,-1))))
plan9={}; log9=[]
for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
    vert=dx!=0
    for a_ in range(W if vert else H):
        b=0; L=H if vert else W
        while b<L:
            x,y=(a_,b) if vert else (b,a_)
            def grens(x,y,T=None):
                return mag9(x,y) and mag9(x+dx,y+dy) and g[y][x]!=g[y+dy][x+dx] and (T is None or g[y][x]==T)
            if grens(x,y):
                T=g[y][x]; c=b
                while c+1<L:
                    xx,yy=(a_,c+1) if vert else (c+1,a_)
                    if grens(xx,yy,T): c+=1
                    else: break
                if c-b+1>=4:
                    cells=[(a_,t) if vert else (t,a_) for t in range(b,c+1)]
                    naam=f"{T}|{'rechts' if dx>0 else 'links' if dx<0 else 'onder' if dy>0 else 'boven'} {'x' if vert else 'y'}={a_+(10 if vert else 1)} {b+(1 if vert else 10)}-{c+(1 if vert else 10)} ({c-b+1} px)"
                    e=[]
                    for x_,y_ in cells:
                        m1,m2=celmean9(x_,y_),celmean9(x_+dx,y_+dy)
                        e.append(None if m1 is None or m2 is None or abs(m1-m2)<8 else prof9(x_,y_,dx,dy,(m1+m2)/2))
                    while len(cells)>=4 and e[0] is None: cells=cells[1:]; e=e[1:]
                    while len(cells)>=4 and e[-1] is None: cells=cells[:-1]; e=e[:-1]
                    if len(cells)<4 or any(v is None for v in e): log9.append(naam+': geen doorlopende modeltoongrens, recht laten')
                    else:
                        n=len(e); dev=[e[i]-(e[0]+(e[-1]-e[0])*i/(n-1)) for i in range(n)]; mx,mn=max(dev[1:-1]),min(dev[1:-1])
                        s_='%s: model %s, afwijking +%.2f/%.2f'%(naam,' '.join('%.2f'%v for v in e),mx,mn)
                        if max(mx,-mn)<0.2: log9.append(s_+' -> recht laten')
                        else:
                            sg=1 if mx>=-mn else -1; pk=max(range(1,n-1),key=lambda i: sg*dev[i]); th=max(0.2,0.5*sg*dev[pk]); S=[pk]; i=pk
                            while i-1>=1 and sg*dev[i-1]>=th: i-=1; S.insert(0,i)
                            i=pk
                            while i+1<=n-2 and sg*dev[i+1]>=th: i+=1; S.append(i)
                            if len(S)<2:
                                cand=[j for j in (pk-1,pk+1) if 1<=j<=n-2]
                                if cand: S.append(max(cand,key=lambda j: sg*dev[j])); S.sort()
                            for i in S:
                                x_,y_=cells[i]
                                tgt=(x_+dx,y_+dy,T) if sg>0 else (x_,y_,g[y_+dy][x_+dx])
                                plan9.setdefault((tgt[0],tgt[1]),[]).append((tgt[2],naam))
                            log9.append(s_+' -> %s op %s'%('grens 1 px naar de buurtint (vlak '+T+' groeit)' if sg>0 else 'grens 1 px terug (buurtint groeit)',', '.join('(%d,%d)'%(cells[i][0]+10,cells[i][1]+1) for i in S)))
                b=c+1
            else: b+=1
def clusters9(x,y):
    v=g[y][x]; seen={(x,y)}; st=[(x,y)]
    while st and len(seen)<3:
        cx,cy=st.pop()
        for i,j in((1,0),(-1,0),(0,1),(0,-1)):
            q=(cx+i,cy+j)
            if q not in seen and 0<=q[0]<W and 0<=q[1]<H and g[q[1]][q[0]]==v: seen.add(q); st.append(q)
    return len(seen)
for (x,y),acts in plan9.items():
    if len({c for c,_ in acts})>1: log9.append('(%d,%d): tegenstrijdige runs, overgeslagen'%(x+10,y+1)); continue
    c=acts[0][0]; oud=g[y][x]
    if oud==c: continue
    g[y][x]=c
    buren=[(x+i,y+j) for i,j in((1,0),(-1,0),(0,1),(0,-1)) if 0<=x+i<W and 0<=y+j<H and g[y+j][x+i]==oud]
    if clusters9(x,y)<3 or any(clusters9(*q)<3 for q in buren):
        g[y][x]=oud; log9.append('(%d,%d) %s->%s: zou een vlakje <3 px geven, niet gedaan'%(x+10,y+1,oud,c)); continue
    g[y][x]=oud; put('r9',x,y,c,'r9 tintgrens op de gemeten modeltoongrens ('+acts[0][1]+')')
json.dump(log9,open('r9/runs.json','w'),indent=0)
OX=(64-W)//2; OY=64-H
pal=[]
for k in ORDER: pal+=PAL[k]
pal+=[0,0,0]*(16-len(ORDER))
def save(G,fn):
    img=np.zeros((64,64),'uint8')
    for y in range(H):
        for x in range(W): img[OY+y,OX+x]=ORDER.index(G[y][x])
    im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(fn,transparency=0)
import os; os.makedirs(RN,exist_ok=True)
save(g,f'{RN}/impala_{RN}.png'); save(kaal,f'{RN}/kaal_gemapt.png')
Image.open(f'{RN}/impala_{RN}.png').convert('RGBA').resize((512,512),Image.NEAREST).save(f'{RN}/impala_{RN}_8x.png')
json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g],'kaal':[''.join(r) for r in kaal]},open(f'{RN}/grid.json','w'),indent=0)
with open(f'{RN}/wijzigingen.txt','w') as f:
    for e in log: f.write('%s (%d,%d) %s->%s  %s\n'%e)
print(RN,dict(Counter(z for z,*_ in log)),'kleuren',len(set(c for r in g for c in r))-1,'+ transparant; P20/P85 flank',round(P20,1),round(P85,1))
print('\n'.join('%2d '%j+''.join(r) for j,r in enumerate(g)))
