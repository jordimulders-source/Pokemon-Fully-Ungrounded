# Volgorde om alles opnieuw te maken: klassen.py -> draden.py -> draadlijnen.py -> stap1.py -> skel.py -> fijnmap.py
# -> (mond: python3 -c met mond_model, zie mond.py) mond.py -> mondpoly.py -> shuppet.py -> build.py -> vel.py cur.npy vel.png
# Controle: controle.py cur.npy. Hulpmiddelen: raster.py / fijn.py / overlay.py (model met spriteraster), cmp4.py.
# Banette-evolutie r1: model overnemen (kale reductie) + benoemde reparaties per zone
import numpy as np; from view import png,zij
S=968/62
d=np.load('stap1.npz'); cov,maj,lum=d['cov'],d['maj'],d['lum']; cnt=np.load('skel_cnt.npy'); F=np.load('fijn.npy')
# ---------- 1. kale reductie (b2) ----------
sil=cov>=0.45
def fill(m,l):
    if m==2: return 3 if l>=118 else 4
    if m==3: return 6 if l>=112 else 7
    if m==4: return 8
    if m==5: return 9
    if m==6: return 10 if l>=135 else (11 if l>=108 else 12)
    if m==7: return 13
    return 1
g=np.zeros((64,64),int)
for j in range(64):
  for i in range(64):
    if sil[j,i]: g[j,i]=fill(maj[j,i],lum[j,i])
g[(cnt>=0.5*S)&sil]=1
kaal=g.copy()
LOG={}
VAST=set()   # pixels die per pixel uit het model zijn gezet (ogen, bellen, kruizen): niet herkleuren
def put(name,pts):
    n=0
    for (x,y),v in pts:
        if g[y,x]!=v: n+=1
        g[y,x]=v
    LOG[name]=LOG.get(name,0)+n
def grid(name,x0,y0,rows,key):
    pts=[]
    for dy,row in enumerate(rows):
        for dx,ch in enumerate(row):
            if ch==' ' or ch=='_': continue
            pts.append(((x0+dx,y0+dy),key[ch])); VAST.add((x0+dx,y0+dy))
    put(name,pts)
np.save('kaal.npy',kaal)
# ---------- 2. mond: polygoon uit de modelranden ----------
M=np.load('mond_sprite.npy')
# oude mondpixels (bruin/zwart in de kale reductie binnen de mondzone) die buiten de polygoon vallen -> huid van de buren
pts=[]
for j in range(30,44):
  for i in range(14,44):
    if M[j,i]:
        nb=M[j-1,i] and M[j+1,i] and M[j,i-1] and M[j,i+1]
        pts.append(((i,j),8 if nb else 1))
put('mond',pts)
def huid(i,j):
    # huidtint uit de kale reductie: rood of grijs naar meerderheid van het model in dit vak
    return 6 if F[j,i,5]+F[j,i,6]>F[j,i,3]+F[j,i,2] else 3
pts=[]
for j in range(30,45):
  for i in range(14,44):
    if not M[j,i] and g[j,i] in (1,8) and sil[j,i]:
        # alleen als het model hier geen eigen lijn heeft buiten de mond (buitenrand blijft)
        P=np.pad(sil,1); inner=P[j,i+1]&P[j+2,i+1]&P[j+1,i]&P[j+1,i+2]
        if inner and cnt[j,i]<0.5*S*2: pts.append(((i,j),huid(i,j)))
put('mond_rest',pts)
# ---------- 3. ogen: per pixel gemeten op het model (fijn.py 15 24 37 32) ----------
# k zwart, O ring (rood licht), Y iris, d oogkas (grijs donker), r huid rood, g huid grijs
KEY={'k':1,'O':5,'Y':9,'d':4,'r':6,'g':3,'D':14}
grid('oog_links',16,26,[
 "k__kk__",
 "kkkOk__",
 "kOOOk__",
 "kOYkOk_",
 "kOYkOdk",
 "_kOOOkk",
 "__kkk__"],KEY)
grid('oog_rechts',26,24,[
 "____kkk_kk_",
 "____kOOkddk",
 "___kkYkOddk",
 "___kOYkOddk",
 "__kdOYkOdk_",
 "_kddOOOOk__",
 "kkkkkkkk___"],KEY)
# ---------- 4. belletjes: één sjabloon, gemeten op het linkerbelletje (fijn.py 3 31 14 40) ----------
BEL=["_kkkk_",
     "kWLggk",
     "kLgggk",
     "kgkkdk",
     "kdgkdk",
     "_kkkk_"]
BK={'k':1,'W':13,'L':2,'g':3,'d':4}
grid('bel_links',5,32,BEL,BK)
grid('bel_rechts',50,16,BEL,BK)
# ---------- 4b. Shuppets: eigen reductie per Shuppet (shuppet.py): silhouet (dekking >= 0,5), kop vóór lijf,
#             tonen uit de gladgemaakte modelhelderheid, binnenlijnen alleen waar het model ze in het lijf heeft (armen)
from scipy import ndimage as ndi
SH=np.load('shuppet.npy',allow_pickle=True)[0]
KOPGRENS={'L':49,'R':54}
for z,(cv,lm,sc) in SH.items():
    ss=cv>=0.5
    HOORN={'L':41,'R':46}[z]
    ss[:HOORN+1]|=(cv[:HOORN+1]>=0.35)      # hoorn: dunne punt, lagere drempel zodat hij niet wegvalt
    ys,xs=np.where(ss); yb0,yb1,xb0,xb1=ys.min()-1,ys.max()+2,xs.min()-1,xs.max()+2
    kop=ss.copy(); kop[KOPGRENS[z]+1:]=False
    lijf=ss&~kop
    # gladgemaakte helderheid (alleen binnen het silhouet)
    w=ndi.gaussian_filter(ss.astype(float),0.9); lv=ndi.gaussian_filter(np.where(ss,lm,0),0.9)/np.maximum(w,1e-6)
    pts=[]
    for j in range(yb0,yb1):
      for i in range(xb0,xb1):
        if not ss[j,i]:
            if g[j,i] in (10,11,12,14) or (g[j,i]==1 and F[j,i,8]>0.05 and F[j,i,3]+F[j,i,2]<0.2): pts.append(((i,j),0))
            continue
        deel=kop if kop[j,i] else lijf
        P=np.pad(deel,1)
        u,d_,l_,r_=not P[j,i+1],not P[j+2,i+1],not P[j+1,i],not P[j+1,i+2]
        if u or d_ or l_ or r_:
            # rand naar de kop toe (lijf onder de kop) telt als binnenlijn
            licht=(u or l_) and not (d_ or r_)
            if deel is lijf and u and kop[j-1,i] and not (d_ or l_ or r_):
                v=(lv[j,i]-80)/10; pts.append(((i,j),10 if v>=5.5 else (11 if v>=2.5 else 12))); continue
            pts.append(((i,j),14 if licht else 1)); continue
        if deel is lijf and sc[j,i]>=0.8*S: pts.append(((i,j),14)); continue
        v=(lv[j,i]-80)/10
        pts.append(((i,j),10 if v>=5.5 else (11 if v>=2.5 else 12)))
    put('shuppet_'+z,pts)
# ---------- 4c. Shuppet-lijven: per pixel overgenomen van het model (raster.py 2 37 17 57 / 46 40 62 63); de reductie gaf vlekken ----------
SK={'k':1,'s':14,'l':10,'m':11,'d':12,'.':0}
grid('shuppet_L_lijf',5,50,[
 "__smmmkssk..",
 "ssmmmmslmk..",
 "sllmmmslmk..",
 "kkmmmdsmdk..",
 ".smmddkddk..",
 ".kdddkddk...",
 "..kkk.kk...."],SK)
grid('shuppet_R_lijf',46,55,[
 "____smmmdk....",
 ".sssmmmmdssk..",
 ".sllmmmmsmmdk.",
 ".kkkkmmdsmddk.",
 "....smdsdddk..",
 "....kmddddddk.",
 ".....kkkkkkk.."],SK)
# ---------- 5. Shuppet-ogen: gemeten op het model (raster.py) ----------
# oogring in marine (het model heeft een donkerblauwe ring, geen zwarte); de rand van de kop blijft zwart
EK={'k':1,'n':14,'C':10,'W':13}
grid('shuppet_L_oog_voor',9,44,["_nn_","nCCn","nWCn","_nn_"],EK)
grid('shuppet_L_oog_ver',4,45,["_nn","kCn","_nn"],EK)
grid('shuppet_R_oog_voor',52,50,["_nnn_","nCWCn","_nnn_"],EK)
grid('shuppet_R_oog_ver',47,50,["_nn","kCn","_nn"],EK)
# ---------- 6. kruizen en armen ----------
# Kruisen: twee rechte balken op de hartlijnen en de breedte gemeten op het model (raster.py 43 13 64 37 / 0 13 18 33);
# zo blijven vorm en eindpunten van het model en vallen knipranden/ruis weg. Arm rechts: omtrek gemeten op het model.
from matplotlib.path import Path
def seg(p,a,b):
    p,a,b=map(np.array,(p,a,b)); t=np.clip(np.dot(p-a,b-a)/np.dot(b-a,b-a),0,1); return np.linalg.norm(p-(a+t*(b-a)))
def balken(bars,w,box):
    x0,y0,x1,y1=box; m=np.zeros((64,64),bool)
    for j in range(y0,y1):
        for i in range(x0,x1):
            m[j,i]=any(seg((i+0.5,j+0.5),a,b)<=w/2 for a,b in bars)
    return m
def poly(pts):
    P=Path(pts); m=np.zeros((64,64),bool)
    for j in range(64):
        for i in range(64): m[j,i]=P.contains_point((i+0.5,j+0.5))
    return m
KR=balken([((51.0,25.6),(59.4,18.4)),((51.5,18.0),(61.6,25.0))],3.3,(44,14,64,30))
KL=balken([((4.3,18.2),(8.8,24.6)),((2.0,24.8),(10.0,17.9))],2.8,(0,14,14,30))
AR=poly([(49.0,16.4),(50.6,17),(50.6,22),(50.2,27),(49.6,28.3),(47.5,30.6),(45.4,33.6),(44.5,33.6),(44.5,27),(45.0,27),(45.6,25),(46.4,23),(47.2,21),(48.0,19)])
# linkerarm: in het model achter de mutspunt; zichtbaar gemaakt in de holte onder het kruis als gespiegelde rechterarm
# (zelfde breedte/helling als rechterarm rij 24-31, gespiegeld rond de figuur), loopt achter de mutspunt (x>=7) en het belletje
AL=poly([(2.6,25.5),(7.6,25.5),(7.6,32.2),(6.6,32.2),(4.6,29.6),(3.0,27.4)])
ROOD={5,6,7}
# rechterkant leegmaken (behalve rood hoofd) en opbouwen: arm, kruis (bel komt hierna weer terug)
pts=[]
for j in range(14,30):
  for i in range(45,64):
    if g[j,i] not in ROOD and not (i<=45 and g[j,i]==1 and j>=24): pts.append(((i,j),0))
put('rechts_leeg',pts)
def teken(m,naam,schaduw_rechts=True,achter=()):
    # kruis: zwarte omlijning rondom (zoals het model), bovenvlak licht, zijvlak (dikte) donker langs de onderrand
    P=np.pad(m,1); pts=[]
    for j,i in zip(*np.where(m)):
        if g[j,i] in achter: continue
        u,d,l,r=not P[j,i+1],not P[j+2,i+1],not P[j+1,i],not P[j+1,i+2]
        if u or d or l or r: pts.append(((i,j),1))
        elif not P[j+2,i+1] or not P[j+3,i+1] and not P[j+2,i]: pts.append(((i,j),4))
        elif not P[j+2,i+1+1] and not P[j+2,i]: pts.append(((i,j),4))
        else: pts.append(((i,j),2))
    put(naam,pts); VAST.update(p for p,v in pts)
# arm rechts: lichte linkerkant, donkere strook rechts (zoals het model), achter het rode hoofd
pts=[]; P=np.pad(AR,1)
for j,i in zip(*np.where(AR)):
    if g[j,i] in ROOD or (g[j,i]==1 and i<=44): continue
    u,d,l,r=not P[j,i+1],not P[j+2,i+1],not P[j+1,i],not P[j+1,i+2]
    if r or d: v=1
    elif l or u: v=4 if (g[j,i-1]==0) else 2
    elif not P[j+1,i+3]: v=4
    elif not P[j+1,i-1] or not P[j+1,i]: v=2
    else: v=3
    pts.append(((i,j),v))
put('arm_rechts',pts); VAST.update(p for p,v in pts)
teken(KR,'kruis_rechts')
# links: kruis over de bestaande pixels (niet over de mutspunt: alles rechts van de mutsrand blijft)
MUTS=np.zeros((64,64),bool)
for j in range(14,34):
    xs=[i for i in range(0,16) if g[j,i]==1 and F[j,i,2]+F[j,i,3]>0.3 and i>=7]
pts=[]
for j in range(15,28):
  for i in range(0,10):
    if (i,j) in VAST: continue
    if KL[j,i] or (g[j,i] in (2,3,4,1) and i<=6): pts.append(((i,j),0))
put('links_leeg',pts)
# arm links eerst (achter kruis en mutspunt), dan kruis
pts=[]; P=np.pad(AL,1)
for j,i in zip(*np.where(AL)):
    if g[j,i]!=0 and (i,j) not in VAST and not (g[j,i] in (2,3,4) and i<=6): continue
    leeg=lambda x,y: not P[y+1,x+1] and g[y,x]==0
    u,d,l,r=leeg(i,j-1),not P[j+2,i+1],leeg(i-1,j),not P[j+1,i+2]
    if (l or u) and not d: v=4
    elif d or (l and d): v=1
    elif not P[j+1,i+2]: v=4
    elif not P[j+1,i]: v=2
    else: v=3
    pts.append(((i,j),v))
put('arm_links',pts); VAST.update(p for p,v in pts)
teken(KL,'kruis_links',achter=())
# belletjes opnieuw bovenop (hangen vóór kruis en arm)
grid('bel_links',5,32,BEL,BK)
grid('bel_rechts',50,16,BEL,BK)
# ---------- 7. buitenlijn: 1 px, zwart aan de schaduwkant, gekleurde selout aan de lichtkant ----------
GRP={2:'g',3:'g',4:'g',14:'b',13:'g',5:'r',6:'r',7:'r',10:'b',11:'b',12:'b',15:'r',8:'m',9:'r'}
SEL={'g':4,'r':7,'b':14}
def groep(i,j):
    if g[j,i] in GRP and g[j,i]!=1: return GRP[g[j,i]]
    vs=[GRP[g[y,x]] for x,y in ((i-1,j),(i+1,j),(i,j-1),(i,j+1),(i-1,j-1),(i+1,j+1),(i-1,j+1),(i+1,j-1)) if 0<=x<64 and 0<=y<64 and g[y,x] in GRP]
    return max(set(vs),key=vs.count) if vs else 'g'
fig=g>0
P=np.pad(fig,1)
up,dn,lf,rt=~P[:-2,1:-1],~P[2:,1:-1],~P[1:-1,:-2],~P[1:-1,2:]
pts=[]
for j in range(64):
  for i in range(64):
    if not fig[j,i]: continue
    if not(up[j,i] or dn[j,i] or lf[j,i] or rt[j,i]): continue
    licht=(up[j,i] or lf[j,i]) and not (dn[j,i] or rt[j,i])
    G=groep(i,j)
    pts.append(((i,j),SEL[G] if (licht and G in SEL) else 1))
put('buitenlijn',[(p,v) for p,v in pts if p not in VAST])
# ---------- 8. draden: middellijnen uit het model (draadlijnen.py), 1 px, alleen op lege pixels ----------
LIJN=np.load('draadlijnen.npy',allow_pickle=True)[0]
DRAAD=set()
def draad(pts,naam,verleng_onder=False,verleng_boven=True):
    pts=np.array(pts); xs,ys=pts[:,0],pts[:,1]
    y0,y1=ys.min(),ys.max()
    def xat(y):
        if y<=y0: return xs[0]+(y-y0)*(xs[1]-xs[0])/max(ys[1]-ys[0],1e-6) if False else np.interp(y,ys,xs)
        return np.interp(y,ys,xs)
    # helling over de hele lijn voor verlengen
    k=(xs[-1]-xs[0])/(ys[-1]-ys[0])
    out=[]
    j=int(np.floor(y0))
    # omhoog verlengen tot het kruis (eerste niet-lege pixel)
    if verleng_boven:
        jj=j
        while jj>j-3:
            x=int(np.floor(xs[0]+(jj+0.5-ys[0])*k))
            if g[jj,x]!=0: break
            out.append((x,jj)); jj-=1
    for jj in range(j,int(np.floor(y1))+1):
        x=int(np.floor(np.interp(jj+0.5,ys,xs)))
        out.append((x,jj))
    if verleng_onder:
        jj=int(np.floor(y1))+1
        while jj<63:
            x=int(np.floor(xs[-1]+(jj+0.5-ys[-1])*k))
            if g[jj,x]!=0: break
            out.append((x,jj)); jj+=1
    # twee draden mogen niet tegen elkaar liggen (anders leest het als één touw van 2 px): 1 px opschuiven, weg van de buur
    oo=[]
    for x,y in out:
        if g[y,x]==0 and (x-1,y) in DRAAD and (x+1,y) not in DRAAD and g[y,x+1]==0: x=x+1
        elif g[y,x]==0 and (x+1,y) in DRAAD and (x-1,y) not in DRAAD and g[y,x-1]==0: x=x-1
        oo.append((x,y))
    pp=[((x,y),4) for x,y in oo if g[y,x]==0]; put(naam,pp); VAST.update(p for p,v in pp); DRAAD.update(p for p,v in pp)
for k,pts in LIJN.items():
    if pts[-1][1]-pts[0][1]<2.5: continue      # stukjes draad in de inkeping van een kruis: vallen weg (1-2 px ruis)
    pts=[(x,y) for x,y in pts]
    draad(pts,'draden',verleng_onder=(k==5))
# ---------- 9. ruis: tintvlakjes < 3 px (8-buren) en losse zwarte pixels midden in een vlak nemen de buurtint aan ----------
from scipy import ndimage as ndi
VUL={2,3,4,5,6,7,8,10,11,12}
for ronde in range(3):
    pts=[]
    for c in VUL|{1}:
        lab,n=ndi.label(g==c,structure=np.ones((3,3)))
        for k in range(1,n+1):
            m=lab==k
            if m.sum()>=3: continue
            for j,i in zip(*np.where(m)):
                if (i,j) in VAST: continue
                nb=[g[y,x] for x in range(i-1,i+2) for y in range(j-1,j+2) if (x,y)!=(i,j) and 0<=x<64 and 0<=y<64]
                if 0 in nb and c==1: continue          # zwart aan de rand = buitenlijn
                if 0 in nb and c in VUL:
                    pts.append(((i,j),1)); continue     # vlakje aan de rand -> omlijning
                cand=[v for v in nb if v in VUL and v!=c]
                if cand: pts.append(((i,j),max(set(cand),key=cand.count)))
    put('ruis',pts)
# ---------- 10. licht linksboven: glansband 1-2 px binnen de buitenrand aan de lichtkant (rood -> 15, grijs -> 2) ----------
fig=g>0
E=np.zeros((64,64),bool)
for j in range(1,63):
    for i in range(1,63):
        if fig[j,i] and (not fig[j-1,i] or not fig[j,i-1]) and fig[j+1,i] and fig[j,i+1]: E[j,i]=True
pts=[]
for j in range(64):
    for i in range(64):
        if (i,j) in VAST: continue
        if g[j,i] not in (6,3): continue
        near=False
        for dx,dy in ((1,1),(0,1),(1,0),(0,2),(2,0),(1,2),(2,1)):
            x,y=i-dx,j-dy
            if 0<=x<64 and 0<=y<64 and E[y,x] and g[y,x] in (1,4,7): near=True
        if near and j<=26: pts.append(((i,j),15 if g[j,i]==6 else 2))
put('licht',pts)
# ---------- 11. buitenlijn eenduidig: per randstuk zwart (schaduwkant) of selout (lichtkant) op de gladgemaakte normaal ----------
fig=g>0
bl=ndi.gaussian_filter(fig.astype(float),1.6); gy,gx=np.gradient(bl)
P=np.pad(fig,1)
pts=[]
for j in range(64):
    for i in range(64):
        if not fig[j,i] or g[j,i] not in (1,4,7,14): continue
        if (i,j) in VAST: continue      # draden, kruisen, bellen, ogen: al per pixel gezet
        if P[j,i+1] and P[j+2,i+1] and P[j+1,i] and P[j+1,i+2]: continue   # geen rand
        nx,ny=-gx[j,i],-gy[j,i]; nn=np.hypot(nx,ny)+1e-9
        licht=(-nx-ny)/nn/1.414>0.30
        G=groep(i,j)
        v=SEL[G] if (licht and G in SEL) else 1
        pts.append(((i,j),v))
put('buitenlijn_normaal',pts)
# ---------- 12. laatste losse pixels en gaatjes (controle.py), per pixel benoemd ----------
put('reparatie',[
 ((26,13),4),((11,19),4),((11,20),4),   # losse lichttint / middentint in de donkere mutsband
 ((51,15),1),                    # rode punt sluit aan op het belletje
 ((50,25),1),((51,22),1),((50,23),1),   # gaatjes en losse pixel waar arm, kruis en bel samenkomen
 ((7,25),1),                     # gaatje tussen kruisonderkant en mutsrand
 ((10,31),1),((10,32),1),        # gaatje tussen mutspunt en draad
 ((56,47),1),                    # gaatje tussen draad en Shuppet-kop rechts
 ((58,49),0),((58,50),0),        # draad 6 eindigt op de kop i.p.v. een gaatje in te sluiten
 ((49,22),4),((49,23),4),((49,24),4),((49,25),4),((49,26),4),   # rechterarm: donkere strook (model 'd'), geen dubbele zwarte lijn tegen het kruis
])
np.save('cur.npy',g)
