# Mightyena-evolutie r2: alleen kleur binnen het silhouet van r1 (alpha-diff 0, lijnen blijven). Basis = r1; metingen op het model
# op spriteschaal (natief raster met dezelfde rijen/kolommen geschrapt als de kale reductie). Bouwen: cd mightyena_evo && python3 sprite_r2/bouw.py
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *; from schrap import schrap
UIT='sprite_r2'
r1=np.asarray(Image.open('sprite_r1/mightyena_evo_r1.png')).astype(int); kaal=np.asarray(Image.open('sprite_r1/kaal.png')).astype(int)
o=r1.copy()
a,c,L=klassen(); s,rows,cols,_,_=schrap(c); Ls=np.delete(np.delete(L,rows,0),cols,1); H,W=s.shape
ML=np.full((64,64),-1.); ML[Y0:Y0+H,X0:X0+W]=np.where(s>0,Ls,-1)       # modelhelderheid per spritepixel
MC=np.zeros((64,64),int); MC[Y0:Y0+H,X0:X0+W]=s                         # modelklasse per spritepixel
N4=((-1,0),(1,0),(0,-1),(0,1)); P=lambda q:np.pad(q,1)
tel={}
def stap(n,v): tel[n]=tel.get(n,0)+int((v!=o).sum())
def box(x0,x1,y0,y1):
    m=np.zeros((64,64),bool); m[y0:y1+1,x0:x1+1]=True; return m
dk=np.isin(o,(1,2,3,4)); lab,n=label(dk,acht=False); GROOT=np.zeros((64,64),bool)
for i in range(1,n+1):
    if (lab==i).sum()>40: GROOT|=lab==i
FUR=GROOT&np.isin(o,(2,3,4))                              # zwarte vacht = grote donkere massa (geen vlekken op het lijf)
# zones (vacht)
VP=box(22,33,47,61)&FUR; MP=box(37,42,43,56)&FUR; AP=box(48,57,46,58)&FUR
OP=box(3,14,27,47)&FUR                                   # opgeheven poot
SN=box(0,14,17,28)&np.isin(o,(2,3,4))                    # snuit (vachttinten in de kop onder de ogen)
MA=FUR&~VP&~MP&~AP&~OP&~SN&box(14,63,4,47)&~box(0,19,0,30)               # manen + nek + staart

# --- 8. opgeheven poot: model even donker als de andere poten (mediaan L 41 vs 38-41; zie NOTITIES) -> zelfde tinten als de poten:
#        basis 2, modelpixels D (L>=46) -> 3; lichtkant volgt hieronder in stap 2 ---
v=o.copy()
for Y,X in zip(*np.where(OP)): o[Y,X]=3 if ML[Y,X]>=46 and MC[Y,X]==3 else 2
stap('opgeheven poot: donker als de poten (meting)',v)

# --- 7. snuit één tint donkerder (model: zwartste deel van de kop): 3->2, 4->3; vorm, neusgat, bek, tanden blijven ---
v=o.copy()
for Y,X in zip(*np.where(SN)): o[Y,X]={2:2,3:2,4:3}[o[Y,X]]
stap('snuit donkerder',v)

# --- 1. manen: strengen uit het model. Donker/middengrijze modelpixels (D, L>=46) worden in de haarrichting (kop -> staart, langs de
#        rug (43,37), voorin steiler (1,1.6), achterin vlakker (1,0.5)) samengevoegd met een lijnfilter van 5 px; streng = D-pixel met
#        >=2 D op de lijn, of tussenpixel met >=3, en minstens 3 px groot.
#        Streng 3; de lichtkant (bovenrand) van een streng van >=4 px -> 4 (samenhangend, >=2 px). Wat geen streng vormt: buurtint 2. ---
v=o.copy()
D=MA&(MC==3)&(ML>=46)
sc=np.zeros((64,64),int)
for dd in ((43.,37.),(1.,1.6),(1.,0.5)):        # haarrichting: langs de rug, voorin steiler omlaag, achterin vlakker; per pixel de beste
    d=np.array(dd); d/=np.linalg.norm(d); s1=np.zeros((64,64),int)
    for Y,X in zip(*np.where(MA)):
        for t in (-2,-1,0,1,2):
            xx=int(round(X+t*d[0])); yy=int(round(Y+t*d[1]))
            if 0<=xx<64 and 0<=yy<64 and D[yy,xx]: s1[Y,X]+=1
    sc=np.maximum(sc,s1)
st=MA&((D&(sc>=2))|(sc>=3))
lab,n=label(st,acht=True)
for i in range(1,n+1):
    if (lab==i).sum()<3: st[lab==i]=False
for Y,X in zip(*np.where(MA)): o[Y,X]=3 if st[Y,X] else 2
# lichtkant: strengpixel met boven (of rechtsboven) een donkere vachtpixel en streng-lengte >=4
lab,n=label(st,acht=True)
hl=np.zeros((64,64),bool)
for i in range(1,n+1):
    m=lab==i
    if m.sum()<4: continue
    for Y,X in zip(*np.where(m)):
        if o[Y-1,X]==2 or o[Y-1,X]==1: hl[Y,X]=True
lab,n=label(hl,acht=True)
for i in range(1,n+1):
    if (lab==i).sum()>=2: o[lab==i]=4
stap('manen: strengen uit het model',v)

# --- 2. zwarte poten: lichtkant (voorkant/links) in tint 3 die de poot volgt. Per rij de eerste vachtpixel(s) rechts van de linkerlijn;
#        2 px breed waar de poot >= 6 px breed is, anders 1. Klauwen/tenen (lichte modelpixels onderaan) blijven. ---
v=o.copy()
for Z in (VP,MP,AP,OP):
    for Y in range(64):
        xs=[X for X in range(64) if Z[Y,X]]
        if not xs: continue
        x0=xs[0]
        if o[Y,x0-1]!=1 and o[Y,x0-1]!=0: continue          # geen lijn links: binnenkant, geen lichtkant
        w=2 if len(xs)>=6 else 1
        for X in range(x0,x0+w):
            if Z[Y,X] and o[Y,X]==2: o[Y,X]=3
stap('poten: lichtkant',v)

# --- 3. volume lijf: geen band langs de manen maar een bolling op schouder, rug en dij. r1-hooglicht (7) eerst terug naar 6; dan 7 in
#        een ellips per bolling, minstens 2 px van de bovenrand (manen/lijn) en alleen op 6. ---
v=o.copy()
o[(o==7)&~box(0,22,0,30)]=6
BOL=[(18,33,3.2,3.0),(33,31,4.6,2.0),(46,35,3.2,2.6)]
f=o>0
for cx,cy,rx,ry in BOL:
    for Y in range(64):
        for X in range(64):
            if o[Y,X]!=6 or ((X-cx)/rx)**2+((Y-cy)/ry)**2>1: continue
            if any(o[Y-k,X] in (0,1,2,3,4) and not (o[Y-k,X]==2 and not FUR[Y-k,X]) for k in (1,2)): continue
            o[Y,X]=7
lab,n=label(o==7,acht=False)
for i in range(1,n+1):
    if (lab==i).sum()<3 and not box(0,22,0,30)[lab==i].any(): o[lab==i]=6
stap('lijf: hooglicht als bolling',v)

# --- 4. losse 1-px vlekjes op het lijf: modelcluster >=3 px -> 2-3 px op de modelplek (pixels van het cluster die de schrapping overleefden
#        of de buurpixel naar het clusterzwaartepunt), anders buurtint ---
v=o.copy()
kr=[i for i in range(c.shape[0]) if i not in rows]; kk=[i for i in range(c.shape[1]) if i not in cols]
nl,_n=label(np.isin(c,(1,2)),acht=False)
for X,Y in [(44,30),(14,37),(16,37),(23,39),(24,40),(16,41),(49,44),(38,47)]:
    if o[Y,X]!=2: continue
    uu=kk[X-X0]; vv=kr[Y-Y0]; g=(nl==nl[vv,uu]).sum() if nl[vv,uu] else 0
    if g>=3:
        cy,cx=np.argwhere(nl==nl[vv,uu]).mean(0); dy,dx=np.sign(cy-vv),np.sign(cx-uu)
        for ddy,ddx in [(int(dy),0),(0,int(dx))] if abs(cy-vv)>=abs(cx-uu) else [(0,int(dx)),(int(dy),0)]:
            if (ddy or ddx) and o[Y+ddy,X+ddx] in (5,6,7): o[Y+ddy,X+ddx]=2; break
    else:
        nb=[o[Y+dy,X+dx] for dy,dx in N4 if o[Y+dy,X+dx] in (5,6,7)]
        if nb: o[Y,X]=max(set(nb),key=nb.count)
    print('vlek',(X,Y),'modelcluster',g)
stap('lijf: losse vlekjes',v)

# --- 5. kop: lichtkant in tint 7 (zoals Mightyena): voorhoofd/kruin en de binnenrand van de oren aan de lichtkant; alleen op 6,
#        ogen (y>=14), bek en tanden niet. ---
v=o.copy()
KG=box(0,21,2,13)&(o==6)          # alleen middengrijs: de donkere modeltekening (5) op de kop blijft
for Y,X in zip(*np.where(KG)):
    rand=any(o[Y+dy,X+dx]==4 for dy,dx in ((-1,0),(0,-1)))          # direct onder/rechts van de selout van oor/schedel
    kruin=((X-11)/3.6)**2+((Y-10)/1.7)**2<=1   # voorhoofd boven het nabije oog (daar is de kop middengrijs)
    if rand or kruin: o[Y,X]=7
lab,n=label((o==7)&box(0,21,2,13),acht=False)
for i in range(1,n+1):
    if (lab==i).sum()<3: o[lab==i]=6
stap('kop: lichtkant',v)

# --- 6. linkerrand bij de oorvoet (x0-1, y6-13): één soort rand, selout 4 (lichtkant) ---
v=o.copy()
for Y in range(6,14):
    for X in (0,1):
        if o[Y,X]==1 and (X==0 or o[Y,X-1]==0): o[Y,X]=4
stap('linkerrand oorvoet: selout',v)

# --- 9. opruimen: vachttintjes (3/4 samen, 8-samenhangend) < 3 px in manen, snuit en poten (tenen/klauwen onderaan uitgezonderd) -> 2;
#        grijze tintvlekjes < 3 px op de kop (na de lichtkant) -> buurtint ---
v=o.copy()
Z=(MA|SN|((VP|MP|AP|OP)&~box(0,63,53,63)))&np.isin(o,(3,4))
lab,n=label(Z,acht=True)
for i in range(1,n+1):
    if (lab==i).sum()<3: o[lab==i]=2
for _ in range(2):
    for k in (5,6,7):
        lab,n=label((o==k)&box(0,21,2,13),acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=3: continue
            for Y,X in np.argwhere(m):
                if any(o[Y+dy,X+dx]==0 for dy,dx in N4): continue
                nb=[o[Y+dy,X+dx] for dy,dx in N4 if o[Y+dy,X+dx] in (5,6,7) and o[Y+dy,X+dx]!=k]
                if nb: o[Y,X]=max(set(nb),key=nb.count)
stap('opruimen kleine tintjes',v)

assert ((o>0)==(r1>0)).all(), 'silhouet veranderd'
opslaan(o,UIT+'/mightyena_evo_r2.png')
print('per stap t.o.v. r1:'); [print('  %-46s %d'%(k,v)) for k,v in tel.items()]
print('anders dan r1:',int((o!=r1).sum()),'| anders dan kaal:',int((o!=kaal).sum()),'| alpha-diff met r1:',int(((o>0)!=(r1>0)).sum()))
if len(sys.argv)>1: toon(o)
