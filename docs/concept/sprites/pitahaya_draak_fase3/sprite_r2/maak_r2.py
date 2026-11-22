# Pitahaya-draak fase 3, r1: kale reductie (half.py) -> lijnen uit het modelskelet -> technische opschoning.
# Model = overnemen, nooit hertekenen: elke stap is een regel op modelmetingen; elke gewijzigde pixel staat in het logbestand.
# Gebruik: python3 maak_r1.py KAAL.png NATIEF.png UIT.png [--toon] [--lmin 15]
import sys,numpy as np; from PIL import Image; from collections import Counter
from groepen import laad; from lijnen import projecteer
KAAL,NAT,UIT=sys.argv[1:4]
def arg(k,d,t=float): return t(sys.argv[sys.argv.index(k)+1]) if k in sys.argv else d
MONDZONE=lambda y,x: 1<=x<=15 and 25<=y<=34
ZMIN=arg('--zmin',30,int); LT=arg('--lt',.4); PL=arg('--pl',95.); RKOP=arg('--rkop',15,int)
LMIN=arg('--lmin',15,int); RMIN=arg('--rmin',25,int); RSP=arg("--rsp",5,int)
K=Image.open(KAAL); kaal=np.asarray(K).astype(int); pal=K.getpalette()
info=np.load(KAAL[:-4]+'_info.npz'); geo=info['geo']; F={k:info['f%d'%k] for k in (0,1,2,4,6,7,8)}
S,OX,OY,bx0,by0=geo[:5]; ymin,xmin,Y0,X0,U=[int(v) for v in geo[5:]]
a,lum,g=laad(NAT); H,W=g.shape
P=np.array(pal[:3*16]).reshape(16,3); L=P@[0.299,0.587,0.114]
GRP={1:'zwart',2:'roze',3:'roze',4:'roze',5:'roze',6:'groen',7:'groen',8:'groen',9:'groen',10:'wit',11:'wit',12:'geel',13:'geel',14:'geel',15:'pit'}
TON={'roze':[2,3,4,5],'groen':[6,7,8,9],'wit':[10,11],'geel':[12,13,14]}
GN={2:'roze',4:'groen',6:'wit',8:'geel'}
o=kaal.copy(); log=[]
def zet(y,x,v,stap):
    if o[y,x]!=v: log.append((stap,x,y,o[y,x],v)); o[y,x]=v
def venster(Y,X):
    j=Y-Y0+ymin; i=X-X0+xmin
    y0=by0-S+OY+S*j; x0=bx0-S+OX+S*i
    return slice(max(int(round(y0)),0),int(round(y0+S))),slice(max(int(round(x0)),0),int(round(x0+S)))
def n2s(nx,ny):   # natieve coordinaat -> spritepixel
    return int(np.floor((nx-(bx0-S+OX))/S))-xmin+X0, int(np.floor((ny-(by0-S+OY))/S))-ymin+Y0
def vlaktint(Y,X,groep=None,zonder_donker=False):
    sl=venster(Y,X); gb=g[sl]; cnt={k:(gb==k).sum() for k in (2,4,6,8)}
    k=groep if groep else max(cnt,key=cnt.get)
    if cnt[k]==0: return None
    c=a[sl][gb==k].mean(0); t=TON[GN[k]][1:] if zonder_donker and k in (2,4) else TON[GN[k]]
    return t[int(((P[t]-c)**2).sum(1).argmin())]
def rand4(m):
    p=np.pad(m,1); return m&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
R0=rand4(kaal>0)
OOG=lambda y,x: 9<=x<=13 and 21<=y<=24
# ---- T: binnenvulling roze en groen uit de gladde modelhelderheid (toonkaart, sigma 1,5 spritepx), drempels uit de eigen
#      toonverdeling (fase 1/2-recept; volume blijft, ribvlekjes verdwijnen; de ribben komen als lijnen terug in stap L)
def gauss(x,s):
    r=int(3*s)+1; k=np.exp(-0.5*(np.arange(-r,r+1)/s)**2); k/=k.sum()
    y=np.apply_along_axis(lambda v: np.convolve(v,k,'same'),0,x); return np.apply_along_axis(lambda v: np.convolve(v,k,'same'),1,y)
for k,naam in ((2,'roze'),(4,'groen')):
    licht=(g==k)&(lum>=(62 if k==2 else 72))           # zonder de donkere naad-/ribpixels
    TK=gauss(lum*licht,1.5*S)/np.maximum(gauss(licht.astype(float),1.5*S),1e-6)
    vals=[]; pos=[]
    for y,x in zip(*np.where((kaal>0)&~R0)):
        if GRP.get(kaal[y,x])!=naam or OOG(y,x): continue
        sl=venster(y,x)
        if (g[sl]==k).sum()<0.4*g[sl].size: continue
        vals.append(TK[sl].mean()); pos.append((y,x))
    vals=np.array(vals); q=np.percentile(vals,[50,90] if k==4 else [40,PL])   # r2: groen 50/40/10, roze 40/50/10 (verdeling teju-sprite: hooglicht klein)
    t=TON[naam]
    for v,(y,x) in zip(vals,pos): zet(y,x,t[1] if v<q[0] else (t[2] if v<q[1] else t[3]),'T')
# ---- L: lijnen uit het skelet van alle donkere modellijnen (zwart, donkergroen lum<72, donkerroze lum<62), componenten >= LMIN
D=(g==1)|((g==4)&(lum<72))|((g==2)&(lum<62))
cnt,ln,sk=projecteer(g,geo,D)
# r2: zwart telt alleen als de natieve zwarte component groot is (>= ZMIN px: echte structuurlijn tussen ledematen en romp,
#     kaak/bek); kleinere zwarte stukjes (schubranden, ribben) worden een donkere vlaktint.
from lijnen import componenten as _comp
labZ,sizeZ=_comp(g==1)
zw=np.zeros((64,64),int); dn=np.zeros((64,64),int)
for ny,nx in zip(*np.where(sk)):
    X,Y=n2s(nx+.5,ny+.5)
    if 0<=X<64 and 0<=Y<64:
        dn[Y,X]+=1
        if g[ny,nx]==1:
            sz=sizeZ[labZ[ny,nx]]
            kop=X<=21 and Y<=34 and GRP.get(kaal[Y,X])=='roze'
            if (not kop and sz>=ZMIN) or (kop and MONDZONE(Y,X) and sz>=15): zw[Y,X]+=1
LIJN=np.zeros((64,64),int)
for y,x in zip(*np.where((((cnt>=2)&(ln>=LMIN))|((cnt>=1)&(ln>=RMIN)))&(kaal>0)&~R0)):
    gr=GRP[o[y,x]]
    if gr in ('geel','wit','pit') or OOG(y,x): continue
    kop=x<=21 and y<=34
    if zw[y,x]*2>=dn[y,x] and zw[y,x]>0: LIJN[y,x]=1                # echte zwarte modellijn
    elif kop and gr=='roze':
        if ln[y,x]>=RKOP: LIJN[y,x]=2                               # kop: alleen lange naden (grote schubflappen), donkerroze
    elif ln[y,x]>=RMIN: LIJN[y,x]=2 if gr=='roze' else 6           # donkergroene rib / donkerroze naad (alleen lange modellijnen)
# fragmenten: zwarte lijnstukjes < 3 spritepx worden de donkere vlaktint; rib/naad-stukjes < 3 px vervallen
def comp8(m):
    lab=np.zeros(m.shape,int); n=0; out=[]
    for y0,x0 in zip(*np.where(m)):
        if lab[y0,x0]: continue
        n+=1; st=[(y0,x0)]; lab[y0,x0]=n; cl=[]
        while st:
            y,x=st.pop(); cl.append((y,x))
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    yy,xx=y+dy,x+dx
                    if 0<=yy<64 and 0<=xx<64 and m[yy,xx] and not lab[yy,xx]: lab[yy,xx]=n; st.append((yy,xx))
        out.append(cl)
    return out
for cl in comp8(LIJN==1):
    if len(cl)<4:
        for y,x in cl: LIJN[y,x]=2 if GRP[o[y,x]]=='roze' else 6
for v in (2,6):
    for cl in comp8(LIJN==v):
        if len(cl)<4:
            for y,x in cl: LIJN[y,x]=0
for y,x in zip(*np.where(LIJN>0)): zet(y,x,LIJN[y,x],'L')
# ---- A: lijnen 1 px dun (weghalen breekt geen verbinding en een 4-buur in dezelfde lijntint is minstens zo sterk) -> vlaktint
def simpel(y,x,v):
    ring=[(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
    b=[0<=y+dy<64 and 0<=x+dx<64 and o[y+dy,x+dx]==v for dy,dx in ring]
    if sum(b)<2: return False
    return sum(1 for i in range(8) if b[i] and not b[(i+1)%8])==1
for rnd in range(3):
    for n,y,x in sorted([(cnt[y,x],y,x) for y,x in zip(*np.where((o==1)|(o==2)|(o==6)))]):
        v0=o[y,x]
        if R0[y,x] or OOG(y,x) or log and not any(r[1]==x and r[2]==y and r[0]=='L' for r in log[-1:]) and False: continue
        sterk=[1 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if o[y+dy,x+dx]==v0 and cnt[y+dy,x+dx]>=n]
        if sterk and simpel(y,x,v0):
            v=vlaktint(y,x,zonder_donker=True)
            if v and GRP[v]!='wit': zet(y,x,v,'A')
# ---- V: losse lijnpixel (zwart of donkergroen/-roze binnenlijn met geen enkele 8-buur in een lijntint en geen rand) -> vlaktint
for rnd in range(2):
    for y,x in zip(*np.where((o==1)|(o==2)|(o==6))):
        if R0[y,x] or OOG(y,x): continue
        if 4<=x<=17 and 24<=y<=33: continue
        nb=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
        if not any(v in (1,2,6) for v in nb) and 0 not in nb:
            v=vlaktint(y,x,zonder_donker=True)
            if v and GRP[v] in ('roze','groen'): zet(y,x,v,'V')
# ---- B: buitenlijn 1 px: zwart aan de schaduwkant (achtergrond onder/rechts), selout aan de lichtkant (boven/links)
R=rand4(o>0)
SEL={'roze':2,'groen':6,'geel':12,'wit':1,'pit':1,'zwart':1}
# lichtkant = buitennormaal (gradient van het gladde silhouet) wijst naar het licht linksboven (-0,45, -0,9)
M=gauss((o>0).astype(float),1.2); gy_,gx_=np.gradient(M)
for y,x in zip(*np.where(R)):
    nx_,ny_=-gx_[y,x],-gy_[y,x]; nn=np.hypot(nx_,ny_)+1e-9
    licht=(-0.45*nx_-0.9*ny_)/nn>LT
    gr=GRP[o[y,x]]
    if gr=='geel': continue                       # tong apart (stap TONG)
    # dunne groene punten (stekels/bracteeen, <= 1 figuurbuur in 4-richting) houden een groene rand
    nb4=sum(1 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if o[y+dy,x+dx]>0)
    if gr=='groen' and nb4<=1: zet(y,x,6,'B'); continue
    zet(y,x,SEL[gr] if licht else 1,'B')
# ---- BR (r2): bracteeen/stekels = groene modelcomponenten los van het groene lijf (>= 8 natieve px; kop, rug, staartknots).
#      Spritepixel met >= BRT van het venster bractee wordt groen: aan de achtergrond donkergroen (punt/selout), binnen licht groen.
from lijnen import componenten as _c2
_lab,_size=_c2(g==4); _big=max(_size,key=_size.get)
BRM=(g==4)&(_lab!=_big)
for n,sz in _size.items():
    if n!=_big and sz<8: BRM[_lab==n]=False
BRT=arg('--brt',.25)
for y in range(64):
    for x in range(64):
        sl=venster(y,x)
        if sl[0].stop<=sl[0].start or sl[1].stop<=sl[1].start: continue
        f=BRM[sl].mean()
        if f<BRT or GRP.get(o[y,x]) in ('geel','wit','pit') or OOG(y,x): continue
        if o[y,x]==0:
            if any(o[y+dy,x+dx]>0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): zet(y,x,6,'BR')
            continue
        rand=any(o[y+dy,x+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
        zet(y,x,6 if rand else 8,'BR')
# ---- SP (r2): stekel-/bracteepunten uit het model (stekels.py: uitsteeksel = silhouet min opening r 6; punt = verst van de
#      kern, voet = dichtstbijzijnde kernpixel). Het lijnstuk voet->punt wordt geprojecteerd; achtergrondpixels erop die aan de
#      figuur raken worden donkergroen (stekelpunt zoals op de teju-sprite). Tong (geel) en tand (wit) uitgezonderd.
from stekels import punten
SPLOG=[]
for (tx,ty),(vx,vy),sz,dd in punten(g):
    if g[ty,tx] in (6,8) or g[vy,vx]==8: continue
    _X,_Y=n2s(tx+.5,ty+.5)
    if _X<=9 and 24<=_Y<=34: continue                 # tandpunt in de bek: geen stekel (r2)
    pad=[]
    for t in np.linspace(0,1,40):
        X,Y=n2s(vx+.5+t*(tx-vx),vy+.5+t*(ty-vy))
        if (Y,X) not in [p[:2] for p in pad]: pad.append((Y,X,t))
    for y,x,t in pad:
        if o[y,x]==0 and any(o[y+dy,x+dx]>0 for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx):
            zet(y,x,6,'SP'); SPLOG.append((x,y,tx,ty))
        elif GRP.get(o[y,x])=='roze' and o[y,x]!=2 and t>=0.3:
            zet(y,x,8,'SP')          # groene stekelvoet in het roze (model: groene bractee loopt het roze in)
        elif o[y,x] in (2,) and t>=0.5:
            zet(y,x,6,'SP')          # punt op de roze selout: donkergroen
# ---- C: losse vulpixel (8-cluster van 1 in zijn tint) -> meest voorkomende buurtint uit dezelfde groep
for rnd in range(2):
    for y,x in zip(*np.where(o>1)):
        gr=GRP[o[y,x]]
        if gr not in ('roze','groen') or R[y,x] or o[y,x] in (2,6): continue
        nb=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
        if o[y,x] in nb: continue
        c=Counter(v for v in nb if GRP.get(v)==gr and v not in (2,6))
        if c: zet(y,x,c.most_common(1)[0][0],'C')
# ---- OOG/BEK/TONG: per pixel uit de modelmeting (fracties per spritepixel in *_info.npz; natieve kaart in NOTITIES.md)
KOP=[
 # oog: model natief x46-54, y81-89: lid schuin (53,81)->(46,86), pupil = kolom 49 (y83-88), wit x50-53
 (10,21,1,'OOG lid: zwart 32 % van het venster (modellid)'),
 (11,21,1,'OOG lid: zwart 24 %, lid loopt door naar de ooghoek'),
 (10,22,11,'OOG wit: 84 % wit, modeltint 252 = lichtste wit'),
 (10,23,10,'OOG onderkant: wit 52 % met modelgrijs (199-241) -> grijs (schaduw onder in het oog)'),
 # bek
 (6,27,11,'TAND 2: 49 % wit (model natief x35-39, y102-105)'),
 (13,25,11,'TAND 3 (hoektand in de mondhoek): 43 % wit, modeltint 245'),
 (9,27,15,'PIT: sterkste pit-fractie in het vlees-binnenvlak (17 %)'),
 (11,28,15,'PIT: 10 %, niet 8-naast de andere pit, 1 niet-vleesbuur (fase 2-regel)'),
 (9,30,10,'BEK binnen: tussen tong en onderlip; model rij 113-116 = rood/wit gemengd; grijs i.p.v. roze (fase 2: geen roze binnenin)'),
]
MET_TONG=((kaal>=12)&(kaal<=14)).any()
for x,y,v,r in KOP:
    if 'tong' in r and not MET_TONG: continue        # alleen voor de versie met tong
    zet(y,x,v,'KOP')
# tong: tint per pixel uit de gemiddelde modelhelderheid van de gele modelpixels in het venster (drempels = de eigen
#       modeltonen: olijfrand < 140, midden 140-195, licht >= 195); geeft het lichte streepje linksboven en de olijfrand rechtsonder
for y,x in zip(*np.where((o>=12)&(o<=14))):
    sl=venster(y,x); m=g[sl]==8
    if not m.any(): continue
    l=lum[sl][m].mean(); zet(y,x,12 if l<140 else (13 if l<195 else 14),'TONG')
# ---- RECHT: rechte randstukken > 10 px (horizontaal, onderrand): eindpixels met de hoogste achtergrondfractie (>= 0,25) weg
#      zodat de rand een trapje krijgt; de pixel erboven wordt de zwarte buitenlijn (schaduwkant).
def runs_onder():
    fig=o>0; out=[]
    for y in range(1,63):
        x=0
        while x<64:
            if fig[y,x] and not fig[y+1,x]:
                x1=x
                while x1+1<64 and fig[y,x1+1] and not fig[y+1,x1+1]: x1+=1
                if x1-x+1>10: out.append((y,x,x1))
                x=x1+1
            else: x+=1
    return out
for y,x0,x1 in runs_onder():
    for x in (x0,x0+1,x1,x1-1):
        if F[0][y,x]>=0.25 and o[y-1,x]>0:
            zet(y,x,0,'RECHT'); zet(y-1,x,1,'RECHT')
# ---- C2: losse vulpixel ook op de rand (geen 8-buur in dezelfde tint, geen oog/bek/tong) -> meest voorkomende buurtint uit de groep
for y,x in zip(*np.where(o>1)):
    gr=GRP[o[y,x]]
    if gr not in ('roze','groen') or (4<=x<=17 and 20<=y<=33): continue
    nb=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
    if o[y,x] in nb: continue
    c=Counter(v for v in nb if GRP.get(v)==gr)
    if not c: c=Counter(v for v in nb if GRP.get(v) in ('roze','groen') and v not in (2,6))
    if c: zet(y,x,c.most_common(1)[0][0],'C2')
np.save(UIT[:-4]+'_stand.npy',o)
# ---- R2: benoemde reparaties ronde 2, per pixel met modelmeting (meet.py: achtergrond/zwart/groen-fractie, gem. helderheid groen)
R2=[
 # kop/bek (meting: f1 = zwartfractie, f6 = witfractie, f0 = achtergrond)
 (3,27,1,'KAAKLIJN onder de snuit: 40 % zwart; dicht het gat in de lijn (2..7,27)'),
 (2,28,0,'TAND 1: 91 % achtergrond; was zwart/groen door de randstap'),
 (3,28,11,'TAND 1 (snuitpunt): model wit natief x24-26, y102-106 (15 % van het venster, < 1 spritepx); 1 px wit hangend onder de kaaklijn, zoals tand 2/3'),
 (5,25,2,'NEUSGAT: 22 % zwart (dunne donkere modellijn op de snuit); donkerroze binnenlijn'),
 (11,29,1,'BEKHOEK: 35 % zwart; sluit het vruchtvlees rechtsonder af'),
 (10,30,1,'ONDERLIP-LIJN: 31 % zwart; scheidt vruchtvlees/tong van de onderkaak'),
 # voorste hand: 3 modelklauwen op x 9,9-10,7 / 11,3-12,4 / 13,2-14,1; op 64 px 2 klauwen + inkeping
 (10,44,9,'KLAUW voorhand: groen 82 %, zwart 16 %; lichte klauw (lum 101, lichter dan de hand 80-95)'),
 (11,44,1,'KLAUW voorhand: 48 % zwart = lijn tussen de klauwen'),
 (12,44,9,'KLAUW voorhand: groen 56 %, lum 98; lichte klauw'),
 (13,44,1,'KLAUW voorhand: 42 % zwart, 12 % achtergrond = rand'),
 (10,45,1,'KLAUWPUNT: 39 % zwart, 34 % achtergrond = lijn onder de klauw'),
 (11,45,0,'INKEPING tussen de klauwen: 31 % achtergrond + 47 % zwart (lijn); achtergrond zodat de klauwen los lezen'),
 (12,45,1,'KLAUWPUNT: 42 % zwart'),
 (13,45,0,'82 % achtergrond (was stekelpunt-groen)'),
 (12,46,0,'66 % achtergrond (zwart restje onder de klauw)'),
]
for x,y,v,r in R2: zet(y,x,v,'R2')
# nabije hand (x 27-35, y 44-48): de zwarte klont = 4 modelklauwen met zwarte lijnen ertussen. Regel uit de meting:
# zwart alleen bij >= 30 % zwart, anders groen naar de helderheid van de groene modelpixels (>= 115 licht = klauw, >= 90 midden)
gu=np.repeat(np.repeat(g,4,0),4,1); lu=np.repeat(np.repeat(lum,4,0),4,1)
def win4(X,Y):
    ny=by0-S+OY+S*(Y-Y0+ymin); nx=bx0-S+OX+S*(X-X0+xmin)
    return slice(int(round(4*ny)),int(round(4*(ny+S)))),slice(int(round(4*nx)),int(round(4*(nx+S))))
for Y in range(44,49):
    for X in range(27,36):
        if o[Y,X]==0: continue
        sl=win4(X,Y); gb=gu[sl]; n=gb.size; m=gb==4
        if (gb==0).sum()/n>=0.5: continue
        if (gb==1).sum()/n>=(0.25 if Y>=46 else 0.30): zet(Y,X,6,'HAND'); continue      # lijn tussen de klauwen: donkergroen (geen klont zwart)
        l=lu[sl][m].mean() if m.any() else 0
        if Y>=47: zet(Y,X,9 if l>=90 else 7,'HAND')                 # klauwpunten onderaan lichter (model lum 90-101 vs hand 80-90)
        else: zet(Y,X,8 if l>=100 else 7,'HAND')
# staartonderkant: rij 62 alleen x 40-45 (model is daar vlak; 1 px hoger aan de uiteinden geeft de boog, opdracht r2)
for x in (37,38,39,46,47,48):
    if o[62,x]>0: zet(62,x,0,'STAART'); zet(61,x,1,'STAART')
# staart rechterkant: kolom 61 was 10 px recht (rij 46-55); uiteinden met de hoogste achtergrondfractie weg (42/44 %, 9/12 %) -> 6 px,
# de pixel links ervan wordt de zwarte rand (schaduwkant)
for y in (46,47,54,55):
    if o[y,61]>0: zet(y,61,0,'STAART'); zet(y,60,1,'STAART')
# dambord (2x2 om-en-om van twee vultinten): de pixel die het minst op zijn 8 buren lijkt neemt de meest voorkomende buurtint
for rnd in range(2):
    for y in range(1,62):
        for x in range(1,62):
            q=o[y:y+2,x:x+2]
            if not (q[0,0]==q[1,1] and q[0,1]==q[1,0] and q[0,0]!=q[0,1]): continue
            if not all(GRP.get(v) in ('roze','groen') and v not in (2,6) for v in q.ravel()): continue
            best=None
            for yy,xx in ((y,x),(y,x+1),(y+1,x),(y+1,x+1)):
                nb=[o[yy+dy,xx+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
                same=sum(1 for v in nb if v==o[yy,xx])
                if best is None or same<best[0]: best=(same,yy,xx,Counter(v for v in nb if GRP.get(v) in ('roze','groen') and v not in (2,6)).most_common(1)[0][0])
            zet(best[1],best[2],best[3],'DB')
# losse vulpixels opnieuw (na alle stappen)
for rnd in range(2):
    for y,x in zip(*np.where(o>1)):
        gr=GRP[o[y,x]]
        if gr not in ('roze','groen') or (4<=x<=17 and 20<=y<=33) or (27<=x<=35 and 47<=y<=48) or (9<=x<=13 and 44<=y<=45): continue
        nb=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
        if o[y,x] in nb: continue
        c=Counter(v for v in nb if GRP.get(v)==gr and v!=o[y,x])
        if not c: c=Counter(v for v in nb if v>0)
        if c: zet(y,x,c.most_common(1)[0][0],'LOS')
# ---- PALET (r2): roze, groen, vruchtvlees en pit = tinten van de teju-sprite (fase 2, af); geel/zwart blijven modeltonen
TEJU={2:(104,24,56),3:(177,40,84),4:(231,78,123),5:(248,160,192),6:(48,88,48),7:(79,128,64),8:(120,168,80),9:(176,208,104),
      10:(191,189,192),11:(237,234,237),15:(44,42,46),1:(19,19,15)}
pal=list(pal)
for i,c in TEJU.items(): pal[3*i:3*i+3]=list(c)
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(pal); im.save(UIT,transparency=0)
with open(UIT[:-4]+'_afwijkingen.txt','w') as f:
    f.write('stap x y oud nieuw\n')
    for r in log: f.write('%s %d %d %d %d\n'%r)
c=Counter(r[0] for r in log); tot=(o>0).sum()
print(UIT,dict(c),'px',tot,'zwart binnen %.1f%%'%(100*((o==1)&~rand4(o>0)).sum()/tot),'kleuren',len(set(o.ravel())))
