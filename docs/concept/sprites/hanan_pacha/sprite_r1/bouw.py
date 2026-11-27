# Hanan Pacha r1: model r7 overnemen, kleuren r5. Natief raster 161x161 (pitch 6,40), figuur 138x154 -> 56x63.
# Kale reductie:
#  - figuur = spritepixel met >= 50 % niet-achtergrond (omlijning telt mee);
#  - vlakkleur = grootste vlakgroep (zonder omlijning), tint uit de gemiddelde r7-helderheid van die groep (r5-tinten);
#  - lijnen = elke spritepixel waar het middelpunt van een natieve omlijningspixel in valt (modellijnen punt voor punt
#    overgezet, zodat ze samenhangend blijven) en die >= LMIN omlijning heeft.
# Vingerpennen (r7 goud tussen witte band en donkere punt) krijgen r5-pennenkleuren oranje -> karmijn (gereedschap/pennen.py).
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen; from pennen import pennen; from gemeen import *
a,c,L=klassen('natief_r7.png')
pk,_=pennen(c)
c=c.copy(); c[pk==1]=6; c[pk==2]=7          # 6 oranje pen, 7 karmijn pen
LMIN=float(sys.argv[1]) if len(sys.argv)>1 else 0.25
def tint(g,l):
    if g==3: return 8 if l<66 else 9 if l<100 else 10              # kop/kam
    if g==4: return 2 if l<118 else 3 if l<156 else 4 if l<188 else 5   # goud
    if g==5: return 6 if l<214 else 7                               # wit
    if g==6: return 11 if l<156 else 12                             # oranje pen
    if g==7: return 8 if l<156 else 9                               # karmijn pen (r7-schaduw -> donker)
    if g==2: return 13                                              # donkere punt
BGW=float(sys.argv[3]) if len(sys.argv)>3 else 0.35
TP=float(sys.argv[4]) if len(sys.argv)>4 else 0.35
# veerzones (spritecoordinaten): vleugels buiten het lijf en de staart; daar wint achtergrond (ruimte tussen de pennen) eerder
veer=np.zeros((64,64),bool); veer[:,:]=True
o=np.zeros((64,64),int); fl=np.zeros((64,64))
for Y in range(64):
    for X in range(64):
        f=np.zeros(8); lum=np.zeros(8)
        for u,v,w in overlap(X,Y):
            if 0<=u<c.shape[1] and 0<=v<c.shape[0]:
                k=c[v,u]; f[k]+=w; lum[k]+=w*L[v,u]
        fl[Y,X]=f[1]
        bgw=BGW if veer[Y,X] else 0.5
        if f[2]>=TP: o[Y,X]=13; continue      # donkere penpunt wint vanaf TP (dikte van de punten uit het model)
        if f[0]>=bgw: continue
        if f[2:].sum()==0: o[Y,X]=1; continue
        g=2+int(np.argmax(f[2:]))
        o[Y,X]=tint(g,lum[g]/f[g])
        if g==3:   # kop/kam: de roze bulten (licht) en donkere plooien uit het model houden: licht wint vanaf 38 %, donker vanaf 45 %
            fl_=fd_=0
            for u,v,w in overlap(X,Y):
                if 0<=u<c.shape[1] and 0<=v<c.shape[0] and c[v,u]==3:
                    fl_+=w*(L[v,u]>=100); fd_+=w*(L[v,u]<66)
            if fl_>=0.38: o[Y,X]=10
            elif fd_>=0.45: o[Y,X]=8
# lijnen punt voor punt
lijn=np.zeros((64,64),bool)
for v,u in zip(*np.where(c==1)):
    X=int(np.floor(OX+(u+0.5-NX0)*S)); Y=int(np.floor(OY+(v+0.5-NY0)*S))
    if 0<=X<64 and 0<=Y<64: lijn[Y,X]=True
lijn&=(fl>=LMIN)&(o>0)
o[lijn&(o!=13)]=1
opslaan(o,'kaal.png'); np.save('kaal.npy',o)
print('figuur px',(o>0).sum(),'lijn',(o==1).sum())
if len(sys.argv)>2 and sys.argv[2]=='kaal': sys.exit()

# ---------------- staart: veren langs de modelassen ----------------
# De reductie maakt van de 9 staartveren (1,3-2 px per veer bij de wortel) een streepjesrommel. Reparatie naar het model:
# elke staartveer = de as van zijn donkere modelpunt (PCA, gereedschap/staart in dit blok), van de buitenpunt naar binnen tot Y=46.
# Spritepixel (Y>=STY) binnen 0,9 px van een as = veer: punt (13) over de gemeten puntlengte, anders goud/wit met de
# modelhelderheid; tussen twee veren: achtergrond als het model daar >= 50 % leeg is, anders goud-donker (2) als scheidingslijn.
STY=49
def staartassen():
    lab,n=ndimage.label(c==2,structure=np.ones((3,3))); uit=[]
    for i in range(1,n+1):
        ys,xs=np.where(lab==i)
        if len(ys)<4 or ys.mean()<=100: continue
        P=np.stack([xs,ys],1).astype(float); m=P.mean(0); _,_,vt=np.linalg.svd(P-m); d=vt[0]
        if d[1]>0: d=-d
        pr=(P-m)@d; buiten=m+d*pr.min(); binnen=m+d*pr.max()
        sp=lambda p:np.array([OX+(p[0]+0.5-NX0)*S,OY+(p[1]+0.5-NY0)*S])
        B=sp(buiten); I=sp(binnen); uit.append((B,d,np.linalg.norm(I-B)+0.6))
    return uit
from scipy import ndimage
assen=staartassen(); v_staart=o.copy()
for Y in range(STY,64):
    for X in range(64):
        P=np.array([X+0.5,Y+0.5]); ds=[]
        for B,d,tl in assen:
            w=P-B; s_=w@d; perp=abs(w@np.array([-d[1],d[0]]))
            if s_<-0.6 or B[1]+d[1]*s_<46: perp=99
            ds.append((perp,s_,tl))
        ds.sort(key=lambda t:t[0]); d1,s_,tl=ds[0]
        f=np.zeros(8); lum=np.zeros(8)
        for u,v,w in overlap(X,Y):
            if 0<=u<c.shape[1] and 0<=v<c.shape[0]: k=c[v,u]; f[k]+=w; lum[k]+=w*L[v,u]
        if d1<=0.9:
            if s_<=tl: o[Y,X]=13
            elif f[5]>=0.35: o[Y,X]=7
            else:
                lg=lum[4]/f[4] if f[4]>0 else 170
                o[Y,X]=3 if lg<156 else 4
        elif f[0]>=0.35 or d1>3: o[Y,X]=0
        else: o[Y,X]=2
np.save('staart_kaal.npy',o)
print('staart: anders dan kale reductie',int((o!=v_staart).sum()))

# ---------------- poten: klauwen en tenen uit het model, met "donkerste wint" ----------------
# In de pootzones valt de reductie uiteen in bruine blokken. Opnieuw uit het model: lijn wint vanaf 30 %, licht/klauw (wit) vanaf 30 %,
# achtergrond vanaf 50 %, anders goud met modelhelderheid. Lijnen hier = goud-donker (2) binnen, zwart aan de rand (stap buitenlijn).
POOTZONES=[(19,44,28,49),(29,43,38,48)]   # x0,y0,x1,y1 (exclusief)
v_poot=o.copy()
for x0,y0,x1,y1 in POOTZONES:
    for Y in range(y0,y1):
        for X in range(x0,x1):
            f=np.zeros(8); lum=np.zeros(8)
            for u,v,w in overlap(X,Y):
                if 0<=u<c.shape[1] and 0<=v<c.shape[0]: k=c[v,u]; f[k]+=w; lum[k]+=w*L[v,u]
            if f[0]>=0.5: o[Y,X]=0
            elif f[1]>=0.30: o[Y,X]=1
            elif f[5]>=0.30: o[Y,X]=7 if lum[5]/f[5]>=214 else 6
            elif f[4]>0: o[Y,X]=tint(4,lum[4]/f[4])
pootdiff=int((o!=v_poot).sum()); print('poten: anders dan reductie',pootdiff)

# ---------------- technische opschoning (elke stap geteld) ----------------
from scipy import ndimage
tel={}
def stap(n,v): tel[n]=tel.get(n,0)+int((v!=o).sum())
GRP={2:'g',3:'g',4:'g',5:'g',6:'w',7:'w',8:'r',9:'r',10:'r',11:'o',12:'o',13:'p'}
DONKER={'g':2,'w':6,'r':8,'o':11,'p':13}
N4=((-1,0),(1,0),(0,-1),(0,1))
def nb(o,Y,X,d=N4): return [o[Y+dy,X+dx] if 0<=Y+dy<64 and 0<=X+dx<64 else 0 for dy,dx in d]
N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
# 1. binnenlijnen: modellijn die niet aan de achtergrond grenst -> donkerste tint van de groep ernaast (goud wint bij gelijkspel)
v=o.copy()
for Y,X in zip(*np.where(v==1)):
    n8=nb(v,Y,X,N8)
    if 0 in n8: continue
    gs=[GRP[k] for k in n8 if k in GRP and k!=13]
    if not gs: continue
    tel_g={g:gs.count(g) for g in set(gs)}; best=max(tel_g.values())
    g='g' if tel_g.get('g',0)==best else max(tel_g,key=tel_g.get)
    o[Y,X]=DONKER[g]
stap('binnenlijnen',v)
# 2. buitenlijn: schaduwkant (achtergrond rechts/onder) zwart, lichtkant (alleen links/boven) selout in de donkerste eigen tint.
#    1-px-brede delen (achtergrond aan twee overliggende kanten) en donkere penpunten blijven.
v=o.copy()
for Y,X in zip(*np.where(v>0)):
    k=v[Y,X]
    if k==13: continue
    u,d,l,r=nb(v,Y,X)
    if not(0 in (u,d,l,r)): continue
    if (l==0 and r==0) or (u==0 and d==0):
        continue
    if r==0 or d==0: o[Y,X]=1
    else:
        if k==1:
            gs=[GRP[q] for q in nb(v,Y,X,N8) if q in GRP and q!=13]
            o[Y,X]=DONKER[max(set(gs),key=gs.count)] if gs else 1
        else: o[Y,X]=DONKER[GRP[k]]
stap('buitenlijn',v)
# 3. ontkorrelen: tintvlekjes < 3 px (licht < 2) -> meest voorkomende buurtint van dezelfde groep (lijntinten niet)
def ontkorrel():
    for k,minim in ((3,3),(4,3),(5,2),(7,3),(9,3),(10,2),(12,2)):
        lab,n=ndimage.label(o==k)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=minim: continue
            bu=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in N4 if 0<=Y+dy<64 and 0<=X+dx<64
                and GRP.get(o[Y+dy,X+dx])==GRP[k] and o[Y+dy,X+dx] not in (k,DONKER[GRP[k]])]
            if bu: o[m]=max(set(bu),key=bu.count)
v=o.copy(); ontkorrel(); ontkorrel(); stap('ontkorrelen',v)
# 4. losse zwarte pixel midden in een vlak -> buurtint
v=o.copy()
for Y,X in zip(*np.where(v==1)):
    n8=nb(v,Y,X,N8)
    if 0 not in n8 and 1 not in n8 and 13 not in n8:
        n4=nb(v,Y,X); o[Y,X]=max(set(n4),key=n4.count)
stap('losse zwarte pixels',v)
np.save('schoon.npy',o); opslaan(o,'schoon.png')
# ---------------- met de hand, naar het model (r7 origineel gemeten) ----------------
HAND={'oog':  {(21,20):1,(22,20):7,(21,19):8,(22,19):8},
      'kopgrens':{(16,18):2,(16,19):2},               # modellijn kop/vleugel (x 16,85 in het model, L112) als goud-donker binnenlijn   # oogwit orig x365-370,y339-351 -> (22,20); pupil links ervan; wenkbrauwlijn erboven
      'snavel':{(18,22):7,(17,23):7,(18,23):7,(17,24):14,(18,24):14,(19,23):1,(17,22):2,(16,23):2,(16,24):2},  # ivoor snavel (model 238,234,222 / 202,191,150), lijn rechts; modellijn links/boven (l1-l2 in het model) als goud-donker
      'klauw links':{(23,47):7,(23,48):1}}                 # roomkleurige klauw van de linkerpoot (model w5l4) + punt
for zone,d in HAND.items():
    n=0
    for (X,Y),k in d.items():
        if o[Y,X]!=k: n+=1
        o[Y,X]=k
    tel['hand '+zone]=n
opslaan(o,'sprite.png'); np.save('sprite.npy',o)
print(tel)
