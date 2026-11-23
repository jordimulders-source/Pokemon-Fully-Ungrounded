# r3: Pincurchins mond vloeiend opgeschaald per kleurlaag (methode gengas/gezicht_groter/schaal.py), bovenop de naad.
# Basis = r2/A (lijf + naad, geen mond) binnen het mondvak; buiten het mondvak = r2/B. Midden mond = r2-midden (x22,y45).
import numpy as np, sys
from PIL import Image
from toon import save
g=np.array(Image.open('../../../../../../graphics/pokemon/pincurchin/anim_front.png'))[:64].astype(int)
X0,X1,Y0,Y1=15,27,36,47      # vak rond Pincurchins mond (x16-26, y37-45) + 1 marge
sub=g[Y0:Y1,X0:X1]; H,W=sub.shape
CORE={8,9,10,11}
lab=np.zeros_like(sub)
for y in range(H):
    for x in range(W):
        v=sub[y,x]
        if v in CORE: lab[y,x]=v
        elif v==3 and np.isin(sub[max(0,y-1):y+2,max(0,x-1):x+2],list(CORE)).any(): lab[y,x]=3
classes=[c for c in np.unique(lab)]
U=8
def blur(a,s):
    r=int(3*s); k=np.exp(-0.5*(np.arange(-r,r+1)/s)**2); k/=k.sum()
    a=np.apply_along_axis(lambda m: np.convolve(m,k,'same'),0,a)
    return np.apply_along_axis(lambda m: np.convolve(m,k,'same'),1,a)
soft={c:blur(np.kron((lab==c).astype(float),np.ones((U,U))),0.30*U) for c in classes}
PRI={3:1.3,8:1.25,0:1.0}
MAP={3:0,10:8,9:9,8:12,11:13}   # Pincurchin-index -> onze waarde
# Pincurchins mondmidden in het vak: x16-26 -> 1..11 (midden 6,0), y37-45 -> 1..9 (midden 5,0) -> +0.5 voor pixelmidden
CX,CY=6.5,5.5
A2=np.load('../r2/A.npy'); B2=np.load('../r2/B.npy')
oud=np.zeros((64,64),bool); oud[41:50,17:28]=True
for s in (1.15,1.30):
    h,w=int(round(H*s)),int(round(W*s))
    m=np.zeros((h,w),int)
    for j in range(h):
        for i in range(w):
            yy=min(int((j+0.5)/s*U),H*U-1); xx=min(int((i+0.5)/s*U),W*U-1)
            m[j,i]=max(classes,key=lambda c: soft[c][yy,xx]*PRI.get(c,1.0))
    raw=m.copy()
    # technisch: 1 px lijn rondom (randpixel van de mond = lijn; bovenkant 8, onderkant 3 zoals Pincurchin), lijn binnenin -> buurvultint
    mk=m>0
    def rand(j,i): return any(not(0<=j+dj<h and 0<=i+di<w) or not mk[j+dj,i+di] for dj,di in ((0,1),(1,0),(0,-1),(-1,0)))
    for j in range(h):
        for i in range(w):
            if not mk[j,i]: continue
            if rand(j,i):
                if m[j,i] not in (3,8): m[j,i]=3 if j>=h/2 else 8
            elif m[j,i] in (3,8):
                nb=[m[j+dj,i+di] for dj,di in ((0,1),(1,0),(0,-1),(-1,0)) if m[j+dj,i+di] in (9,10,11)]
                if nb: m[j,i]=max(set(nb),key=nb.count)
    # ruis: vultint-vlakjes van 1 px -> buurvultint
    for j in range(1,h-1):
        for i in range(1,w-1):
            v=m[j,i]
            if v in (9,10,11):
                nb=[m[j+dj,i+di] for dj,di in ((0,1),(1,0),(0,-1),(-1,0))]
                if v not in nb and v!=10:   # 10 = glans (geel), mag 1 px
                    f=[n for n in nb if n in (9,11)]
                    if f: m[j,i]=max(set(f),key=f.count)
    niet=(m!=raw).sum()
    # plaatsen: midden op (22,45)
    ox=int(round(22+0.5-CX*s)); oy=int(round(45+0.5-CY*s))
    B=B2.copy(); B[oud]=A2[oud]          # oude mond weg -> lijf + naad uit r2/A
    vak=oud.copy()
    for j in range(h):
        for i in range(w):
            if m[j,i]>0: B[oy+j,ox+i]=MAP[m[j,i]]; vak[oy+j,ox+i]=True
    # ogen blijven zoals ze zijn: oogpixels gaan voor; mondpixels die tegen het oog komen worden mondlijn (8)
    oog=np.zeros((64,64),bool); oog[39:44,13:18]=True; oog[39:44,28:33]=True; oog&=np.isin(A2,[8,9,10,11])
    over=0
    for y,x in zip(*np.where(oog)):
        if B[y,x]!=A2[y,x]: over+=1
        B[y,x]=A2[y,x]
    mond=vak&~oog&(B!=A2)|(vak&~oog&np.isin(B,[12,13])&~oog)
    for y,x in zip(*np.where(vak&~oog)):
        if B[y,x] in (8,9,13) and not oog[y,x] and (y,x) not in zip(*np.where(oog)):
            if any(oog[y+dy,x+dx] for dy,dx in ((0,1),(1,0),(0,-1),(-1,0))) and B[y,x]!=A2[y,x]:
                B[y,x]=12; niet+=1
    print('oogpixels die de mond zou bedekken:',over)
    # losse mondpixel zonder mondbuur (ontstaat waar het oog de mond afsnijdt) -> terug naar lijf
    MV=(0,8,9,12,13)
    for y,x in zip(*np.where(vak&~oog&(B!=A2))):
        if not any(B[y+dy,x+dx] in (9,12,13) or (B[y+dy,x+dx]==0 and B[y+dy,x+dx]!=A2[y+dy,x+dx]) for dy,dx in ((0,1),(1,0),(0,-1),(-1,0))):
            B[y,x]=A2[y,x]; niet+=1; print('losse pixel terug',x,y)
    tag=f'B{int(round(s*100))}'
    np.save(tag+'.npy',B); save(B,tag+'.png')
    ys,xs=np.where(vak)
    print(tag,'mond',w,'x',h,'op x',ox,'y',oy,'| px niet uit de geschaalde mond:',niet,
          '| diff buiten mondvak t.o.v. r2/B:',((B!=B2)&~vak).sum(),'| mondvak x',xs.min(),xs.max(),'y',ys.min(),ys.max())
