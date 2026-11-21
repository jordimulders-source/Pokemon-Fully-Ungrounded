# Altaria (onweerswolk) r2: op het kop x1,3-model (model_kop/natief_kop13.png; Jordi: kop te klein). Silhouet = r1-reductie op dat model
# (sprite_r2/basis.py -> basis_kop13.png; alleen kop en kuif anders dan r1), daarop alleen kleur/lijn/schaduw opnieuw uit het model.
# Feedback (Jordi bij Swablu, geldt hier ook): "nee de lijnen zijn veel te hard nu, het ligt aan dat er meer dan 2 kleurtinten moeten zijn
# om minder blur te hebben. De belijning moet juist zachter en niet zwart. Kijk desnoods naar de snavel van de echte swablu qua vorm en hoe die belijnd is"
# Studie game-Altaria: wolk zonder zwart, omlijnd in een donkere wolktint (112,112,152), bollen gescheiden door schaduwtint i.p.v. lijnen;
# snavel omlijnd in donkerblauw/navy, niet zwart; ogen: ver oog 1x2 zwart, nabij oog 2x2 met 1 glanspixel.
import sys, numpy as np
from PIL import Image
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'sprite_r2')
import gemeen as G; from gemeen import label, X0, Y0
import basis as B; from basis import blok
UIT='sprite_r2'
# 0 transp | 1 zwart (alleen pupillen) | 2 navy (buitenlijn schaduwkant) | wolk 3 selout 4 donker 5 midden 6 licht 7 hooglicht |
# violet 8 selout 9 donker 10 midden 11 licht | 12 static | 13 glans.  Modelkleuren (klassengemiddelden per helderheidsband, zie NOTITIES).
PAL=[(152,208,160),(6,12,28),(17,31,61),
     (28,50,81),(50,83,116),(72,116,149),(104,156,185),(145,204,223),
     (31,37,88),(54,60,141),(95,99,206),(141,145,233),
     (136,186,210),(236,240,251)]
G.PAL=PAL; P=np.array(PAL,float)
WOLK=[3,4,5,6,7]; VULW=[4,5,6,7]; VIOL=[8,9,10,11]; VULV=[9,10,11]
CH='.KN01234abcdsW'
def toon(o,y0=8,y1=64,x0=0,x1=64):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
a,c,L=B.a,B.c,B.L; af=a.astype(float)
r1=np.asarray(Image.open('sprite_r2/basis_kop13.png')).astype(int)     # basis (r1-regels op het kop x1,3-model)
fig=r1>0
KUIF=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fig)): KUIF[Y,X]=B.kuif(X,Y) and r1[Y,X] in (1,6,7,8,9)
def kuif(X,Y): return KUIF[Y,X]
tel={}
def stap(naam,v,o): tel[naam]=tel.get(naam,0)+int((v!=o).sum())
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
def meest(l): return max(set(l),key=l.count)
def dichtst(kleur,groep): return min(groep,key=lambda k:((P[k]-kleur)**2).sum())
# --- 1. per blok binnen het bevroren silhouet: static blijft waar r1 static had (modelplekken, al opgeschoond); kuif = r1-kuif vertaald;
#        verder: zwart in het model (>=3/9) = lijn (gemarkeerd, kleur volgt in stap 3); anders groep naar aandeel, tint = dichtstbijzijnde
#        vultint bij het blokgemiddelde (4 wolkvultinten = een tussenstap meer dan r1, dus zachtere overgangen) ---
# wolkhelderheid per blok (alleen wolkpixels) en verzacht: 1/2 eigen blok + 1/2 gewogen buren (1-2-1)
Lw=np.full((64,64),np.nan)
for Y,X in zip(*np.where(fig)):
    u,v=blok(X,Y); b=c[v:v+3,u:u+3]; m=np.isin(b,[2,4])
    if m.any(): Lw[Y,X]=L[v:v+3,u:u+3][m].mean()
LW=Lw.copy()
for Y,X in zip(*np.where(~np.isnan(Lw))):
    acc=0; tw=0
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            w=(2-abs(dy))*(2-abs(dx))
            if not np.isnan(Lw[Y+dy,X+dx]): acc+=w*Lw[Y+dy,X+dx]; tw+=w
    LW[Y,X]=0.5*Lw[Y,X]+0.5*acc/tw
Lp=P@[.299,.587,.114]; TH=[(Lp[4]+Lp[5])/2,(Lp[5]+Lp[6])/2,(Lp[6]+Lp[7])/2]
o=np.zeros((64,64),int); lijn=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fig)):
    u,v=blok(X,Y); b=c[v:v+3,u:u+3].ravel(); blk=af[v:v+3,u:u+3].reshape(-1,3)
    if r1[Y,X]==10: o[Y,X]=12; continue
    if kuif(X,Y): o[Y,X]={1:8,6:9,7:10,8:11,9:11}.get(r1[Y,X],10); continue
    nK=(b==1).sum(); nw=(b==2).sum()+(b==4).sum(); nv=(b==3).sum()+(b==5).sum()
    grp=VULW if nw>=nv else VULV
    if nK>=3 or nw+nv==0:
        lijn[Y,X]=True; o[Y,X]=3 if nw>=nv else 8; continue
    m=np.isin(b,[2,4]) if grp is VULW else np.isin(b,[3,5])
    if grp is VULV: o[Y,X]=dichtst(blk[m].mean(0),grp); continue
    # wolk: helderheid van het blok, licht verzacht met de 8 buurblokken (alleen wolkpixels van het model) -> drempels halverwege de tinten.
    # Zo volgen de tintgrenzen de ronde bollen van het model (concentrische banden) i.p.v. hoekige blokken.
    lb=LW[Y,X]; o[Y,X]=4 if lb<TH[0] else 5 if lb<TH[1] else 6 if lb<TH[2] else 7
# donkere naden tussen de bollen -> selout 3 als binnenlijn (donkerste wolktint, geen zwart): alleen een dal in de modelhelderheid, d.w.z. het blok
# is donker (L<62) en in een richting (horizontaal, verticaal of diagonaal) aan beide kanten >=15 lichter: een naad, geen donker vlak
Lz=np.nan_to_num(Lw,nan=-1)
for Y,X in zip(*np.where(fig&(Lz>=0)&(Lz<62)&np.isin(o,VULW))):
    l=Lz[Y,X]
    for dy,dx in ((0,1),(1,0),(1,1),(1,-1)):
        p,q=Lz[Y-dy,X-dx],Lz[Y+dy,X+dx]
        if p>=l+15 and q>=l+15: o[Y,X]=3; break
kaal=o.copy()
# --- 2. ontkorrelen: vultint-vlekjes < 4 px -> meest voorkomende buurvultint van dezelfde groep; uitsteeksels van 1 px idem ---
def groep(k): return VULW if k in VULW else VULV if k in VULV else [k]
def ontkorrel(o,grens=4):
    for k in VULW+VULV:
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            mm=lab==i
            if mm.sum()>=grens: continue
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(mm)) for dy,dx in N4 if o[Y+dy,X+dx] in groep(k) and o[Y+dy,X+dx]!=k]
            if buur: o[mm]=meest(buur)
v=o.copy(); ontkorrel(o); ontkorrel(o)
for _ in range(2):
    for Y,X in zip(*np.where(np.isin(o,VULW+VULV))):
        k=o[Y,X]; nb=[o[Y+dy,X+dx] for dy,dx in N4]
        if nb.count(k)>1: continue
        for t in set(nb):
            if t!=k and t in groep(k) and nb.count(t)>=3: o[Y,X]=t; break
stap('ontkorrelen+uitsteeksels',v,o)
# --- 3. binnenlijnen (zwart in het model): gekleurde selout (wolk 3 / violet 8) in plaats van zwart; een lijnpixel zonder andere lijn/selout-buur
#        (8-buren) is een stip, geen lijn -> buurvultint ---
v=o.copy()
for Y,X in zip(*np.where(np.isin(o,[3,8]))):
    if kuif(X,Y): continue
    if not any(o[Y+dy,X+dx] in (3,8,0) for dy,dx in N8):
        nb=[o[Y+dy,X+dx] for dy,dx in N4 if o[Y+dy,X+dx] in VULW+VULV]
        if nb: o[Y,X]=meest(nb)
stap('selout-stippen',v,o)
# --- 4. buitenlijn: zachter en niet zwart. Achtergrond rechts/onder (schaduwkant) -> navy (17,31,61); lichtkant -> selout van de groep.
#        Static buiten de wolk en de kuif apart. ---
v=o.copy(); uit=[]
for Y,X in zip(*np.where(o>0)):
    k=o[Y,X]
    if k==12 or kuif(X,Y): continue
    bL=not fig[Y,X-1]; bR=not fig[Y,X+1]; bU=not fig[Y-1,X]; bD=not fig[Y+1,X]
    if not(bL or bR or bU or bD): continue
    uit.append((Y,X,2 if (bR or bD) else 3 if k in WOLK else 8))
for Y,X,n in uit: o[Y,X]=n
stap('buitenlijn',v,o)
# --- 5. kuif: kartelige vorm van r1 (= model) blijft; omlijnd in donkerviolet: pixels aan de schaduwkant (achtergrond rechts/onder) van een
#        streng die 2 px dik is -> selout 8; 1 px dunne takjes donker violet 9 (geen zwart, niet weggevallen); licht alleen binnen/aan de lichtkant ---
v=o.copy(); uit=[]
for Y,X in zip(*np.where(o>0)):
    if not kuif(X,Y) or o[Y,X]==12: continue
    k=o[Y,X]; bL=not fig[Y,X-1]; bR=not fig[Y,X+1]; bU=not fig[Y-1,X]; bD=not fig[Y+1,X]
    dik=(fig[Y-1,X] and fig[Y+1,X]) or (fig[Y,X-1] and fig[Y,X+1]) or (bD and fig[Y-1,X]) or (bR and fig[Y,X-1])
    dun=sum(fig[Y+dy,X+dx] for dy,dx in N4)<=1 or (bL and bR) or (bU and bD)
    if dun and not dik: uit.append((Y,X,10 if k==11 else k))   # 1 px dunne takjes: midden/donker violet (geen licht op de rand, niet weggevallen)
    elif (bR or bD) and (fig[Y-1,X] or fig[Y,X-1]): uit.append((Y,X,8))
for Y,X,n in uit: o[Y,X]=n
stap('kuif omlijnd',v,o)
def zet(lijst,naam):
    v=o.copy()
    for X,Y,k in lijst: o[Y,X]=k
    stap(naam,v,o)
# --- 6. gezicht (de reductie gaf geen ogen meer: zwart -> selout -> stip weg). Modelogen: zwarte ovalen natief x72-75 / x85-87, y50-53 =
#        X23 / X27, Y21 + bovenste derde van Y22; glans natief (73,50) en (86,50-51) = bovenkant oog. Game-Altaria: ver oog 1x2 zwart, nabij oog met glanspixel.
OOG=sys.argv[1] if len(sys.argv)>1 else 'C'   # gekozen: C (A/B in NOTITIES)
# kop x1,3-model: linkeroog natief x68-71, rij 48-51 -> (22,20-21); rechteroog x85-88, rij 47-51 -> (27-28,20-21), glans natief (86,47-48) = linksboven
if OOG=='A': zet([(22,20,1),(22,21,1),(27,20,1),(27,21,1)],'ogen')
if OOG=='B': zet([(22,20,1),(22,21,1),(27,20,13),(27,21,1)],'ogen')
if OOG=='C': zet([(22,20,1),(22,21,1),(27,20,13),(28,20,1),(27,21,1),(28,21,1)],'ogen')
#        snavel (Swablu-snavel als voorbeeld: licht boven, donkere onderrand, geen zwart): Y22 hooglicht (model 3/s), Y23 licht teal (model 2/3,
#        mondlijn natief rij 58 valt onderin), Y24 = mondlijn/onderrand in navy (model K op rij 59 en 61) i.p.v. selout+navy door elkaar
#        kop x1,3-model: snavel natief x65-85 (X20-26), rij 53-55 hooglicht (Y22), 56-58 licht met mondlijn onderin (Y23), 59-61 zwarte lijnen (Y24)
zet([(X,22,7) for X in range(21,27)]+[(X,23,6) for X in range(21,27)]+[(X,24,2) for X in range(21,27)],'snavel')
if __name__=='__main__':
    G.opslaan(o,UIT+'/altaria_r2.png'); print(tel); toon(o)
