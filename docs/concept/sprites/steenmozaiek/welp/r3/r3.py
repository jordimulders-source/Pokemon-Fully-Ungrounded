# Ronde 3 (Jordi op r2): rug smooth (mag van het model afwijken), lijfpatronen groter en strak, minder blurry,
# heupspiraal mag de dij niet opheffen. Basis: welp_r2.npy (met extra) en welp_r2_zonder_extra.npy (voor de heup).
import numpy as np, math, sys
HEUP=sys.argv[1] if len(sys.argv)>1 else 'A'
r2=np.load('welp_r2.npy'); z2=np.load('welp_r2_zonder_extra.npy')
FIN=np.load('FIN2.npy')
_,K,d,S,M,L,P,Q,R,g_,W,C,T,G=range(14)
a=r2.copy(); H,Wd=a.shape
# 0. heup terug naar zonder_extra (dijvorm uit het model), borstkrul weg (komt opnieuw)
a[27:40,29:44]=z2[27:40,29:44]
a[23:26,15:18]=z2[23:26,15:18]
frozen=np.zeros_like(a,bool)
# 1. rug: nieuwe rechterrand (exclusief) per rij, vloeiende S: 2-1-1-1-1-2(plat)-1..1 dan verticale runs 2-2-2-3
EDGE={13:28,14:29,15:29,16:30,17:31,18:32,19:34,20:35,21:36,22:37,23:38,24:39,25:40,26:40,27:41,28:41,29:42,30:42,31:43,32:43,33:43,34:44}
for y,e in EDGE.items():
    row=a[y]; xs=np.where(row[:44]>0)[0]; old=xs.max()+1
    inner=row[old-2] if row[old-2] not in (K,d) else row[old-3]
    for x in range(min(old,e)-1,max(old,e)):
        a[y,x]=0 if x>=e else inner
    a[y,e-1]=K
# rugrand: buitenste vulpixel onder de omlijning is schaduw s (sikkel volgt de rug)
for y in range(13,35):
    e=EDGE[y]; 
    if a[y,e-2] in (M,L): a[y,e-2]=S
np.save('stap1.npy',a)
# 2. patronen (strak, groter); kleuren: lila r, lijn d, bruin = basis, creme c
from spiraal import spiral
COL={'lila':R,'lijn':d,'creme':C,'kern':d}
def plak(o,base_bruin=M,skip=(0,K,W,T,G,g_)):
    n=0
    for (x,y),k in o.items():
        if not(0<=x<Wd and 0<=y<H) or a[y,x] in skip: continue
        v=COL.get(k,base_bruin)
        if a[y,x]!=v: a[y,x]=v; n+=1
        frozen[y,x]=True
    return n
# schouder: was cremeboog r~5 rond (24,25); nu r 6.5, opening linksonder zoals het model
for (x,y) in [(x,y) for x in range(17,31) for y in range(18,32)]:
    if a[y,x] in (P,Q,R,C) and (x-24)**2+(y-25)**2<=6.8**2 and not (y>=29 and x>=26): a[y,x]=M   # oude ring weg
n_sch=plak(spiral(24,25,6.5,3.0,boog=(300,210)))
np.save('stap2.npy',a)
print('schouder',n_sch)
# 3. rugband: oude wazige lila band weg, nieuwe band volgt de gladde rugrand (2 px licht lila + 1 px donkerlila onderlijn),
#    eindigend in een krul zoals in het model
for y in range(12,28):
    for x in range(22,41):
        if a[y,x] in (P,Q,R) and not frozen[y,x]: a[y,x]=M
n_rug=0
for y in range(14,22):
    e=EDGE[y]
    for x,v in ((e-2,R),(e-3,R),(e-4,P)):
        if a[y,x]!=v: a[y,x]=v; n_rug+=1
        frozen[y,x]=True
# rugkrul: de band draait aan het eind naar binnen (model), 1 px lila lijn op bruin
for y in range(21,27):
    e=EDGE[y]
    for x in range(29,e-1):
        if not frozen[y,x] and a[y,x] not in (K,C,d): a[y,x]=M
    if a[y,e-2]!=K and not frozen[y,e-2]: a[y,e-2]=S
o=spiral(33,24,2.8,3.0,cw=-1,klassen=('lila','bruin','bruin'),kern=0.6)
for (x,y),k in o.items():
    if k in ('lila','kern') and a[y,x] not in (0,K) and not frozen[y,x]:
        a[y,x]=R; n_rug+=1; frozen[y,x]=True
np.save('stap3.npy',a); print('rug',n_rug)
# 4. heup/dij (Jordi: "de heupspiraal is nog niet geslaagd want daardoor valt het been weg"):
#    de dij is in het model een eigen ovaal vlak met donkere rand, licht halve maan linksboven, schaduw rechtsonder;
#    die vorm eerst strak neerzetten, de spiraal er binnen.
cx,cy,rx,ry=35.9,33.4,5.7,5.1
def inell(x,y,sh=0): return ((x+.5-cx)/(rx-sh))**2+((y+.5-cy)/(ry-sh))**2<=1
def ang(x,y): return math.degrees(math.atan2(-(y+.5-cy),x+.5-cx))%360
n_heup=0; base=a.copy()
for y in range(26,40):
    for x in range(28,44):
        if not inell(x,y) or a[y,x] in (0,K): continue
        A=ang(x,y); topleft = 60<=A<=250
        if not inell(x,y,1.0): v=d if topleft else (S if a[y,x]!=d else d)
        elif not inell(x,y,2.0): v=L if 70<=A<=200 else (S if (A>=250 or A<=20) else M)
        else: v=M
        a[y,x]=v
if HEUP=='A':
    # model: cremekrul in het midden, lila boog langs de onderrand, korte lila streep linksboven
    GLYPH=[".ccc.","c...c","c.c.c","c..c.",".cc.."]   # 5x5 spiraal, 1 px lijn (centrum -> buiten, open onder)
    for j,row in enumerate(GLYPH):
        for i,ch in enumerate(row):
            if ch=='c': a[31+j,35+i]=C
    for y in range(26,40):
        for x in range(28,44):
            if inell(x,y,1.0) and not inell(x,y,2.0) and 215<=ang(x,y)<=330: a[y,x]=R
    for x,y in ((34,30),(33,31),(32,32)): a[y,x]=R
else:
    # B: schouderspiraal-stijl (lila/lijn/bruin + cremeboog) kleiner, binnen de dijrand
    COLB={'lila':R,'lijn':d,'creme':C,'kern':d}
    o=spiral(36.0,33.6,3.9,3.0,boog=(300,210))
    for (x,y),k in o.items():
        if inell(x,y,1.0) and a[y,x] not in (0,K): a[y,x]=COLB.get(k,M)
n_heup=int((a!=base).sum())
np.save(f'stap4_{HEUP}.npy',a); print('heup',HEUP,n_heup)
# 5. borst: spiraal (zelfde 5x5-vorm, gespiegeld) in donkerlila op het lichte borstvlak; pootkrul van r2 strak in donkerlila
GLYPH=[".ccc.","c...c","c.c.c","c..c.",".cc.."]
n_borst=0
for j,row in enumerate(GLYPH):
    for i,ch in enumerate(row[::-1]):
        x,y=14+i,22+j
        if ch=='c' and a[y,x] not in (0,K): 
            if a[y,x]!=P: n_borst+=1
            a[y,x]=P; frozen[y,x]=True
for (x,y) in ((3,24),(4,24),(3,25),(3,26),(4,26),(5,26)):
    if a[y,x]!=P: a[y,x]=P; n_borst+=1
    frozen[y,x]=True
a[25,4]=d; frozen[25,4]=True
# 6. ontkorrelen (Krassault): bruine vulclusters < 4 px nemen de buurtint aan; lijnen, patronen, teenlijnen, dij en gezicht bevroren
for (x,y) in ((20,41),(19,42),(19,43),(32,41),(32,42),(35,41),(35,42)): frozen[y,x]=True
for y in range(26,40):
    for x in range(28,44):
        if inell(x,y): frozen[y,x]=True
frozen[7:13,9:16]=True     # oog
BR={S,M,L}; n_korrel=0
for it in range(3):
    seen=np.zeros_like(a,bool)
    for j in range(H):
        for i in range(Wd):
            if seen[j,i] or a[j,i] not in BR: continue
            c=a[j,i]; st=[(j,i)]; cl=[]; seen[j,i]=True
            while st:
                y,x=st.pop(); cl.append((y,x))
                for yy,xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                    if 0<=yy<H and 0<=xx<Wd and not seen[yy,xx] and a[yy,xx]==c: seen[yy,xx]=True; st.append((yy,xx))
            if len(cl)<4 and not any(frozen[y,x] for y,x in cl):
                cnt={}
                for y,x in cl:
                    for yy,xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
                        if 0<=yy<H and 0<=xx<Wd and a[yy,xx] in BR and a[yy,xx]!=c: cnt[a[yy,xx]]=cnt.get(a[yy,xx],0)+1
                if cnt:
                    v=max(cnt,key=cnt.get)
                    for y,x in cl: a[y,x]=v; n_korrel+=1
print('borst+poot',n_borst,'ontkorreld',n_korrel)
np.save(f'welp_r3_{HEUP}.npy',a)
# oogvarianten: oogblok x10-14, y8-11 (+ lid) 1 of 2 px naar links; vrijgekomen kolom krijgt het bruin dat rechts naast het oog ligt
eye=[(x,y) for y in range(8,12) for x in range(10,15) if a[y,x] in (K,W,G,g_,C) or (y==11 and x==10)]
for sh in (1,2):
    b=a.copy()
    for (x,y) in eye: b[y,x]=a[y,15] if a[y,15] in BR else M
    for (x,y) in eye: b[y,x-sh]=a[y,x]
    np.save(f'welp_r3_{HEUP}_oog{sh}.npy',b)
