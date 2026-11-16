# r4: alleen de KOP (zone KZ van r3). Basis ../r3/sprite.png (gezicht V, spikkels B). Lijf, lijnen, pijl, twinkels,
# lijfspikkels en spikkels bevroren (diff 0, zie telling4.py).
#  1. silhouet: dekking van het model per spritepixel (meting.npz) >= DREMPEL, alleen vast aan de kop; dunne tongen/snuit
#     met een lagere drempel (DUN) als ze aan het silhouet vast zitten.
#  2. helderheid (+ goud/tan-strengen uit goudkaart.py: >= 4 natieve px -> 3, 2-3 -> hooguit 4): creme-binnenpixels naar de mediane modelhelderheid van het blok (zonder lijn/roze/glitter):
#     >= T5 -> 5 (lichtste creme), >= T4 -> 4, anders 3; tan/goud alleen waar het model donker is.
#  3. rand: lijn 2 waar het model een lijn heeft (lijnaandeel >= 0,2), anders selout naar de p15 van het blok (14 goud / 3 tan).
#  4. roze strepen: r3-pixels houden; nieuwe pixels roze 7 als de lijnkaart (../r3/kaart_roze.npy >= 2) een streep heeft.
#  5. gezicht: r3-V lijnen (../r3/gezicht_r3.json) als basis, + reparaties per pixel in gezicht4.json (zie rapport).
import json, sys, numpy as np; from PIL import Image
PAL=json.load(open('palet.json'))
base=np.asarray(Image.open('../r3/sprite.png')).astype(int); kop3=np.load('../r3/r3_kop_V.npy')
Mz=np.load('meting.npz'); cov,lijn,med,p15,roze,md=Mz['cov'],Mz['lijn'],Mz['med'],Mz['p15'],Mz['roze'],Mz['md']
P=np.array(PAL,float)
rk=np.load('../r3/kaart_roze.npy')
DREMPEL,DUN,T5,T4=0.35,0.22,218,195
H,W=base.shape; Y,X=np.mgrid[:H,:W]
KZ=(X<26)&(Y<31)&~((X>=22)&(Y>=24))
SPIK=base!=kop3
TW=np.zeros_like(KZ)
for cx,cy in [(8,6),(5,9),(29,18),(20,26),(16,29)]:
    for dx,dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1)): TW[cy+dy,cx+dx]=1
E=KZ&~SPIK&~TW                                    # bewerkbaar
DZ=((X<14)&(Y<14))|((X<10)&(Y>=19))&~((X<=4))      # dunne-delen-zone: vlamtongen linksboven en de snuit/kin linksonder
                                                  # (niet x<=4: daar ligt de modelomlijning op x=5, dekking 0,2-0,3 is lijnrand)
def n4(m,y,x): return [(y+dy,x+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<H and 0<=x+dx<W]
def comp(m,start):
    seen={start}; st=[start]
    while st:
        p=st.pop()
        for q in n4(m,*p):
            if m[q] and q not in seen: seen.add(q); st.append(q)
    return seen
# 1. silhouet
sil=(base>0)&~E | (E&(cov>=DREMPEL))
for _ in range(2):                                   # dunne delen: lagere drempel, vast aan het silhouet
    add=E&DZ&~sil&(cov>=DUN)&np.array([[any(sil[q] for q in n4(None,y,x)) for x in range(W)] for y in range(H)])
    sil|=add
lijf=comp(sil,(40,20)); L=np.zeros_like(sil)
for p in lijf: L[p]=1
sil=np.where(E,L,sil)
SZ=(X<22)&(Y<27)&(Y>6)&~((X>=18)&(Y>=24))      # alleen hier wijzigen (kop zelf); hals, bovenste vlammen rechtsboven,
sil=np.where(E&~SZ,base>0,sil)                     # lijfrand en losse vlam linksonder blijven r3
E=E&SZ
a=base.copy(); a[E&~sil]=0
def rand(y,x): return any(not sil[q] for q in n4(None,y,x)) or y in (0,H-1) or x in (0,W-1)
GEZ=json.load(open('../r3/gezicht_r3.json'))['V']['px']
KAAL='kaal' in sys.argv
G4={} if KAAL else json.load(open('gezicht4.json'))
gk=np.load('kaart_goud.npy')
def creme(y,x):
    m=med[y,x]; t=5 if m>=T5 else (4 if m>=T4 else 3)
    if gk[y,x]>=4: t=3                               # goud/tan-streng uit het model (goudkaart.py), donkerste wint
    elif gk[y,x]>=2 and t==5: t=4
    return t
for y in range(H):
    for x in range(W):
        if not(E[y,x] and sil[y,x]): continue
        v3=kop3[y,x]; k='%d,%d'%(x,y)
        if v3 in (6,7,8,1,9,10,11,12) and k not in GEZ: a[y,x]=v3; continue       # roze strepen/hals uit r3
        if v3==0 and (rk[y,x]>=2 or roze[y,x]>=0.25): a[y,x]=7 if not rand(y,x) else 6; continue
        if k in GEZ: a[y,x]=GEZ[k]; continue
        if rand(y,x):
            ks=[2,3,14,6,7]; a[y,x]=2 if lijn[y,x]>=0.2 else ks[int(((P[ks]-md[y,x])**2).sum(1).argmin())]
        else:
            a[y,x]=creme(y,x)
# 6. opschonen: creme-vlakjes (3/4/5, 8-buren) < 3 px binnen de kop nemen de meest voorkomende creme-buurtint aan
#    (alleen binnenpixels; niet de rand, niet de modelstrengen (goudkaart >= 2), niet het gezicht-vak van gezicht4.json, niet r3-pixels die niet in de bewerkzone liggen)
from scipy import ndimage
GV={tuple(map(int,k.split(','))) for k in G4 if not k.startswith('_')}
OPG=[]
if G4:
  for k in (3,4,5):
    lab,n=ndimage.label((a==k)&E,np.ones((3,3)))
    for c in range(1,n+1):
        ys,xs=np.where(lab==c)
        if len(ys)>=3: continue
        for y,x in zip(ys,xs):
            if rand(y,x) or (x,y) in GV or gk[y,x]>=2: continue        # goud/tan-strengen uit het model blijven
            nb=[a[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and a[y+dy,x+dx] in (3,4,5) and a[y+dy,x+dx]!=k]
            if len(nb)>=4: a[y,x]=max(set(nb),key=nb.count); OPG.append((int(x),int(y),k,int(a[y,x])))
  print('opgeschoond',len(OPG),OPG)
for k,v in G4.items():
    if k.startswith('_'): continue
    x,y=map(int,k.split(',')); a[y,x]=v
im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48))
im.save('sprite_kaal.png' if KAAL else 'sprite.png',transparency=0)
if not KAAL: np.save('kop4.npy',a)
d=a!=base; print('diff t.o.v. r3: kop-zone',int((d&KZ).sum()),'buiten',int((d&~KZ).sum()))
HX='.123456789ABCDEF'
if 'stil' not in sys.argv:
    for y in range(31): print('%2d'%y,''.join(HX[v] for v in a[y,:30]),'  ',''.join(HX[v] for v in base[y,:30]))
