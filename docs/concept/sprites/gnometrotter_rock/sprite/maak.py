# maak.py: kale reductie (kaal.png) -> technisch opgeschoond -> red.png (onderlaag voor de omlijningsronde)
# Alles komt uit de kale reductie; alleen technisch: buitenlijn 1 px (DC: outline base aan de lichtkant, zwart aan de schaduwkant),
# kleur per onderdeel binnen de eigen familie (<= 3 vlaktinten + lijn), binnenlijnen niet zwart, ruis < 3 px weg,
# gebroken stok heel (drempel), en Jordi's toegestane afwijking: oogstrook dicht met mutskleur.
import numpy as np; from PIL import Image; from scipy import ndimage as nd
from gemeen import *
from reductie_gedeeld import reduceer
kaal=lees('kaal.png'); zone=np.load('zone.npy'); kl=np.load('lijnkans.npy'); oog=np.load('oog.npy')
a=np.asarray(Image.open('../r8/gemini_r8.png').convert('RGB')).astype(float); gem,dek=reduceer(a)
fg=zone>0
o=kaal.copy()
for Y,X in zip(*np.where(fg&(o==0))):          # stok: pixels onder de 50 %-drempel die de stok heel houden
    o[Y,X]=1+np.argmin(((np.array(PAL[1:],float)-gem[Y,X])**2).sum(1))
FAM={1:'z',2:'d',3:'d',4:'d',5:'d',6:'r',7:'r',8:'r',15:'r',9:'b',10:'b',11:'b',12:'l',13:'l',14:'l'}
ZFAM={z:('r' if RAMP[z]==ROZE else 'b' if RAMP[z]==BLAUW else 'l' if RAMP[z]==LICHT else 'd') for z in RAMP}
L=lambda k: lum(PAL[k])
for Y,X in zip(*np.where(fg)):
    z=zone[Y,X]; k=o[Y,X]; zf=ZFAM[z]; b=BASIS[z]
    if k==1 or k==b: continue                                   # lijn (model) blijft lijn; zwart binnenin volgt hieronder
    if FAM[k]==zf and k in RAMP[z]: continue                    # eigen vlaktint
    if L(k)<=L(b)+8 or (FAM[k]!=zf and kl[Y,X]>=0.17): o[Y,X]=b # donkerder dan de vlaktinten / modelnaad door de vlakgemiddelde -> lijn
    else:                                                       # vreemde/te veel tint -> dichtstbijzijnde vlaktint op helderheid
        o[Y,X]=min(RAMP[z],key=lambda t:abs(L(t)-lum(gem[Y,X])))
# oogstrook (Jordi "1 akkoord"): dicht met mutskleur (onderkant muts = tint 3)
oog&=zone!=5                     # neusrand blijft neus
zone[oog]=1; o[oog]=3
# buitenlijn 1 px, Dragonfly Cave: zwart = outline shadow (schaduwkant), lichtkant = outline base van het vlak
fg=zone>0
OUT=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg)):
    if any(not(0<=Y+dy<64 and 0<=X+dx<64) or not fg[Y+dy,X+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): OUT[Y,X]=True
LICHT=np.array([-0.6,-0.8])
def normaal(Y,X):
    v=np.zeros(2)
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if (dy or dx) and (not(0<=Y+dy<64 and 0<=X+dx<64) or not fg[Y+dy,X+dx]): v+=(dx,dy)
    n=np.linalg.norm(v); return v/n if n else v
for Y,X in zip(*np.where(OUT)): o[Y,X]=BASIS[zone[Y,X]] if normaal(Y,X)@LICHT>0.35 else 1
# zwart binnenin (modellijn) -> outline base van het eigen vlak (binnenlijnen niet zwart)
for Y,X in zip(*np.where(fg&~OUT&(o==1))): o[Y,X]=BASIS[zone[Y,X]]
# onderdeelgrens zonder lijn in de reductie: lijn op het voorste onderdeel
rank={p:i for i,p in enumerate(PRIO)}
islijn=lambda Y,X: o[Y,X] in (1,BASIS[zone[Y,X]])
BIN=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg&~OUT)):
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        y,x=Y+dy,X+dx
        if zone[y,x]!=zone[Y,X] and rank[zone[y,x]]>rank[zone[Y,X]] and not islijn(Y,X) and not islijn(y,x): BIN[Y,X]=True
for Y,X in zip(*np.where(BIN)): o[Y,X]=BASIS[zone[Y,X]]
# modelnaden die de vlakgemiddelde wegpoetste (lijn 0,5 px breed): lijnbedekking >= 0,17 en lokaal maximum dwars op de lijn,
# alleen waar binnen 1 px nog geen lijn ligt (geen dubbele lijnen)
K=np.pad(kl,1)
def nms(Y,X):
    c=kl[Y,X]; y,x=Y+1,X+1
    return (c>=K[y,x-1] and c>K[y,x+1]) or (c>=K[y-1,x] and c>K[y+1,x])
NAAD=[]
for Y,X in zip(*np.where(fg&~OUT&~oog&(kl>=0.17))):
    if islijn(Y,X) or not nms(Y,X): continue
    if any(islijn(Y+dy,X+dx) and zone[Y+dy,X+dx]==zone[Y,X] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): continue
    NAAD.append((Y,X))
for Y,X in NAAD: o[Y,X]=BASIS[zone[Y,X]]
print('naden toegevoegd',len(NAAD))
# ronde onderdelen (neus, hand R, bovenarm R): rand rondom in 6, zwart als boog linksmidden-linksonder-ondermidden (SPRITE_KERN, Gnomini r10)
for zz in (5,9,8):
    m=zone==zz; yy,xx=np.where(m); cy,cx=yy.mean(),xx.mean()
    rand=m&nd.binary_dilation(~m,structure=np.array([[0,1,0],[1,1,1],[0,1,0]]))
    for Y,X in zip(*np.where(rand)):
        h=np.degrees(np.arctan2(Y-cy,X-cx)); o[Y,X]=1 if 80<=h<=190 else 6
LIJN=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg)): LIJN[Y,X]=o[Y,X] in (1,BASIS[zone[Y,X]]) and not (zone[Y,X] in (5,6,7,8,9) and False)
# ruis: tintvlekjes < 3 px binnen een vlak -> meest voorkomende buurtint van hetzelfde onderdeel (glans 15 en lijnen uitgezonderd)
for _ in range(2):
    for k in set(o[fg].ravel())-{1,2,4,6,9,15}:
        lab,n=nd.label((o==k)&fg,structure=np.ones((3,3)))
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=3: continue
            ys,xs=np.where(m); z=zone[ys[0],xs[0]]
            r=nd.binary_dilation(m,structure=np.ones((3,3)))&~m&(zone==z)
            t=o[r]; t=t[(t!=k)&np.isin(t,RAMP[z])]
            if len(t): o[m]=np.bincount(t).argmax()
# losse lijnstipjes (< 3 px, raken geen andere lijn): modelnaad die na de reductie als stip overbleef -> vlaktint van de buren
lm=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg)): lm[Y,X]=o[Y,X] in (1,BASIS[zone[Y,X]]) or (zone[Y,X] in (5,8,9) and o[Y,X]==6)
lab,n=nd.label(lm,structure=np.ones((3,3))); stip=0
for i in range(1,n+1):
    m=lab==i
    if m.sum()>=3: continue
    for Y,X in zip(*np.where(m)):
        t=[o[y,x] for y in range(Y-1,Y+2) for x in range(X-1,X+2) if 0<=y<64 and 0<=x<64 and fg[y,x] and not lm[y,x] and o[y,x] in RAMP[zone[Y,X]]]
        if t: o[Y,X]=np.bincount(t).argmax(); stip+=1
print('lijnstipjes weg',stip)
# vlakken rustiger: 1 ronde meerderheidsfilter (3x3) op de vlaktinten binnen hetzelfde onderdeel; lijnen en glans blijven
isl=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg)): isl[Y,X]=o[Y,X] in (1,BASIS[zone[Y,X]]) or o[Y,X]==15
o2=o.copy()
for Y,X in zip(*np.where(fg&~isl)):
    t=[o[y,x] for y in range(Y-1,Y+2) for x in range(X-1,X+2) if 0<=y<64 and 0<=x<64 and fg[y,x] and not isl[y,x] and zone[y,x]==zone[Y,X]]
    c=np.bincount(t,minlength=16)
    if c.max()>=5 and c[o[Y,X]]<c.max(): o2[Y,X]=c.argmax()
o=o2
np.save('zone_af.npy',zone)
opslaan(o,'red.png')
