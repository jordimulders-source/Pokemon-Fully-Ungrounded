# Guarana fase 1, r1: model overnemen. Natief raster 99x99 (pitch 10,24; figuur 71x60) -> schaal 44/71 (0,620), figuur x10-53, y15-51.
# Verkleinen = oppervlakteweging per spritepixel over het natieve raster; dunne modellijnen winnen vanaf een drempel.
import sys, os, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen; from gemeen import *
a,c,L=klassen()
VAR=os.environ.get('VARIANT','')   # '' hoofdversie | 'zonder_puntjes' | 'ogen_groter'
# zwarte puntjes aan de vruchtpunten (natief, gemeten: zwart met >= 4 achtergrondburen dat buiten de vruchtrand uitsteekt)
PUNTJES=[(30,19),(31,19),(22,26),(22,27),(14,38),(24,53),(25,53),(47,30),(48,30)]
if VAR=='zonder_puntjes':
    for u,v in PUNTJES: c[v,u]=0
UIT='sprite_r1'
TK=0.30   # zwart wint vanaf 30 % oppervlak
TW=0.30   # oogwit wint van rood vanaf 30 %
TKG=float(os.environ.get('TKG','0.30'))   # zwart in groen gebied (ranken)
def tn(g,l):
    if g==2: return 2 if l<72 else 3 if l<100 else 4 if l<140 else 5
    if g==3: return 6 if l<80 else 7 if l<118 else 8 if l<145 else 9
    if g==4: return 10 if l>=215 else 11
o=np.zeros((64,64),int)
for Y in range(64):
    for X in range(64):
        f=np.zeros(5); lum=np.zeros(5)
        for u,v,w in overlap(X,Y):
            k=c[v,u]; f[k]+=w; lum[k]+=w*L[v,u]
        if f[1:].sum()<0.5: continue
        if f[1]>=(TKG if f[3]>f[2] else TK): o[Y,X]=1; continue
        if f[4]>=TW: o[Y,X]=tn(4,lum[4]/f[4]); continue
        g=2+int(np.argmax(f[2:]))
        o[Y,X]=tn(g,lum[g]/f[g])
kaal=o.copy(); opslaan(kaal,UIT+'/kaal.png')
if len(sys.argv)>1 and sys.argv[1]=='kaal':
    toon(o,10,56,4,60); sys.exit()

tel={}
def stap(n,v,o): tel[n]=tel.get(n,0)+int((v!=o).sum())
SEL={**{k:2 for k in ROOD},**{k:6 for k in GROEN}}
GRP={**{k:ROOD for k in ROOD},**{k:GROEN for k in GROEN},**{k:WIT for k in WIT}}
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]

# --- 1. ogen uit het model: per spritepixel de dekking van de modelpupil (zwart binnen het oogwit) en het modeloogwit.
#        pupil >= 40 % -> zwart; anders oogwit >= 40 % -> wit. Verder niets (geen glans; oogvorm = model). ---
from ogen import dekking, PUPIL
v=o.copy(); OOG=np.zeros((64,64),bool); PUP=np.zeros((64,64),bool)
for n in PUPIL:
    for (X,Y),(fp,fw) in dekking(n).items():
        if fp>=0.40: o[Y,X]=1; OOG[Y,X]=PUP[Y,X]=True
        elif fw>=0.40: o[Y,X]=10; OOG[Y,X]=True
stap('ogen (uit model)',v,o)
if VAR=='ogen_groter':
    # variant: elk oog = het nabije oog van Weepinbell (graphics/pokemon/weepinbell/anim_front_gba.png, x26-32 y34-40), pixel voor pixel:
    # O = Weepinbells ooglid/lichtkantlijn (index 2, bruin) -> onze donkerrood 2; W = wit 1 -> 10; K = zwart f -> 1. Weepinbells gezichtswit linksboven (x26-27,y34; x26,y35) hoort niet bij het oog.
    WEEP=['..OOO..',
          '.OWWWK.',
          'OWWWWWK',
          'OWKKWWK',
          'OWKKWWK',
          '.KWWWK.',
          '..KKK..']
    # oorsprong zo dat de 2x2-pupil op de modelpupil valt; rechteroog 1 px naar links zodat het binnen het silhouet blijft
    v=o.copy(); NIEUW=np.zeros((64,64),bool); NP=np.zeros((64,64),bool)
    for x0,y0 in ((16,17),(24,19),(14,27)):
        for dy,rij in enumerate(WEEP):
            for dx,ch in enumerate(rij):
                if ch=='.': continue
                o[y0+dy,x0+dx]={'O':2,'W':10,'K':1}[ch]; NIEUW[y0+dy,x0+dx]=True; NP[y0+dy,x0+dx]=(ch=='K' and 2<=dx<=3 and 3<=dy<=4)
    # oude modeloogpixels buiten de nieuwe ogen -> rood midden (vrucht)
    for Y,X in zip(*np.where(OOG&~NIEUW)): o[Y,X]=4
    OOG=NIEUW; PUP=NP
    stap('ogen groter (Weepinbell)',v,o)

# --- 2. binnenlijnen: zwart dat niet aan de achtergrond grenst en geen pupil/oogrand is, wordt de donkerste eigen tint
#        van het vlak waar het in ligt (Gen 3: zwart alleen op de buitenlijn). Rood raster tussen de vruchten -> donkerrood,
#        lijnen waar ranken over de rank vallen -> donkergroen. Zwart dat aan oogwit grenst blijft zwart (oogcontour, zoals het model). ---
v=o.copy()
def binnenlijnen(o):
    fg=o>0; uit=[]
    for Y,X in zip(*np.where(o==1)):
        if PUP[Y,X]: continue
        if any(not fg[Y+dy,X+dx] for dy,dx in N4): continue
        if any(o[Y+dy,X+dx] in WIT for dy,dx in N4): continue
        r=sum(o[Y+dy,X+dx] in ROOD for dy,dx in N8); g=sum(o[Y+dy,X+dx] in GROEN for dy,dx in N8)
        uit.append((Y,X,2 if r>=g else 6))
    for Y,X,k in uit: o[Y,X]=k
binnenlijnen(o); stap('binnenlijnen (zwart -> eigen donker)',v,o)

# --- 3. buitenlijn: geen open of lichte rand. Achtergrond rechts/onder = zwart (schaduwkant); lichtkant = selout van de groep. Zwart blijft zwart. ---
def rand(o):
    fg=o>0; uit=[]
    for Y,X in zip(*np.where(fg)):
        k=o[Y,X]
        if k==1 or k in WIT: continue
        bgL=not fg[Y,X-1]; bgR=not fg[Y,X+1]; bgU=not fg[Y-1,X]; bgD=not fg[Y+1,X]
        if not(bgL or bgR or bgU or bgD): continue
        n=1 if (bgR or bgD) else SEL[k]
        if n!=k: uit.append((Y,X,n))
    for Y,X,k in uit: o[Y,X]=k
v=o.copy(); rand(o); stap('buitenlijn',v,o)
# --- 3b. zwart van het model op de lichtkant van de buitenlijn (achtergrond alleen boven/links) -> selout van de groep
#         (Gen 3: zwart alleen aan de schaduwkant). Niet: pupillen, oogcontour, en de zwarte puntjes aan de vruchtpunten (blijven zoals het model). ---
PUNT=np.zeros((64,64),bool)
for Y in range(64):
    for X in range(64):
        if sum(w for u,v_,w in overlap(X,Y) if (u,v_) in PUNTJES)>=0.15: PUNT[Y,X]=True
v=o.copy(); fg=o>0; uit=[]
for Y,X in zip(*np.where(o==1)):
    if OOG[Y,X] or PUNT[Y,X] or any(o[Y+dy,X+dx] in WIT for dy,dx in N4): continue
    bgL=not fg[Y,X-1]; bgR=not fg[Y,X+1]; bgU=not fg[Y-1,X]; bgD=not fg[Y+1,X]
    if not (bgL or bgU) or bgR or bgD: continue
    r=sum(o[Y+dy,X+dx] in ROOD for dy,dx in N8); g=sum(o[Y+dy,X+dx] in GROEN for dy,dx in N8)
    uit.append((Y,X,2 if r>g else 6))
for Y,X,k in uit: o[Y,X]=k
stap('lichtkant zwart -> selout',v,o)

# --- 4. ontkorrelen: tintvlekjes < 3 px (hooglicht < 2) nemen de meest voorkomende buurtint van dezelfde groep aan (lijntinten 2/6 niet) ---
def ontkorrel(o):
    for k,minim in ((3,3),(4,3),(5,2),(7,3),(8,3),(9,2)):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=minim: continue
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in N4 if o[Y+dy,X+dx] in GRP[k] and o[Y+dy,X+dx]!=k and o[Y+dy,X+dx]!=SEL[k]]
            if buur: o[m]=max(set(buur),key=buur.count)
v=o.copy(); ontkorrel(o); ontkorrel(o); stap('ontkorrelen',v,o)

# --- 5. losse zwarte pixel midden in een vlak (geen zwarte 8-buur, geen achtergrond, geen pupil) -> buurtint ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    if OOG[Y,X]: continue
    nb=[o[Y+dy,X+dx] for dy,dx in N4]; nb8=[o[Y+dy,X+dx] for dy,dx in N8]
    if 0 not in nb8 and 1 not in nb8 and not any(k in WIT for k in nb8): o[Y,X]=max(set(nb),key=nb.count)
stap('losse zwarte pixels',v,o)

NAAM=sys.argv[1] if len(sys.argv)>1 else UIT+'/guarana_r1.png'
opslaan(o,NAAM); toon(o,12,54,6,58)
print('stappen',tel); print('totaal anders dan kaal: %d px'%(o!=kaal).sum(),'| kleuren (excl. transp.)',len(set(o.ravel()))-1,'| figuur px',(o>0).sum())
yy,xx=np.where(o>0); print('bbox x%d-%d y%d-%d (%dx%d)'%(xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1))
