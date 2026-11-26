# Sneeuwmonster r1: model overnemen. Natief raster 99x99 (pitch 10,24; figuur 44x66) -> schaal 42/66 (0,636), figuur x18-45, y11-52.
# Verkleinen = oppervlakteweging per spritepixel over het natieve raster; dunne modellijnen winnen vanaf een drempel ("donkerste wint").
# Daarna alleen technische opschoning en reparaties naar het model; elke stap geteld.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen; from gemeen import *
a,c,L=klassen()
UIT='sprite_r1'
TK=0.30   # zwart wint vanaf 30 % oppervlak
TS=0.40   # steen wint vanaf 40 %
TB=0.30   # blauwe sneeuwlijn wint vanaf 30 %
TOOG=float(__import__("os").environ.get("TOOG","0.40"))   # oog: donkere modeldekking
def tw(l): return 3 if l<212 else 4 if l<236 else 5          # sneeuwtint uit de gemiddelde modelhelderheid
def ts(l): return 6 if l<72 else 7 if l<108 else 8           # steentint uit de gemiddelde modelhelderheid
def reductie():
    o=np.zeros((64,64),int)
    for Y in range(64):
        for X in range(64):
            f=np.zeros(5); lum=np.zeros(5)
            for u,v,w in overlap(X,Y):
                k=c[v,u]; f[k]+=w; lum[k]+=w*L[v,u]
            if f[1:].sum()<0.5: continue
            if f[1]>=TK: o[Y,X]=1
            elif f[2]>=TS: o[Y,X]=ts(lum[2]/f[2])
            elif f[3]>=TB: o[Y,X]=2
            else: o[Y,X]=tw(lum[4]/f[4]) if f[4] else 2
    return o
o=reductie(); kaal=o.copy(); opslaan(kaal,UIT+'/kaal.png')
if len(sys.argv)>1 and sys.argv[1]=='kaal':
    toon(o,8,56,14,50); sys.exit()

tel={}
def stap(n,v,o): tel[n]=tel.get(n,0)+int((v!=o).sum())
GRP={k:(SNEEUW if k in SNEEUW else STEEN) for k in range(2,9)}
# --- 1. buitenlijn: geen open of lichte rand. Achtergrond rechts/onder = zwart (schaduwkant), lichtkant = sneeuwlijn (selout),
#        zoals het model zelf (blauwe lijn links/boven, zwart rechts/onder). Zwart blijft zwart. ---
def rand(o):
    fg=o>0; uit=[]
    for Y,X in zip(*np.where(fg)):
        k=o[Y,X]
        if k==1: continue
        bgL=not fg[Y,X-1]; bgR=not fg[Y,X+1]; bgU=not fg[Y-1,X]; bgD=not fg[Y+1,X]
        if not(bgL or bgR or bgU or bgD): continue
        n=1 if (bgR or bgD) else 2
        if n!=k: uit.append((Y,X,n))
    for Y,X,k in uit: o[Y,X]=k
v=o.copy(); rand(o); stap('buitenlijn',v,o)
# --- 2. ontkorrelen: sneeuwtintvlekjes < 3 px (licht < 2) nemen de meest voorkomende buurtint van dezelfde groep aan (lijn 2 niet) ---
def ontkorrel(o,mask=None):
    for k,minim in ((3,3),(4,3),(5,2)):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=minim or (mask is not None and not (m&mask).any()): continue
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[Y+dy,X+dx] in (3,4,5) and o[Y+dy,X+dx]!=k]
            if buur: o[m]=max(set(buur),key=buur.count)
v=o.copy(); ontkorrel(o); ontkorrel(o); stap('ontkorrelen',v,o)
# --- 3. losse zwarte pixel midden in sneeuw (geen zwarte/steen-8-buur, geen achtergrond) -> buurtint ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    nb=[o[Y+dy,X+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
    nb8=[o[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
    if 0 not in nb8 and not any(q in (1,6,7,8) for q in nb8): o[Y,X]=max(set(nb),key=nb.count)
stap('losse zwarte pixels',v,o)

# --- 4. ogen naar het model: de reductie gaf twee grijze blokjes zonder glans (hooglicht viel weg in het gemiddelde).
#        Per spritepixel opnieuw uit het model: oog = donkere modeldekking (zwart+steen) >= 0,40; tint uit de gemiddelde
#        modelhelderheid van die donkere pixels (< 35 zwart, < 72 steen donker, anders steen midden).
#        Glans: het witte modelhooglicht in het oog (L >= 248) ligt linksboven in het oog; zijn zwaartepunt wordt naar de sprite
#        gemapt en de dichtstbijzijnde pixel binnen het oogvak (bbox van de ooggpixels) wordt licht (5).
#        Overige binnenpixels in het oogvak die steen/zwart waren -> sneeuwtint uit het model (buitenlijn blijft). ---
v=o.copy(); fg=o>0
for (x0,x1,y0,y1,nu0,nu1,nv0,nv1) in ((22,26,22,27,31,38,33,41),(29,34,22,28,44,51,33,42)):
    oog=[]
    for Y in range(y0,y1+1):
        for X in range(x0,x1+1):
            if any(not fg[Y+dy,X+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): continue
            fd=ld=fw=lw=0
            for u,v_,w in overlap(X,Y):
                k=c[v_,u]
                if k in (1,2): fd+=w; ld+=w*L[v_,u]
                elif k==4: fw+=w; lw+=w*L[v_,u]
            if fd>=TOOG: o[Y,X]=1 if ld/fd<35 else 6 if ld/fd<72 else 7; oog.append((X,Y))
            elif o[Y,X] in (1,6,7,8): o[Y,X]=tw(lw/fw) if fw else 4
    hv,hu=np.where((c==4)&(L>=248)); sel=(hu>=nu0)&(hu<=nu1)&(hv>=nv0)&(hv<=nv1)
    hx=(hu[sel].mean()+0.5-U0)*S+X0; hy=(hv[sel].mean()+0.5-V0)*S+Y0
    xs=[p[0] for p in oog]; ys=[p[1] for p in oog]
    kand=[(X,Y) for X in range(min(xs),max(xs)+1) for Y in range(min(ys),max(ys)+1)
          if sum((X+dx,Y+dy) in oog for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)))>=2]   # glans ligt ín het oog (>= 2 oogburen), niet op de snee-rand
    X,Y=min(kand,key=lambda p:(p[0]+0.5-hx)**2+(p[1]+0.5-hy)**2); o[Y,X]=5
    print('oog',sorted(oog),'glans model (%.1f,%.1f) -> (%d,%d)'%(hx,hy,X,Y))
stap('ogen (uit model)',v,o)

# --- 5. buitenlijn: geen zwart en sneeuwlijn om en om op één rand. Een losse sneeuwlijnpixel op de buitenrand waarvan alle
#        randburen zwart zijn (en geen randbuur sneeuwlijn) wordt zwart; het zwart zelf komt uit het model. ---
v=o.copy(); fg=o>0
opr=lambda Y,X: fg[Y,X] and any(not fg[Y+dy,X+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
for Y,X in zip(*np.where(o==2)):
    if not opr(Y,X): continue
    nb=[o[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and opr(Y+dy,X+dx)]
    if nb.count(1)>=2 and nb.count(2)==0: o[Y,X]=1
stap('buitenlijn om en om',v,o)

NAAM=UIT+'/sneeuwmonster_r1.png'
opslaan(o,NAAM); toon(o,8,56,14,50)
print('stappen',tel); print('totaal anders dan kaal: %d px'%(o!=kaal).sum(),'| kleuren (excl. transp.)',len(set(o.ravel()))-1,'| figuur px',(o>0).sum())
yy,xx=np.where(o>0); print('bbox x%d-%d y%d-%d'%(xx.min(),xx.max(),yy.min(),yy.max()))

# --- MONDVARIANTEN (apart; het model heeft geen mond). Mondpixels 1-op-1 overgenomen uit een Gen 3-sprite (_gba), alleen herkleurd:
#     tinten als stappen onder de huidtint van de bron -> dezelfde stappen onder onze gezichtstint (licht 5: 1 stap = 4, 2 stappen = 3;
#     een donkere accentkleur = sneeuwlijn 2). Plek: zelfde ligging t.o.v. de ogen als in de bron (midden tussen de ogen,
#     direct onder de onderkant van het laagste oog). ---
MONDEN={
  # Shroomish (graphics/pokemon/shroomish/anim_front_gba.png): ogen (26,28-29) en (32,28-29), mond (28,30) 3 · (29,30) 2 · (30,30) 3
  # op huid 4: tint 3 = 1 stap donkerder, tint 2 = 2 stappen -> onze 4 en 3. Midden tussen de ogen x=29, rij direct onder de ogen.
  'shroomish':[(-1,0,4),(0,0,3),(1,0,4)],
  # Chinchou (graphics/pokemon/chinchou/anim_front_gba.png): mond (31,36) en (31,37) in donkerrood 14 op huid 4, midden tussen de ogen,
  # direct onder de ogen; donkere accentkleur -> sneeuwlijn 2.
  'chinchou':[(0,0,2),(0,1,2)],
}
MX,MY=27,27   # midden tussen de oogmiddens (23 en 31) = x27; rij direct onder het laagste oog (rechteroog eindigt op y26) = y27
for n,px in MONDEN.items():
    m=o.copy()
    for dx,dy,k in px: m[MY+dy,MX+dx]=k
    opslaan(m,UIT+'/mond_%s.png'%n)
    d=[(int(X),int(Y),CH[o[Y,X]]+'>'+CH[m[Y,X]]) for Y,X in zip(*np.where(m!=o))]
    print('mond',n,'diff t.o.v. r1:',d)
