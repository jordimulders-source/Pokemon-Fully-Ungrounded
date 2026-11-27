# r3: vruchten segmenteren in het natieve model: elke vrucht = samenhangend stuk rood (incl. donker vruchtvlees, L>=TH) + het oogwit/de pupil
# die erin ligt (oog-component wordt bij de vrucht gevoegd die hem het meest omringt). Uitvoer: VR (199x199 label), lijst vruchten.
import numpy as np
from gemeen2 import *
from klassen2 import klassen
a,c,L=klassen(NATIEF); H,W=c.shape
TH=60
def label(m,n8=False):
    lab=np.zeros(m.shape,int);k=0
    nb=[(1,0),(-1,0),(0,1),(0,-1)]+([(1,1),(1,-1),(-1,1),(-1,-1)] if n8 else [])
    for y,x in zip(*np.where(m)):
        if lab[y,x]: continue
        k+=1; st=[(y,x)]; lab[y,x]=k
        while st:
            cy,cx=st.pop()
            for dy,dx in nb:
                yy,xx=cy+dy,cx+dx
                if 0<=yy<H and 0<=xx<W and m[yy,xx] and not lab[yy,xx]: lab[yy,xx]=k; st.append((yy,xx))
    return lab,k
R=(c==2)&(L>=TH)
VR,n=label(R); sz=np.bincount(VR.ravel())
# oog: wit (c==4) + zwart dat aan dat wit grenst (pupil/oogrand), per oog-component bij de omringende vrucht
E=(c==4); EL,ne=label(E,True)
for e in range(1,ne+1):
    ys,xs=np.where(EL==e); cnt={}
    for y,x in zip(ys,xs):
        for dy in range(-3,4):
            for dx in range(-3,4):
                yy,xx=y+dy,x+dx
                if 0<=yy<H and 0<=xx<W and VR[yy,xx] and sz[VR[yy,xx]]>=15: cnt[VR[yy,xx]]=cnt.get(VR[yy,xx],0)+1
    if cnt:
        f=max(cnt,key=cnt.get); VR[ys,xs]=f
        # pupil/zwart binnen het oog: zwart dat door dit oogwit omsloten is (binnen de bbox, met wit links en rechts op de rij)
        for y in range(ys.min(),ys.max()+1):
            row=xs[ys==y]
            if len(row):
                for x in range(row.min(),row.max()+1):
                    if c[y,x]==1: VR[y,x]=f
# vruchten die half uit de geplakte achtertros en half uit het origineel bestaan (samengesmolten bij het plakken) splitsen in achter/voor
from PIL import Image as _I
_r10=np.asarray(_I.open('sprite_r1/natief_r10.png').convert('RGB')).astype(int); _BK=np.abs(a-_r10).sum(2)>30
for f in range(1,n+1):
    m=VR==f
    if m.sum()<25: continue
    b=_BK[m].mean()
    if 0.2<b<0.8:
        n+=1; VR[m&_BK]=n
sz=np.bincount(VR.ravel(),minlength=n+1)
VRUCHTEN=[f for f in range(1,n+1) if sz[f]>=25]
if __name__=='__main__':
    from PIL import Image
    print(n,len(VRUCHTEN),sorted(sz[VRUCHTEN]))
    rng=np.random.RandomState(7); col=rng.randint(60,255,(n+1,3)); img=np.full((H,W,3),255,'uint8')
    for f in VRUCHTEN: img[VR==f]=col[f]
    img[(c==1)&~np.isin(VR,VRUCHTEN)]=0; img[c==3]=(200,230,200)
    Image.fromarray(img).crop((10,24,188,172)).resize((178*5,148*5),0).save(sys.argv[1])
