# r10: basis ../r9/sprite_a.png. Alleen de opdrachtzones veranderen (bewijs: telling10.py).
# 1 links van het oog: dubbele bruine klont x3-5 y20-22 ontdubd naar het model (buitenrand x3 + wangljn x5/x6, ertussen de
#   lichte tan-strook uit het model); de 2 rode pixels (verre-oogvlek) worden de omringende creme. Rechteroog = r9 a.
# 2 roze (7) op de buitenrand van het lijf (buiten de kop, boven de pijl) -> gekleurde selout donkerlila (6).
# 3 kopruis: creme-tintvlakjes (3,4,5) < 3 px (4-buren) in de kopzone samengevoegd met de omringende cremetint;
#   tie-break = modelkleur van dat vlak (modelmeet.py). Roze, oog, lijnen, vlamtong niet aangeraakt.
# 4 losse zwarte randpixels tussen donkerlila -> donkerlila.
# 6 variant B = r9-spikkels; variant rond = barst linksonder weg + Jordi's barst b3 (ref_burst.json, pixels letterlijk)
#   (zie onder: 3x b3), alleen op lege pixels met 1 px lege ring, alleen rond de kop.
import json, numpy as np; from PIL import Image
from scipy import ndimage
from modelmeet import inv, M, line, red
PAL=json.load(open('../r9/palet.json')); P=np.array(PAL,float)
r9=np.asarray(Image.open('../r9/sprite_a.png')).astype(int)
SPIK=np.load('spikkels_r9.npy')                 # spikkelpixels van r9 (r5-sprite != r5-kop zonder spikkels)
H=W=64; Y,X=np.mgrid[:H,:W]
KZ=(X<26)&(Y<31)&~((X>=22)&(Y>=24))             # kopzone (zoals ../r5/kop5.py)
def modelkleur(x,y):
    pts=[inv(x+(i+.5)/8,y+(j+.5)/8) for i in range(8) for j in range(8)]
    c=np.array([M[int(120+12*v),int(106+12*u)] for u,v in pts if not line[int(120+12*v),int(106+12*u)]])
    return np.median(c,0) if len(c) else np.array([250.,234,196])
a=r9.copy(); log={}
# ---- 1
Z1={(4,20):3,(4,21):3,(4,22):4,(9,21):5,(9,22):5}
for (x,y),v in Z1.items(): a[y,x]=v
log['1 links van het oog']=Z1
# ---- 2
op=r9>0; lab,n=ndimage.label(op,np.ones((3,3))); big=lab==(np.argmax(np.bincount(lab.ravel())[1:])+1)
rb=big&~ndimage.binary_erosion(big,np.ones((3,3)),border_value=0)
Z2=(~KZ&(Y<45))|((X>=23)&(X<=34)&(Y>=15)&(Y<=31))                                  # het roze lijf: alles buiten de kop en boven de pijl (de 3 genoemde zones + rechterrand naar de hals)
m2=rb&(r9==7)&Z2; a[m2]=6; log['2 roze rand']=sorted((int(x),int(y)) for y,x in zip(*np.where(m2)))
# ---- 4
Z4=[(56,28),(19,36),(20,38)]
for x,y in Z4: a[y,x]=6
log['4 zwart']=Z4
# ---- 3
OOG=(X>=11)&(X<=14)&(Y>=20)&(Y<=23)              # rechteroog met lid: exact r9 a
TW=np.zeros((64,64),bool)                       # twinkels uit het model (plusjes), niet aanraken
for cx,cy in ((6,4),(3,8),(20,26),(15,31),(29,18)):
    for dx,dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1)): TW[cy+dy,cx+dx]=1
op9=r9>0; l9,_=ndimage.label(op9,np.ones((3,3))); BIG9=l9==(np.argmax(np.bincount(l9.ravel())[1:])+1)
CR=[3,4,5]; Z3=KZ&~SPIK&~OOG&BIG9&~TW; gewijzigd={}   # alleen de kop zelf: losse twinkels (model-sparkles) niet
for ronde in range(6):
    klein=[]
    for i in CR:
        l,k=ndimage.label((a==i)&Z3)
        for j in range(1,k+1):
            m=l==j
            if m.sum()<3: klein.append((i,m))
    if not klein: break
    for i,m in klein:
        ring=ndimage.binary_dilation(m,np.ones((3,3)))&~m
        nb=[v for v in a[ring] if v in CR and v!=i]
        if not nb: continue
        cnt={v:nb.count(v) for v in set(nb)}; top=max(cnt.values()); kand=[v for v in cnt if cnt[v]==top]
        if len(kand)>1:
            ys,xs=np.where(m); mc=np.mean([modelkleur(x,y) for x,y in zip(xs,ys)],0)
            kand.sort(key=lambda v:((P[v]-mc)**2).sum())
        for y,x in zip(*np.where(m)):
            if (x,y) not in gewijzigd: gewijzigd[(int(x),int(y))]=(int(r9[y,x]),int(kand[0]))
            a[y,x]=kand[0]
# creme-eenlingen midden in een roze streep: modelkleur daar is roze -> de omringende roze (7)
for i in CR:
    l,k=ndimage.label((a==i)&Z3)
    for j in range(1,k+1):
        m=l==j
        if m.sum()>=3: continue
        ring=ndimage.binary_dilation(m)&~m
        if all(v in (6,7,8) for v in a[ring]):
            ys,xs=np.where(m); mc=np.mean([modelkleur(x,y) for x,y in zip(xs,ys)],0)
            if np.argmin(((P[1:]-mc)**2).sum(1))+1 in (6,7,8,11,12):
                for y,x in zip(ys,xs): gewijzigd.setdefault((int(x),int(y)),None); a[y,x]=7
log['3 kopruis']={k:v for k,v in gewijzigd.items() if a[k[1],k[0]]!=r9[k[1],k[0]]}
for k in log['3 kopruis']: log['3 kopruis'][k]=(int(r9[k[1],k[0]]),int(a[k[1],k[0]]))
def save(arr,f):
    im=Image.fromarray(arr.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save(f,transparency=0)
save(a,'sprite_B.png')
# ---- 6 rond
B=json.load(open('../r3/ref_burst.json'))
def stempel(a,g,cx,cy,mag):
    g=np.array(g); gh,gw=g.shape; ys,xs=np.where(g>0); my,mx=int(round(ys.mean())),int(round(xs.mean())); o=a.copy()
    for y in range(H):
        for x in range(W):
            if a[y,x]!=0 or not mag[y,x]: continue
            if any(0<=y+dy<H and 0<=x+dx<W and a[y+dy,x+dx]>0 for dy in (-1,0,1) for dx in (-1,0,1)): continue
            gy,gx=y-cy+my,x-cx+mx
            if 0<=gy<gh and 0<=gx<gw and g[gy,gx]>0: o[y,x]={1:6,2:7,3:8}[g[gy,gx]]
    return o
b=a.copy(); LO=SPIK&(X<=26)&(Y>=28); b[LO]=0
# kop = hoofdmassa links van de hals; spikkels alleen op lege pixels binnen 6 px van de kop (x<=27, y<=35), 1 px lege ring.
# Drie keer Jordi's kleine barst b3 (dezelfde als de bovenste spikkels): links, onder en rechtsonder van de kop; de kop zelf
# dekt het midden af, zodat alleen de buitenste stralen rond de kop overblijven (net als bij de bovenste).
op=b>0; lab,n=ndimage.label(op,np.ones((3,3))); big=lab==(np.argmax(np.bincount(lab.ravel())[1:])+1)
dist=ndimage.distance_transform_edt(~(big&(X<=24)&(Y<=31)))
MAG=(dist<=6)&(X<=27)&(Y<=35)
for cx,cy in ((2,20),(9,31),(18,32)): b=stempel(b,B['b3'],cx,cy,MAG)
save(b,'sprite_rond.png')
log['6 rond: barst linksonder weg']=int(LO.sum()); log['6 rond: nieuwe spikkelpixels']=int(((b>0)&(a==0)).sum())
json.dump({k:(v if not isinstance(v,dict) else {str(kk):vv for kk,vv in v.items()}) for k,v in log.items()},open('wijzigingen.json','w'),indent=0)
for k,v in log.items(): print(k, len(v) if hasattr(v,'__len__') else v)
