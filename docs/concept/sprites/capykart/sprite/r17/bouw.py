# Capykart r17: model overnemen (Dundragoon-methode). Natief raster 99x99 (pitch 10,24; figuur 73x72) -> schaal 62/73.
# 1) kale reductie (kaal.py) 2) alleen technische opschoning, elke stap geteld 3) bovenlaag gezicht uit r15b (Jordi: "het Capybarrel-gezicht,
# de morrillo, de Bibarel-tanden — deze blijven"), pixel voor pixel op de modelplek 4) palet naar 16 (blauw-boven 3 px -> blauw-licht).
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'sprite/r17'); from gemeen import *; from kaal import reduce
UIT='sprite/r17/'
o=reduce(); kaal=o.copy()
tel={}; stapmap=np.full((64,64),'',object)
def stap(n,v,o):
    tel[n]=tel.get(n,0)+int((v!=o).sum()); stapmap[v!=o]=n
# --- 1. buitenlijn: geen open/lichte rand. Achtergrond rechts/onder = zwart; lichtkant = eigen donkerste tint (selout). Zwart blijft. ---
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
# --- 2. ontkorrelen: tintvlekjes < 3 px (hoogste bruin < 2) -> meest voorkomende buurtint uit dezelfde groep (lijntinten niet) ---
def ontkorrel(o,mask=None):
    for k,minim in ((3,3),(4,3),(5,3),(6,2),(7,2),(9,2),(10,3),(12,2),(13,3),(15,3)):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=minim: continue
            if mask is not None and not (m&mask).any(): continue
            G=groep(k)
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[Y+dy,X+dx] in G and o[Y+dy,X+dx]!=k and o[Y+dy,X+dx] not in (2,8)]   # lijntinten (bruin-lijn, hoepel-donker) zijn geen vultint
            if buur: o[m]=max(set(buur),key=buur.count)
v=o.copy(); ontkorrel(o); ontkorrel(o); stap('ontkorrelen',v,o)
# --- 3. losse zwarte pixel midden in een vlak (geen zwarte 8-buur, geen achtergrond) -> buurtint ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    nb=[o[Y+dy,X+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
    nb8=[o[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx)]
    if 0 not in nb8 and 1 not in nb8: o[Y,X]=max(set(nb),key=nb.count)
stap('losse zwarte pixels',v,o)
# --- 3b. wat stap 3 kapotmaakte terug naar het model: neusgat (20,23) (model: 2 neusgaten, het linker valt samen met de buitenlijn) en
#         de mondlijn (18,29),(20,30) (model: zwarte mondpixels onder de snuit). Alleen pixels die in de kale reductie zwart waren. ---
v=o.copy()
for X,Y in [(20,23),(18,29),(20,30)]:
    assert kaal[Y,X]==1; o[Y,X]=1
stap('neusgat+mond terug (model)',v,o)
# --- 4. bovenlaag gezicht uit r15b (pixel voor pixel; r15b-index -> rol in dit palet: 1 zwart->1, 4 donkerste vacht->2 bruin-lijn,
#        8 blauwgrijs->8 hoepel-donker, 9 crème->9 geel (enige lichte geeltint; palet vol)). Plek: op het modelonderdeel.
r15=np.asarray(Image.open('sprite/r15b/capykart_creme.png')).astype(int)
ROL={1:1,4:2,8:8,9:9}
def plak(x0,x1,y0,y1,dx,dy,idx,naam):
    v=o.copy()
    for Y in range(y0,y1+1):
        for X in range(x0,x1+1):
            if r15[Y,X] in idx: o[Y+dy,X+dx]=ROL[r15[Y,X]]
    stap(naam,v,o)
# oog + wenkbrauw (blije Capybarrel-oog): r15b x28-31, y16-20 -> modeloog (+1,+1); het modeloog (3x3 zwart) eerst terug naar de vachttint eromheen
v=o.copy()
for Y,X in [(19,30),(19,31),(19,32),(20,29),(20,30),(20,31),(21,29),(21,30),(21,31)]:
    if o[Y,X]==1: o[Y,X]=5
stap('oog: modeloog weg',v,o)
plak(28,31,16,20,1,1,{1,4},'oog+wenkbrauw (r15b)')
# morrillo: r15b (22-24,15),(21-23,16) -> snuitrug van het model (0,+1), net binnen de buitenlijn zoals in r15b
plak(21,24,15,16,0,1,{8},'morrillo (r15b)')
# Bibarel-tanden: r15b x18-23, y30-33 (zwart kader, crème, grijs) -> onder de bovenlip van het model (0,+2)
plak(18,23,30,33,0,2,{1,8,9},'tanden (r15b)')
# --- 5. palet naar 16: blauw-boven (12, 3 px in de reductie) -> blauw-licht (13); indices 13-16 schuiven 1 op ---
v=o.copy(); o[o==12]=13; stap('blauw-boven -> blauw-licht',v,o)
o2=o.copy(); o2[o>12]-=1; k2=kaal.copy(); k2[k2==12]=13; k2[kaal>12]-=1
PAL16=PAL[:12]+PAL[13:]
NAAM=UIT+'capykart.png'
opslaan(o2,NAAM,PAL16); opslaan(k2,UIT+'kaal16.png',PAL16)
# variant (alleen palet anders, pixels identiek): index 9 = r15b-crème (252,232,150) gedeeld door tanden en geel blok
PALC=list(PAL16); PALC[9]=(252,232,150); opslaan(o2,UIT+'capykart_tandcreme.png',PALC)
Image.open(UIT+'capykart_tandcreme.png').convert('RGBA').resize((512,512),Image.NEAREST).save(UIT+'capykart_tandcreme_8x.png')
Image.open(NAAM).convert('RGBA').resize((512,512),Image.NEAREST).save(UIT+'capykart_8x.png')
toon(o)
print('stappen',tel); print('totaal anders dan kaal: %d px'%(o!=kaal).sum(),'| kleuren incl. transp.',len(PAL16),'| figuur px',(o>0).sum())
yy,xx=np.where(o>0); print('bbox x%d-%d y%d-%d'%(xx.min(),xx.max(),yy.min(),yy.max()))
np.save(UIT+'_stap.npy',stapmap); np.save(UIT+'_o.npy',o); np.save(UIT+'_kaal.npy',kaal)
