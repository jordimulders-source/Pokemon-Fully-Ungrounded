# Staryu r2 = r1-pijplijn met klassen(r2=True) (naden uit de chocoladeklasse) + 5 keurderreparaties onderaan (keuring_r1/KEURING.md).
# Staryu-koekje r1: model overnemen. Natief raster 99x99 (pitch 10,24; figuur 74x76) -> schaal 0,56, figuur vanaf x11, y12.
# Verkleinen = oppervlakteweging per spritepixel over het natieve raster; kleine kenmerken (chips, juweel, glans) winnen vanaf een drempel.
# Daarna alleen technische opschoning en reparaties naar het model; elke stap geteld.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen; from gemeen import *
a,c,L=klassen(r2=True)
UIT='sprite_r2'
H,W=c.shape
# --- voorbewerking klassen (alleen indelen): zwart dat niet aan de achtergrond grenst is een binnenlijn van chip of juweel (model: zwarte onderrand van de chips)
c2=c.copy(); rimm=np.zeros(c.shape,bool)
for v,u in zip(*np.where(c==1)):
    nb=c[max(0,v-1):v+2,max(0,u-1):u+2]
    if (nb==0).any(): continue
    n5=c[max(0,v-2):v+3,max(0,u-2):u+3]
    c2[v,u]=4 if (n5==4).sum()>(n5==2).sum() else 2 if (n5==2).any() else 3
    rimm[v,u]=True
# juweelglans (lichtroze) valt in de chipklasse door lage verzadiging: binnen het juweelvak -> juweel
for v in range(40,58):
    for u in range(37,56):
        if c2[v,u]==2 and (c2[max(0,v-2):v+3,max(0,u-2):u+3]==4).sum()>=4: c2[v,u]=4
c=c2
def tnD(l): return 3 if l<140 else 4 if l<188 else 5
def tnC(l): return 6 if l<75 else 7
def tnJ(l): return 9 if l<55 else 10 if l<88 else 11 if l<135 else 12 if l<195 else 13
TC=0.35; TJ=0.35; TCH=0.18; TJG=0.20; TK=0.30
o=np.zeros((64,64),int)
for Y in range(64):
    for X in range(64):
        f=np.zeros(5); lum=np.zeros(5); fch=0; fjg=0; frim=0; fj={}
        for u,v,w in overlap(X,Y,W,H):
            k=c[v,u]; f[k]+=w; lum[k]+=w*L[v,u]
            if k==2 and L[v,u]>=140: fch+=w
            if k==2 and (rimm[v,u] or L[v,u]<30): frim+=w
            if k==4: t=tnJ(L[v,u]); fj[t]=fj.get(t,0)+w
        tot=f[1:].sum()
        if tot<0.5: continue
        if f[1]>=TK: o[Y,X]=1; continue
        if f[4]>=TJ:
            o[Y,X]=max(fj,key=fj.get); continue   # juweel: meest voorkomende modeltint (geen gemiddelde, anders mengen de strepen)
        if f[2]>=TC:
            o[Y,X]=8 if fch>=TCH else 6 if frim/f[2]>=0.40 else 7; continue
        o[Y,X]=tnD(lum[3]/f[3]) if f[3]>0 else 4
kaal=o.copy(); opslaan(kaal,UIT+'/kaal.png')
if len(sys.argv)>1 and sys.argv[1]=='kaal':
    toon(o,8,60,6,58); sys.exit()

tel={}
def stap(n,v,o): tel[n]=tel.get(n,0)+int((v!=o).sum())
GRP={k:(DEEG if k in DEEG else CHOC if k in CHOC else JUW) for k in range(2,14)}
# --- 1. chipglans: per glanscluster van het model (lichtroze in de chip) precies één glanspixel op de gemeten plek; reductieglans elders -> chipmidden ---
v=o.copy()
o[o==8]=7
A,C0,L0=klassen(r2=True)
lab,n=label((C0==2)&(L0>=140))
for i in range(1,n+1):
    pts=np.argwhere(lab==i); vv,uu=pts.mean(0)
    if 38<=uu<=56 and 40<=vv<=57: continue   # juweelglans, niet een chip
    X=int((uu+.5-U0)*S+X0); Y=int((vv+.5-V0)*S+Y0)
    kand=[(abs(dx)+abs(dy),Y+dy,X+dx) for dy in (-1,0,1) for dx in (-1,0,1) if o[Y+dy,X+dx] in (6,7)]
    if kand: _,yy,xx=min(kand); o[yy,xx]=8
stap('chipglans',v,o)
# --- 1b. juweelrand: het model heeft een gesloten donkere ring (boven/links donkerrood, onder/rechts donkerst); reductie liet gaten ---
v=o.copy()
for Y,X in zip(*np.where(np.isin(o,list(JUW)))):
    nb=lambda dy,dx: o[Y+dy,X+dx] not in JUW
    if nb(1,0) or nb(0,1): o[Y,X]=9
    elif nb(-1,0) or nb(0,-1): o[Y,X]=10 if v[Y,X]!=9 else 9
stap('juweelrand',v,o)
# --- 2. buitenlijn: geen open of lichte rand. Achtergrond rechts/onder = zwart (schaduwkant); lichtkant = selout 2. Zwart uit het model blijft zwart. ---
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
# --- 3. ontkorrelen deeg: tintvlekjes < 3 px (lichtste < 2) nemen de meest voorkomende deegbuurtint aan; chips, juweel en lijnen niet ---
def ontkorrel(o):
    for k,minim in ((3,3),(4,3),(5,3)):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=minim: continue
            buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[Y+dy,X+dx] in (3,4,5) and o[Y+dy,X+dx]!=k]
            if buur: o[m]=max(set(buur),key=buur.count)
v=o.copy(); ontkorrel(o); ontkorrel(o); stap('ontkorrelen deeg',v,o)
# --- 3b. barstjes: de 1-px barstlijnen in het deeg vallen bij 0,56x weg. Elke dunne donkere deegpixel van het model (L<135, weinig donker deeg
#     in zijn 5x5-buurt, >=3 natieve px van de rand) wordt naar zijn spritepixel geprojecteerd en daar deegschaduw (alleen op midden/licht deeg). ---
v=o.copy()
def buren(m,r):
    p=np.pad(m.astype(int),r); return sum(p[r+dy:r+dy+m.shape[0],r+dx:r+dx+m.shape[1]] for dy in range(-r,r+1) for dx in range(-r,r+1))
donker=(C0==3)&(L0<135)
dicht=buren(donker,2)
barst=donker&(dicht<=11)&(buren(C0==0,3)==0)
lb,nb=label(barst)
for i in range(1,nb+1):
    if (lb==i).sum()<6: barst[lb==i]=False   # alleen echte lijnen (>= 6 natieve px), geen losse vlekjes
for vv,uu in zip(*np.where(barst)):
    X=int((uu+.5-U0)*S+X0); Y=int((vv+.5-V0)*S+Y0)
    if o[Y,X] in (4,5): o[Y,X]=3
stap('barstjes',v,o)
# --- 3c. tweede ontkorrelronde alleen voor midden/licht deeg (barstlijnen bevroren): splinters < 3 px tussen barst en licht nemen de buurtint 4/5 aan ---
v=o.copy()
for k in (4,5):
    lab,n=label(o==k,acht=False)
    for i in range(1,n+1):
        m=lab==i
        if m.sum()>=3: continue
        buur=[o[Y+dy,X+dx] for Y,X in zip(*np.where(m)) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if o[Y+dy,X+dx] in (4,5) and o[Y+dy,X+dx]!=k]
        if buur: o[m]=buur[0]
stap('ontkorrelen na barstjes',v,o)
# --- 4. losse zwarte pixels binnen de figuur -> deegschaduw ---
v=o.copy()
for Y,X in zip(*np.where(o==1)):
    if all(o[Y+dy,X+dx]!=0 for dy in (-1,0,1) for dx in (-1,0,1)) and not any(o[Y+dy,X+dx]==1 for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx): o[Y,X]=3
stap('losse zwarte pixel',v,o)
# --- 5. keurderreparaties r1 (keuring_r1/KEURING.md), elk op gemeten modelhelderheid; assert op de oude waarde ---
REP=[((11,29),1,2),   # 1: zwart/selout om en om bij de linkerarmtip -> selout; zwart begint op (12,31)
     ((24,32),6,3),((24,33),6,3),   # 2: chiprand tegen de juweelring -> deegschaduw (model gem. 142/119, deeg ertussen)
     ((20,36),3,2),   # 3: naad uit de inkeping, model gem. 94 -> selout (na de klassenreparatie stond hier al 3 i.p.v. chipbruin)
     ((30,13),4,3),((31,13),4,3),((31,14),4,3),((29,15),4,5),((29,16),4,5)]   # 4: bovenarm naar de modelhelderheid (150/135/141 -> 3; 186/197 -> 5)
v=o.copy()
for (X,Y),oud,nieuw in REP:
    assert o[Y,X]==oud,((X,Y),o[Y,X],oud); o[Y,X]=nieuw
# 5 (optioneel): (26,35) staat al op 9 (donkerst); geen wijziging nodig
assert o[35,26]==9
stap('keurderreparaties r1',v,o)
if __name__=='__main__':
    toon(o,8,60,6,58); print(tel, 'totaal',sum(tel.values()))
    opslaan(o,UIT+'/staryu_r2.png')
