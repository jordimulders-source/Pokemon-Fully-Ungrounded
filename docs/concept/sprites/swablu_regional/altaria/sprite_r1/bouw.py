# Altaria (onweerswolk) r1: model overnemen. Natief raster 199x199 (pitch 5,12) -> gehele 3x3-blokken (schaal 1/3), sprite x3-61, y9-62.
# Stap 1 = kale reductie (alleen tellen en kiezen uit modelpixels), daarna technische opschoning, elke stap geteld.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen, statisch; from gemeen import *
a,c,L=klassen(); st=statisch(a,c,L)
UIT='sprite_r1'
P=np.array(PAL,float)
# --- 0. elke natieve pixel naar de dichtstbijzijnde paletkleur van zijn klasse (geen mengen: zo blijven de tintvlakken van het model hard) ---
q=np.zeros(c.shape,int)
for cl,grp in ((1,[1]),(2,[2,3,4,5]),(3,[6,7,8]),(4,[10]),(5,[9])):
    m=c==cl; d=((a[m][:,None,:]-P[grp][None])**2).sum(2); q[m]=np.array(grp)[d.argmin(1)]
q[st]=10
q[(c==4)&~st]=5    # cyaanwit dat geen lijntje is (hooglicht op een wolkbol) -> wolkhooglicht
# --- 1. kale reductie per 3x3-blok ---
def kies(Y,X):
    u,v=blok(X,Y); b=q[v:v+3,u:u+3].ravel(); n=lambda k:(b==k).sum()
    fig=(b>0).sum()
    if Y<=16 or (Y<=21 and X>=32):              # kuif (strengen 4-7 natieve px dik = 1,5-2 spritepx): violet wint vanaf 3/9, lavendelwit telt als licht violet
        vi=sum(n(k) for k in (6,7,8,9))
        if n(10)>=2 and vi<3: return 10
        if vi>=3:
            tel=[(n(6),6),(n(7),7),(n(8)+n(9),8)]; m=max(t for t,k in tel); beste=[k for t,k in tel if t==m]
            return 9 if n(9)>=5 else beste[-1] if len(beste)>1 else beste[0]
        if n(1)>=3: return 1
        return 0
    if n(10)>=2: return 10                       # dun static-lijntje (1 natieve px = 3 per blok) wint
    if fig<5: return 0                           # minder dan een halve pixel figuur = achtergrond
    if n(1)>=3: return 1                         # dunne zwarte lijn wint
    if n(9)>=2: return 9                         # kuiflicht / oogglans
    w=sum(n(k) for k in WOLK); vi=sum(n(k) for k in VIOLET)
    grp=WOLK if w>=vi else VIOLET
    if max(w,vi)==0: return 1
    tel=[(n(k),k) for k in sorted(grp)]; m=max(t for t,k in tel)
    beste=[k for t,k in tel if t==m]
    if len(beste)==1: return beste[0]
    gem=a[v:v+3,u:u+3].reshape(-1,3)[np.isin(b,list(grp))].mean(0)          # gelijkspel: dichtst bij het blokgemiddelde
    return min(beste,key=lambda k:((P[k]-gem)**2).sum())
o=np.zeros((64,64),int)
for Y in range(64):
    for X in range(64):
        u,v=blok(X,Y)
        if 0<=u<197 and 0<=v<197: o[Y,X]=kies(Y,X)
kaal=o.copy(); opslaan(kaal,UIT+'/kaal.png')
if __name__=='__main__' and len(sys.argv)>1 and sys.argv[1]=='kaal': toon(o); sys.exit()
tel={}
def stap(naam,v,o): tel[naam]=tel.get(naam,0)+int((v!=o).sum())
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def groep(k): return WOLK if k in WOLK else VIOLET if k in VIOLET else {k}
def meest(lijst): return max(set(lijst),key=lijst.count)
# --- 2. static: losse static-pixels (geen static-8-buur) zijn ruis -> meest voorkomende buurtint (niet-static) ---
v=o.copy()
for Y,X in zip(*np.where(o==10)):
    if not any(o[Y+dy,X+dx]==10 for dy,dx in N8):
        nb=[o[Y+dy,X+dx] for dy,dx in N4 if o[Y+dy,X+dx] not in (10,)]; o[Y,X]=meest(nb)
stap('static los',v,o)
# --- 3. ontkorrelen: tintvlekjes < 3 px (4-buren) nemen de meest voorkomende buurtint van dezelfde groep aan (lijnen, static, wit niet) ---
def ontkorrel(o,grens=3):
    for k in (2,3,4,5,6,7,8):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=grens: continue
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in N4 if o[Y+dy,X+dx] in groep(k) and o[Y+dy,X+dx]!=k]
            if buur: o[m]=meest(buur)
v=o.copy(); ontkorrel(o); ontkorrel(o); stap('ontkorrelen',v,o)
# --- 4. losse zwarte pixels midden in een vlak (geen zwarte 8-buur, niet aan de buitenrand) -> meest voorkomende buurtint ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    nb8=[o[Y+dy,X+dx] for dy,dx in N8]
    if 0 in nb8 or 1 in nb8: continue
    o[Y,X]=meest([o[Y+dy,X+dx] for dy,dx in N4])
stap('losse zwarte pixels',v,o)
# --- 5. buitenlijn: geen open of lichte rand. Achtergrond rechts/onder = schaduwkant -> zwart; lichtkant -> selout (wolk 2, violet 6) ---
def rand(o):
    fg=o>0; uit=[]
    for Y,X in zip(*np.where(fg)):
        k=o[Y,X]
        if k in (1,10): continue
        bL=not fg[Y,X-1]; bR=not fg[Y,X+1]; bU=not fg[Y-1,X]; bD=not fg[Y+1,X]
        if not(bL or bR or bU or bD): continue
        n=1 if (bR or bD) else 2 if k in WOLK else 6 if k in VIOLET|{9} else k
        if n!=k: uit.append((Y,X,n))
    for Y,X,n in uit: o[Y,X]=n
v=o.copy(); rand(o); stap('buitenlijn',v,o)
def zet(lijst,naam):
    v=o.copy()
    for X,Y,k in lijst: o[Y,X]=k
    stap(naam,v,o)
def opsl():
    opslaan(o,UIT+'/altaria_r1.png')
    print('stappen',tel); print('totaal anders dan kaal: %d px'%(o!=kaal).sum(),'| kleuren (excl. transp.)',len(set(o.ravel()))-1,'| figuur px',(o>0).sum())
    yy,xx=np.where(o>0); print('bbox x%d-%d y%d-%d'%(xx.min(),xx.max(),yy.min(),yy.max()))
if __name__=='__main__': opsl(); toon(o)
