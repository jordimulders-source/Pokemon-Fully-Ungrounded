# tint.py: Gen 3-tintopbouw (Gnomad/Regirock) op alle vlakken; vormen en lijnen blijven zoals ze zijn.
# Vlak = 4-samenhangende vlakpixels van één materiaal tussen de lijnen. Per vlak: licht waar het vlak linksboven open is,
# schaduwsikkel waar het rechtsonder open is (de rand volgt de vorm), midden binnenin. Grote vlakken: licht 2 px diep linksboven.
import numpy as np; from PIL import Image; from scipy import ndimage as nd
O=np.load('na_vorm.npy'); Z=np.load('zone.npy'); r6=Image.open('r6.png')
def mat(y,x):
    z=Z[y,x]
    if z in (2,3,4): return 'licht'
    if z in (5,6,7,8,9): return 'roze'
    if z==12: return 'blauw'
    return 'steen'
T={'steen':(3,4,5),'licht':(12,13,14),'roze':(7,8,15),'blauw':(9,10,11)}
L={'steen':{1,2},'licht':{1,2,4},'roze':{1,6,2},'blauw':{1,9,2}}
S=O>0
M=np.full((64,64),'',object); F=np.zeros((64,64),bool)
for y,x in zip(*np.where(S)):
    m=mat(y,x); v=O[y,x]
    if Z[y,x] in (10,11,13,14): continue   # riem, stok, zolen: r6-tinten waren al goed (licht/midden/schaduw per rij)
    if v in T[m] and not (m=='blauw' and v==9) and not (m=='steen' and v==2): M[y,x]=m; F[y,x]=True
uit=O.copy()
def loop(c,y,x,dy,dx):
    n=0
    while 0<=y+dy<64 and 0<=x+dx<64 and c[y+dy,x+dx]: y+=dy; x+=dx; n+=1
    return n
def ratio(c,y,x):
    tl=(loop(c,y,x,-1,0)+loop(c,y,x,0,-1)+loop(c,y,x,-1,-1))/3+0.5; br=(loop(c,y,x,1,0)+loop(c,y,x,0,1)+loop(c,y,x,1,1))/3+0.5
    return tl/(tl+br)
ROTS=np.zeros((64,64),bool); ROTS[4:20,40:51]=True; ROTS&=(Z==1)
G=S.copy()   # hele figuur: globale lichtrichting (rechterkant/onderkant van de figuur ligt in de schaduw)
LI,SH,WG,WM=0.38,0.62,0.3,0.5
d=np.load('meet6.npz'); hel=d['hel']
NORM={}
for m in T:
    v=np.array([hel[y,x] for y,x in zip(*np.where(F&(M==m))) if hel[y,x]>0]); NORM[m]=np.percentile(v,[10,50,90])
for m in T:
    lab,n=nd.label(F&(M==m))
    for i in range(1,n+1):
        c=lab==i; k=c.sum(); ys,xs=np.where(c); sh,mid,li=T[m]
        for y,x in zip(ys,xs):
            r=(1-WG)*ratio(c,y,x)+WG*ratio(G,y,x)          # vorm: 0 linksboven .. 1 rechtsonder
            lo,me,hi=NORM[m]
            if hel[y,x]>0: r=(1-WM)*r+WM*np.clip(0.5-(hel[y,x]-me)/(hi-lo),0,1)   # + gemeten modelhelderheid (mediaan = midden)
            if 4<k<=12: r=ratio(c,y,x)                     # kleine vormen (arm): eigen licht/midden/schaduw, los van de omgeving
            if k<=4: t=mid if r<SH else sh
            else: t=li if r<LI else sh if r>(0.72 if m=='blauw' else SH) else mid
            if ROTS[y,x] and hel[y,x]>0:          # mutspunt + rugrots: tinten rechtstreeks uit het model (lichte schuine voorkant, donkere zijkant)
                t=3 if hel[y,x]<110 else 4 if hel[y,x]<145 else 5
            uit[y,x]=t
PLAAT=np.zeros((64,64),int); PS={}; nr=0
for m in T:
    lab,n=nd.label(F&(M==m))
    for i in range(1,n+1): nr+=1; PLAAT[lab==i]=nr; PS[nr]=(lab==i).sum()
# vlekjes: tintvlakjes < 3 px gaan op in de meest voorkomende buurtint van hetzelfde vlak
for ronde in range(2):
    for m in T:
        for t in T[m]:
            lab,n=nd.label((uit==t)&F&(M==m))
            for i in range(1,n+1):
                c=lab==i
                if c.sum()>=3: continue
                pl=PLAAT[c].max(); grens=2 if PS.get(pl,99)<=12 else 3   # kleine vorm: 2-px licht/schaduw mag
                if c.sum()>=grens: continue
                for y,x in zip(*np.where(c)):
                    nb=[uit[y+dy,x+dx] for dy,dx in ((0,1),(0,-1),(1,0),(-1,0)) if F[y+dy,x+dx] and M[y+dy,x+dx]==m and uit[y+dy,x+dx]!=t]
                    if nb: uit[y,x]=max(set(nb),key=nb.count)
# losse lijnpixels in het haar (1-px strengen) -> donkerste haartint; schouderhoek (46,22) sluit aan op de lijn 2 ernaast
for y,x in ((17,15),(17,17)):
    if uit[y,x]==4: uit[y,x]=12
uit[22,46]=2
for y in range(1,63):              # laatste losse tintpixels -> meest voorkomende buurtint (8-buren) van hetzelfde materiaal
    for x in range(1,63):
        v=uit[y,x]
        if not F[y,x] or any(uit[y+dy,x+dx]==v for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx): continue
        nb=[uit[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and F[y+dy,x+dx] and M[y+dy,x+dx]==M[y,x]]
        if nb: uit[y,x]=max(set(nb),key=nb.count)
np.save('na_tint.npy',uit)
p=Image.fromarray(uit.astype('uint8'),'P'); p.putpalette(r6.getpalette()); p.save('na_tint.png',transparency=0)
