# Dundragoon r2 (op r1, 3 benoemde reparaties: lijfhooglicht, oogring, boortinten): model overnemen. Natief raster 99x99 (pitch 10,24; figuur 86x86) -> schaal 61/86 (0,709), figuur x1-61, y1-61.
# Verkleinen = oppervlakteweging per spritepixel over het natieve raster; dunne modellijnen winnen vanaf een drempel ("donkerste wint").
# Daarna alleen technische opschoning en reparaties naar het model; elke stap geteld.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen; from gemeen import *
from gemeen import toon
a,c,L=klassen()
UIT='sprite_r2'
TK=0.30   # zwart wint vanaf 30 % oppervlak
TO=0.30   # olijflijn (geel, L<150) wint vanaf 30 %
TB=0.30   # blauw wint van vleugelwit vanaf 30 % (aders/rand in de vleugel)
def tn(g,l):
    if g==2: return 2 if l<150 else 3 if l<200 else 4 if l<228 else 5
    if g==3: return 6 if l<98 else 7 if l<128 else 8
    if g==4: return 9 if l<185 else 10 if l<221 else 11
o=np.zeros((64,64),int)
for Y in range(64):
    for X in range(64):
        f=np.zeros(5); lum=np.zeros(5); fo=0; fyl=0; lyl=0
        for u,v,w in overlap(X,Y):
            k=c[v,u]; f[k]+=w; lum[k]+=w*L[v,u]
            if k==2:
                if L[v,u]<150: fo+=w
                else: fyl+=w; lyl+=w*L[v,u]
        tot=f[1:].sum()
        if tot<0.5: continue
        if f[1]>=TK: o[Y,X]=1; continue
        if fo>=TO: o[Y,X]=2; continue
        if f[3]>=TB and f[4]>f[2]: o[Y,X]=tn(3,lum[3]/f[3]); continue
        g=2+int(np.argmax(f[2:]))
        if g==2 and fyl>0: o[Y,X]=tn(2,lyl/fyl)
        else: o[Y,X]=tn(g,lum[g]/f[g])
kaal=o.copy(); opslaan(kaal,UIT+'/kaal.png')
if len(sys.argv)>1 and sys.argv[1]=='kaal':
    toon(o,0,64,0,64); sys.exit()

tel={}
def stap(n,v,o): tel[n]=tel.get(n,0)+int((v!=o).sum())
GRP={k:(GEEL if k in GEEL else BLAUW if k in BLAUW else VLEUGEL) for k in range(2,12)}
SEL={**{k:2 for k in GEEL},**{k:6 for k in BLAUW},**{k:9 for k in VLEUGEL}}
# --- 1. buitenlijn: geen open of lichte rand. Achtergrond rechts/onder = zwart (schaduwkant); lichtkant = selout van de groep. Zwart blijft zwart. ---
def rand(o):
    fg=o>0; uit=[]
    for Y,X in zip(*np.where(fg)):
        k=o[Y,X]
        if k==1: continue
        bgL=not fg[Y,X-1]; bgR=not fg[Y,X+1]; bgU=not fg[Y-1,X]; bgD=not fg[Y+1,X]
        if not(bgL or bgR or bgU or bgD): continue
        n=1 if (bgR or bgD) else SEL[k]
        if n!=k: uit.append((Y,X,n))
    for Y,X,k in uit: o[Y,X]=k
v=o.copy(); rand(o); stap('buitenlijn',v,o)
# --- 2. ontkorrelen: tintvlekjes < 3 px (hooglicht < 2) nemen de meest voorkomende buurtint van dezelfde groep aan (lijnen 2/6/9 niet) ---
def ontkorrel(o):
    for k,minim in ((3,3),(4,3),(5,2),(7,3),(8,2),(10,3),(11,2)):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=minim: continue
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[Y+dy,X+dx] in GRP[k] and o[Y+dy,X+dx]!=k and o[Y+dy,X+dx]!=SEL[k]]
            if buur: o[m]=max(set(buur),key=buur.count)
v=o.copy(); ontkorrel(o); ontkorrel(o); stap('ontkorrelen',v,o)
# --- 3. losse zwarte pixel midden in een vlak (geen zwarte 8-buur, geen achtergrond) -> buurtint ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    nb=[o[Y+dy,X+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
    nb8=[o[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
    if 0 not in nb8 and 1 not in nb8: o[Y,X]=max(set(nb),key=nb.count)
stap('losse zwarte pixels',v,o)

# --- 4. oog: blauwe ring uit de modeldekking (blauw >= 45 % van de spritepixel = ring), toon uit de gemiddelde modelhelderheid
#        (< 112 donker, anders midden); overige blauwe restjes binnen het oogvak -> geel midden. Ooglijn = kale reductie (bleef heel). ---
v=o.copy()
for Y in range(9,21):
    for X in range(8,22):
        if (Y<=10 and X>=18) or (Y>=19 and X<=10): continue
        fb=lb=0
        for u,v_,w in overlap(X,Y):
            if c[v_,u]==3: fb+=w; lb+=w*L[v_,u]
        if fb>=0.45: o[Y,X]=7
        elif o[Y,X] in BLAUW: o[Y,X]=4
# r2 (coördinator): hele ring middenblauw, alleen de buitenrand donker (ringpixel met een 4-buur buiten de ring)
ring=np.zeros((64,64),bool); ring[9:21,8:22]=o[9:21,8:22]==7
for Y in range(9,21):
    for X in range(8,22):
        if (Y<=10 and X>=18) or (Y>=19 and X<=10): ring[Y,X]=False
buiten=np.zeros((64,64),bool); st=[(8,7)]; buiten[8,7]=True
while st:
    y_,x_=st.pop()
    for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
        yy,xx=y_+dy,x_+dx
        if 7<=yy<=22 and 6<=xx<=23 and not ring[yy,xx] and not buiten[yy,xx]: buiten[yy,xx]=True; st.append((yy,xx))
for Y,X in zip(*np.where(ring)):
    if any(buiten[Y+dy,X+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): o[Y,X]=6
stap('oog (ring uit model)',v,o)

# --- 5. boor (Jordi: "de drill is nog niet zo mooi, maar dat kunnen we in de sprite met kleurgebruik oplossen"; vorm = model).
#        a) de spiraallijnen komen uit het model: elke olijflijn van het natieve model (8-samenhangend cluster in de boor) wordt
#           punt voor punt naar de sprite gemapt en als 1-px lijn gezet (de reductie brak ze in stukjes);
#        b) vultinten (3/4/5) per dwarsdoorsnede van de kegel: onder/links schaduw (zoals het model), midden, lichte band
#           bovenop (licht van boven), midden vlak vóór de zwarte rand. Buitenlijn en silhouet blijven. ---
v=o.copy()
dd=np.array([14,20.]); dd/=np.linalg.norm(dd); nn=np.array([dd[1],-dd[0]])
fg=o>0
L0={41:53,42:53,43:53,44:52,45:51,46:47}   # overgangslijn lijf->boor (uit de reductie): links ervan is staartlijf
boor=np.zeros((64,64),bool)
for Y in range(41,64):
    for X in range(44,64):
        if o[Y,X] and X>L0.get(Y,0): boor[Y,X]=True
def aanrand(Y,X): return any(not fg[Y+dy,X+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
for Y,X in zip(*np.where(boor)):
    if o[Y,X]==2 and not aanrand(Y,X): o[Y,X]=4      # gebroken reductielijnen weg (worden hieronder uit het model teruggezet)
for Y,X in zip(*np.where(boor)):
    if o[Y,X] in (3,5): o[Y,X]=4          # vultinten opnieuw, per segment (hieronder, na de lijnen)
sl_kegel={}
for Y,X in zip(*np.where(boor)):
    a_=int(round(dd@[X,Y])); s_=nn@[X,Y]; lo,hi=sl_kegel.get(a_,(1e9,-1e9)); sl_kegel[a_]=(min(lo,s_),max(hi,s_))
# a) modellijnen
ol=(c==2)&(L<150); lab,n=label(ol,acht=True); natbg=c==0
lijnen=[]
for i in range(1,n+1):
    vs,us=np.where(lab==i)
    if len(us)<5 or us.mean()<69 or vs.mean()<62: continue
    if np.mean([any(natbg[v_+dy,u+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))) for v_,u in zip(vs,us)])>0.5: continue   # selout langs de buitenrand, geen spiraallijn
    pts=sorted(set((int((u+0.5-U0)*S+X0),int((v_+0.5-V0)*S+Y0)) for v_,u in zip(vs,us)))
    lijnen.append(pts)
for pts in lijnen:
    P=set(pts)
    for X,Y in sorted(P):   # hoekpixels weg: een pixel met een horizontale én verticale lijnburen is overbodig (1-px lijn)
        h=[(X+dx,Y) for dx in (-1,1) if (X+dx,Y) in P]; vv=[(X,Y+dy) for dy in (-1,1) if (X,Y+dy) in P]
        if h and vv and len(P)>2:
            Q=P-{(X,Y)}; 
            # alleen weghalen als de lijn 8-samenhangend blijft
            st=[next(iter(Q))]; gez={st[0]}
            while st:
                x_,y_=st.pop()
                for dx in (-1,0,1):
                    for dy in (-1,0,1):
                        q=(x_+dx,y_+dy)
                        if q in Q and q not in gez: gez.add(q); st.append(q)
            if gez==Q: P=Q
    for X,Y in P:
        if o[Y,X] not in (0,1): o[Y,X]=2
# b) r2: per segment (vlak tussen twee spiraallijnen) schaduw onder/links -> midden -> licht bovenop; geen band die lijnen kruist.
#    t = dwars over de kegel (0 onder/links, 1 boven/rechts), u = langs de as binnen het segment (0 = lijn aan de lijfkant, 1 = lijn aan de puntkant).
#    De spiraal loopt in het model niet tot de rechterrand door (de windingen hangen daar aan elkaar); om per winding te kunnen
#    kleuren wordt elke lijn alleen vóór het indelen (niet getekend) in zijn eigen richting verlengd tot de buitenlijn.
grens=np.zeros((64,64),bool)
for pts in lijnen:
    P=sorted(pts); e=np.array(P[-1],float); p=np.array(P[max(0,len(P)-4)],float); r=(e-p)/max(np.linalg.norm(e-p),1e-9)
    q=e.copy()
    for _ in range(8):
        q=q+r*0.5; X,Y=int(round(q[0])),int(round(q[1]))
        if not boor[Y,X] or o[Y,X] in (0,1): break
        if o[Y,X]==4: grens[Y,X]=True
vul=boor&(o==4)&~grens; lab_s,ns=label(vul,acht=False)
for i in range(1,ns+1):
    m=lab_s==i; ys,xs=np.where(m)
    sl={}
    for Y,X in zip(ys,xs):
        b_=int(round(nn@[X,Y])); a_=dd@[X,Y]; lo,hi=sl.get(b_,(1e9,-1e9)); sl[b_]=(min(lo,a_),max(hi,a_))
    for Y,X in zip(ys,xs):
        lo,hi=sl_kegel[int(round(dd@[X,Y]))]; t=(nn@[X,Y]-lo)/max(hi-lo,1e-9)
        alo,ahi=sl[int(round(nn@[X,Y]))]; u=(dd@[X,Y]-alo)/max(ahi-alo,1e-9) if ahi>alo else 0.5
        if t<0.36 or (u>0.7 and t<0.6): o[Y,X]=3
        elif t>=0.52 and t<0.86 and u<0.5: o[Y,X]=5
        else: o[Y,X]=4
for Y,X in zip(*np.where(grens)):   # verlengstukjes nemen de tint van de winding erboven (lijfkant) aan
    nb=[o[Y+dy,X+dx] for dy,dx in ((-1,0),(0,-1),(-1,-1),(0,1),(1,0)) if o[Y+dy,X+dx] in (3,4,5) and not grens[Y+dy,X+dx]]
    if nb: o[Y,X]=nb[0]
bo=o.copy(); ontkorrel(o); o[~boor]=bo[~boor]   # tintvlekjes < 3 px in de boor weg
stap('boor (kleur)',v,o)

# --- 6. volume lijf (kleur, geen vorm): het model is op het lijf één vlak middengeel; r2: gebogen hooglicht op de rugbolling (zie onder). ---
v=o.copy()
da=np.array([26,20.]); da/=np.linalg.norm(da); na=np.array([da[1],-da[0]])   # na wijst naar de rug (rechtsboven)
lijf=np.zeros((64,64),bool)
for Y in range(14,46):
    for X in range(18,56):
        if o[Y,X] in GEEL|BLAUW and not boor[Y,X] and X>=24: lijf[Y,X]=True
# r2: geen rechte band. Hooglicht volgt de bolling van de rug: per rij 2-3 px links van de blauwe rugband (dus evenwijdig aan
#     de modelrand), alleen bovenaan de romp tussen kop en vleugels (rij 20-26), smal aan de uiteinden.
for Y,w in ((20,1),(21,2),(22,2),(23,2),(24,2),(25,1),(26,1)):
    xb=next(X for X in range(26,40) if o[Y,X] in BLAUW)
    for X in range(xb-2-w+1,xb-1) if w>1 else (xb-2,):
        if o[Y,X]==4: o[Y,X]=5
bo=o.copy(); ontkorrel(o); o[~lijf]=bo[~lijf]
stap('volume lijf (kleur)',v,o)

NAAM=UIT+'/dundragoon_r2.png'
opslaan(o,NAAM); toon(o,0,64,0,64)
print('stappen',tel); print('totaal anders dan kaal: %d px'%(o!=kaal).sum(),'| kleuren (excl. transp.)',len(set(o.ravel()))-1,'| figuur px',(o>0).sum())
yy,xx=np.where(o>0); print('bbox x%d-%d y%d-%d'%(xx.min(),xx.max(),yy.min(),yy.max()))
