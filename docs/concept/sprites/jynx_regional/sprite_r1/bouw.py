# Regionale Jynx r1: model overnemen. Natief raster 99x99 (pitch 10,24; figuur 72x77) -> schaal 58/77 (0,753), figuur x5-59, y5-62.
# Verkleinen = oppervlakteweging per spritepixel over het natieve raster; dunne/kleine modeldelen winnen vanaf een drempel.
# Daarna alleen technische opschoning en reparaties naar het model; elke stap geteld.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen; from gemeen import *
a,c,L=klassen()
UIT='sprite_r1'
# modeltinten per groep (helderheidsdrempels gemeten op het histogram, zie NOTITIES)
def tn(g,l):
    if g==2: return 3 if l<125 else 4 if l<152 else 5          # veren: schaduw / midden / licht (lijn apart)
    if g==3: return 6 if l<80 else 7 if l<105 else 8           # haar: donker / schaduw / midden
    if g==4: return 9 if l<235 else 10                          # gezicht
    if g==5: return 11 if l<70 else 12                          # lippen
    if g==6: return 13
    if g==7: return 14
    if g==8: return 15
TK=0.30; TL=0.30; TKLEIN=0.30
o=np.zeros((64,64),int)
for Y in range(64):
    for X in range(64):
        f=np.zeros(9); lum=np.zeros(9); fl=0; fv=0; lv=0
        for u,v,w in overlap(X,Y):
            k=c[v,u]; f[k]+=w; lum[k]+=w*L[v,u]
            if k==2:
                if L[v,u]<95: fl+=w
                else: fv+=w; lv+=w*L[v,u]
        tot=f[1:].sum()
        if tot<0.5: continue
        if f[1]>=TK: o[Y,X]=1; continue
        klein=[k for k in (7,6,5,8) if f[k]>=TKLEIN]
        if klein: k=klein[0]; o[Y,X]=tn(k,lum[k]/f[k]); continue
        if fl>=TL and f[2]>=f[3:].max(): o[Y,X]=2; continue
        g=2+int(np.argmax(f[2:]))
        if g==2: o[Y,X]=tn(2,lv/fv) if fv>0 else 2
        else: o[Y,X]=tn(g,lum[g]/f[g])
kaal=o.copy(); opslaan(kaal,UIT+'/kaal.png')
if len(sys.argv)>1 and sys.argv[1]=='kaal':
    toon(o,0,64,0,64); print('figuur px',(o>0).sum()); sys.exit()

tel={}
def stap(n,v,o): tel[n]=tel.get(n,0)+int((v!=o).sum())
GROEP={**{k:'veer' for k in VEER},**{k:'haar' for k in HAAR},**{k:'gez' for k in GEZ},**{k:'lip' for k in LIP},14:'oog',15:'klauw'}
DONKER={'veer':2,'haar':6,'klauw':15}
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def buren(o,Y,X,nb=N8): return [o[Y+dy,X+dx] for dy,dx in nb if 0<=Y+dy<64 and 0<=X+dx<64]
def aan_bg(o,Y,X): return any(v==0 for v in buren(o,Y,X,N4))

# --- 1. binnenlijnen: zwart dat niet aan de achtergrond grenst wordt de donkerste eigen tint (Gen 3: binnenlijnen niet zwart).
#        Gezichtscontour (zwart dat aan gezicht én haar/veren grenst) -> haar donker, rondom gelijk. Zwart binnen het gezicht
#        (wimpers, mondopening) blijft zwart. Overige: donkerste tint van de groep met de meeste buren (gelijk -> haar). ---
v=o.copy()
for ronde in (1,2):          # 2e ronde: zwart dat alleen aan (inmiddels omgezette) contour grensde
  nieuw=[]
  for Y,X in zip(*np.where(o==1)):
    if aan_bg(o,Y,X): continue
    if (19<=X<=21 or 25<=X<=30) and 15<=Y<=17: continue   # wimpers/ooghoeken (oogvakken uit het model) blijven zwart
    nb=[GROEP[k] for k in buren(o,Y,X) if k>1]
    if not nb: continue
    gez=any(g in ('gez','lip','oog') for g in nb)
    rest=[g for g in nb if g in ('veer','haar')]
    if gez and not rest: continue                      # wimper / mond: blijft zwart
    if gez: nieuw.append((Y,X,6)); continue           # gezichtscontour
    nv=rest.count('veer'); nh=rest.count('haar')
    nieuw.append((Y,X,2 if nv>nh else 6))
  for Y,X,k in nieuw: o[Y,X]=k
stap('binnenlijnen',v,o)

# --- 2. buitenlijn: lichtkant (naar linksboven gerichte rand, normaal uit de afgevlakte silhouetrand) = gekleurde selout
#        van de groep; schaduwkant = zwart. Geldt ook voor zwart uit het model. Klauwpunten blijven klauwgrijs. ---
v=o.copy(); fg=(o>0).astype(float)
pad=np.pad(fg,3); bl=np.zeros((64,64))
for dy in range(-3,4):
    for dx in range(-3,4): bl+=pad[3+dy:67+dy,3+dx:67+dx]
gy,gx=np.gradient(bl)
uit=[]
for Y,X in zip(*np.where(o>0)):
    if not aan_bg(o,Y,X): continue
    k=o[Y,X]
    if k==15: continue
    nx,ny=-gx[Y,X],-gy[Y,X]; n=np.hypot(nx,ny)+1e-9
    licht=(-nx-ny)/(n*np.sqrt(2))>0.30
    if not licht: uit.append((Y,X,1)); continue
    g=GROEP.get(k)
    if k==1 or g not in DONKER:
        nb=[GROEP[q] for q in buren(o,Y,X) if q>1 and GROEP[q] in DONKER]
        g=max(set(nb),key=nb.count) if nb else None
    if g: uit.append((Y,X,DONKER[g]))
for Y,X,k in uit: o[Y,X]=k
stap('buitenlijn',v,o)

# --- 3. ontkorrelen: tintvlekjes < 3 px (hooglicht/wit < 2) nemen de meest voorkomende buurtint van dezelfde groep aan
#        (lijntinten 2/6, lippen, oog en klauwen niet: die zijn kleine modeldelen). ---
LIJN={2,6}
def ontkorrel(o,mask=None):
    for k,minim in ((3,3),(4,3),(5,3),(7,3),(8,3),(9,3),(10,2)):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=minim: continue
            if mask is not None and not mask[m].any(): continue
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in N4 if 0<=Y+dy<64 and 0<=X+dx<64
                  and GROEP.get(o[Y+dy,X+dx])==GROEP[k] and o[Y+dy,X+dx]!=k and o[Y+dy,X+dx] not in LIJN]
            if buur: o[m]=max(set(buur),key=buur.count)
v=o.copy(); ontkorrel(o); ontkorrel(o); stap('ontkorrelen',v,o)

# --- 4. gezicht per pixel naar het model (de reductie liet de dunne zwarte lijnen te breed winnen):
#        a) kin: model = witte punt die tot rij 27 doorloopt met de contour eronder (dekking W 50-60 %, K 40 %) -> gezichtsschaduw;
#        b) bovenkant gezicht (22,10): W 49 % > K 42 % -> gezicht (ronde kop zoals het model, contour (22,9) blijft);
#        c) bovenlip: het model heeft twee bultjes (cupidoboog, natief x37 en x39); de reductie hield er één ((23,18)).
#           (21,18) -> lipdonker, (22,18) blijft wit ertussen. ---
v=o.copy()
def gez_toon(X,Y):
    fw=lw=0
    for u,v_,w in overlap(X,Y):
        if c[v_,u]==4: fw+=w; lw+=w*L[v_,u]
    return tn(4,lw/fw)
for X,Y in ((23,27),(24,27),(25,27),(26,27)): o[Y,X]=9
o[10,22]=10                 # wit zoals de buren (modeldekking W 49 %)
o[27,28]=6                  # d) kincontour doorlopend: diagonaal (27,27)->(29,26) had een veerlijnpixel ertussen
o[18,21]=11
stap('gezicht naar model',v,o)

NAAM=UIT+'/jynx_regional_r1.png'
opslaan(o,NAAM); toon(o,3,64,0,64)
print('stappen',tel); print('totaal anders dan kaal: %d px'%(o!=kaal).sum(),'| kleuren (excl. transp.)',len(set(o.ravel()))-1,'| figuur px',(o>0).sum())
yy,xx=np.where(o>0); print('bbox x%d-%d y%d-%d'%(xx.min(),xx.max(),yy.min(),yy.max()))
