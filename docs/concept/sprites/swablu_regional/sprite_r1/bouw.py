# Swablu (onweerswolk) r1: model overnemen. Natief raster (239x130, pitch 4,27; figuur 90x81) -> schaal 34/81 (0,420), y16-49, x13-50.
# Verkleinen = oppervlakteweging per spritepixel; daarna alleen technische opschoning, elke stap geteld.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen; from gemeen import *
a,c,L=klassen(); af=a.astype(float)
TK=0.30; TKR=0.15; TG=0.25; TW=0.30
UIT='sprite_r1'
def toon_van(groep,kleur):
    ks=sorted(groep); d=[((np.array(PAL[k])-kleur)**2).sum() for k in ks]; return ks[int(np.argmin(d))]
# --- 0. fracties per spritepixel ---
F=np.zeros((64,64,6)); C=np.zeros((64,64,6,3))
for Y in range(64):
    for X in range(64):
        for u,v,w in overlap(X,Y):
            k=c[v,u]; F[Y,X,k]+=w; C[Y,X,k]+=w*af[v,u]
fK=F[...,1]
def kam(Y,X):   # dunne zwarte modellijn die tussen twee spritepixels valt: de pixel met de meeste lijn (rug dwars op de lijn) wint
    h=fK[Y,X]>=fK[Y,X-1] and fK[Y,X]>=fK[Y,X+1]; v=fK[Y,X]>=fK[Y-1,X] and fK[Y,X]>=fK[Y+1,X]
    return h or v
# --- 1. kale reductie ---
o=np.zeros((64,64),int)
for Y in range(1,63):
    for X in range(1,63):
        f=F[Y,X]
        if f[1:].sum()<0.5: continue                      # minder dan een halve pixel figuur = achtergrond
        if f[4]>=TG: o[Y,X]=toon_van(GEEL,C[Y,X,4]/f[4]); continue      # dunne vonk wint
        if f[1]>=TK or (f[1]>=TKR and kam(Y,X)): o[Y,X]=1; continue     # dunne zwarte lijn wint (drempel, of rug van de lijn)
        if f[5]>=TW: o[Y,X]=toon_van(WIT,C[Y,X,5]/f[5]); continue
        g=2+int(np.argmax(f[2:4]))
        o[Y,X]=toon_van(VOGEL if g==2 else WOLK,C[Y,X,g]/f[g])
kaal=o.copy(); opslaan(kaal,UIT+'/kaal.png')
tel={}
def stap(n,v,o): tel[n]=tel.get(n,0)+int((v!=o).sum())
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def groep(k): return WOLK if k in WOLK else VOGEL if k in VOGEL else GEEL if k in GEEL else WIT if k in WIT else {k}
# --- 2. ontkorrelen: tintvlekjes < 3 px nemen de meest voorkomende buurtint van dezelfde groep aan (lijnen, geel, wit, oog niet) ---
def ontkorrel(o):
    for k in (3,4,5,6,7,8,9,10):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=3: continue
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in N4 if o[Y+dy,X+dx] in groep(k) and o[Y+dy,X+dx]!=k]
            if buur: o[m]=max(set(buur),key=buur.count)
v=o.copy(); ontkorrel(o); ontkorrel(o); stap('ontkorrelen',v,o)
# --- 3. losse zwarte pixels midden in een vlak (geen zwarte 8-buur, niet aan de buitenrand) -> meest voorkomende buurtint ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    nb8=[o[Y+dy,X+dx] for dy,dx in N8]
    if 0 in nb8 or 1 in nb8: continue
    nb=[o[Y+dy,X+dx] for dy,dx in N4]; o[Y,X]=max(set(nb),key=nb.count)
stap('losse zwarte pixels',v,o)
def opsl():
    opslaan(o,UIT+'/swablu_r1.png')
    print('stappen',tel); print('totaal anders dan kaal: %d px'%(o!=kaal).sum(),'| kleuren (excl. transp.)',len(set(o.ravel()))-1,'| figuur px',(o>0).sum())
    yy,xx=np.where(o>0); print('bbox x%d-%d y%d-%d'%(xx.min(),xx.max(),yy.min(),yy.max()))
# --- 4. buitenlijn: geen open of lichte rand. Achtergrond rechts/onder = schaduwkant -> zwart; lichtkant -> selout van de groep
#        (lichte wolk -> wolk midden 4, donkere wolk -> wolk selout 2, vogel -> vogel donker 8). Vonken: zie stap 5. ---
def rand(o):
    fg=o>0; uit=[]
    for Y,X in zip(*np.where(fg)):
        k=o[Y,X]
        if k==1 or k in GEEL: continue
        bL=not fg[Y,X-1]; bR=not fg[Y,X+1]; bU=not fg[Y-1,X]; bD=not fg[Y+1,X]
        if not(bL or bR or bU or bD): continue
        if bR or bD: n=1
        elif k in VOGEL: n=8
        elif k in WOLK: n=4 if k>=5 else 2
        else: n=k
        if n!=k: uit.append((Y,X,n))
    for Y,X,n in uit: o[Y,X]=n
v=o.copy(); rand(o); stap('buitenlijn',v,o)
# --- 5. vonken: geen lichtgeel op de buitenrand; schaduwkant (rechts/onder) oker, lichtkant geel ---
v=o.copy(); fg=o>0
for Y,X in zip(*np.where(np.isin(o,list(GEEL)))):
    bR=not fg[Y,X+1]; bD=not fg[Y+1,X]; bL=not fg[Y,X-1]; bU=not fg[Y-1,X]
    if (bR or bD) and o[Y,X]!=11: o[Y,X]=11
    elif (bL or bU) and o[Y,X]==13: o[Y,X]=12
stap('vonkrand',v,o)
# --- 6. oog: het model heeft een zwart ovaal (natief x109-113, y51-56 = sprite x27,7-29,8 / y27,3-29,9) met een witte glans
#        linksboven (natief x110-111, y52-53 = sprite (28,28)). De reductie gaf een plusteken zonder glans; terug naar de gemeten modelplekken. ---
def zet(lijst,naam,verwacht=None):
    v=o.copy()
    for X,Y,k in lijst: o[Y,X]=k
    stap(naam,v,o)
zet([(28,27,1),(28,28,15),(29,28,1),(28,29,1),(29,29,1),(27,28,9)],'oog')
# --- 7. voelsprieten: dun (model: 2-3 natieve px slate + zwarte rand = ±1,5 spritepx). De buitenlijnregel maakte de linker spriet
#        zwart en de aansluiting op de kop een zwarte klont. Per pixel naar de gemeten fractie (frac.py): slate waar het model
#        >= 50% vogel heeft, zwart waar de zwarte modelrand (schaduwkant rechts/onder) het grootst is. ---
zet([(25,19,9),(26,20,9),(26,21,9),(27,22,9),(27,23,9),     # linker spriet slate (v7, v8, v5, v5, v4)
     (27,21,1),(28,22,1),                                      # zwarte rand rechts ervan (K4, K4)
     (26,22,0),                                                # K3w2: minder dan een halve pixel spriet -> lucht (geen klontje links van de spriet)
     (31,20,8),(30,21,8),                                      # rechter spriet slate (v9, v7), rand eronder blijft zwart
     (31,21,1),                                                # K4: zwarte onderrand rechter spriet (was lucht -> gat in de lijn)
     (33,18,8),(34,18,0)],'voelsprieten')                     # spriettop onder de vonk is slate (model C/E/D), (34,18) w3Y2 = randje -> lucht
if __name__=='__main__' and 'stop7' in sys.argv: opsl(); toon(o,14,36,18,42); sys.exit()
