# r17 stap 1: natief model (r1/natief.png, 200x200) -> 3x3-modus per blok, geen mengen.
# Modelkleuren eerst in K clusters (k-means op de figuurpixels); per blok wint het meest voorkomende cluster,
# celkleur = gemiddelde van de pixels van dat cluster in dat blok (een echte modelkleur).
# Dunne lijnen (zwart, bruine kuifstrengen, lichte vleugelstrepen) die als minderheid zouden verdwijnen,
# mogen winnen bij >=3 van 9 pixels, maar nooit 2 px dik: twee buurblokken met dezelfde lijn die over de grens ligt -> alleen de sterkste.
import numpy as np, sys
from PIL import Image
PY=int(sys.argv[1]) if len(sys.argv)>1 else 7; PX=int(sys.argv[2]) if len(sys.argv)>2 else 32
OUT=sys.argv[3] if len(sys.argv)>3 else 'blad.npy'
a=np.asarray(Image.open('../r1/natief.png').convert('RGB')).astype(float)
bg=a.min(2)>225
# k-means
rng=np.random.default_rng(1)
F=a[~bg]; K=28
C=F[rng.choice(len(F),K,replace=False)]
for it in range(40):
    d=((F[:,None,:]-C[None])**2).sum(2); l=d.argmin(1)
    C=np.array([F[l==k].mean(0) if (l==k).any() else C[k] for k in range(K)])
lab=np.full(bg.shape,-1); d=((a[:,:,None,:]-C[None,None])**2).sum(3); lab=d.argmin(2); lab[bg]=-1
L=a@[.299,.587,.114]
R,G,B=a[...,0],a[...,1],a[...,2]
brown=(~bg)&(R>G+20)&(R>B+28)&(L>=40)&(L<150)          # kuifstrengen (bruin)
DL=float(sys.argv[6]) if len(sys.argv)>6 else 55
dark=(~bg)&(L<DL)&~brown
light=(~bg)&(L>=140)&(R>B-10)                           # lichte vleugelstrepen (roze-wit)
NR,NC=61,49
out=np.zeros((NR,NC,3)); win=np.full((NR,NC),-1); why=np.zeros((NR,NC),'U6')
cnt={k:np.zeros((NR,NC),int) for k in ('dark','brown','light')}
masks={'dark':dark,'brown':brown,'light':light}
def blk(r,c): return slice(PY+3*r,PY+3*r+3),slice(PX+3*c,PX+3*c+3)
for r in range(NR):
    for c in range(NC):
        ys,xs=blk(r,c); lb=lab[ys,xs].ravel()
        if lb.size<9: lb=np.concatenate([lb,np.full(9-lb.size,-1)])
        v,n=np.unique(lb,return_counts=True); w=v[n.argmax()]
        # gelijkspel: figuur boven achtergrond
        if (n==n.max()).sum()>1 and w==-1: w=v[(n==n.max())&(v!=-1)][0]
        win[r,c]=w; why[r,c]='modus'
        for k,m in masks.items(): cnt[k][r,c]=m[ys,xs].sum()
pref=['dark','brown','light']
promo=np.zeros((NR,NC),'U6')
TH={'dark':int(sys.argv[4]) if len(sys.argv)>4 else 2,'brown':3,'light':2}
for r in range(NR):
    for c in range(NC):
        ys,xs=blk(r,c)
        wl=win[r,c]
        ok=[]
        for k in pref:
            if cnt[k][r,c]>=TH[k]:
                if wl>=0 and masks[k][ys,xs].ravel()[lab[ys,xs].ravel()==wl].mean()>0.5: ok=[]; break   # lijn wint al via de modus
                ok.append(k)
        if ok: promo[r,c]=max(ok,key=lambda k:cnt[k][r,c])
# niet dikker dan 1 px: lijn over de blokgrens -> alleen het blok met de meeste lijnpixels
drop=np.zeros((NR,NC),bool)
for r in range(NR):
    for c in range(NC):
        k=promo[r,c]
        if not k: continue
        for dr,dc in ((0,1),(1,0)):
            r2,c2=r+dr,c+dc
            if r2>=NR or c2>=NC or promo[r2,c2]!=k: continue
            ys,xs=blk(r,c); ys2,xs2=blk(r2,c2); m=masks[k]
            if dc: edge=m[ys,xs.stop-1].any() and m[ys2,xs2.start].any() and (m[ys,xs.stop-1]&m[ys2,xs2.start]).any()
            else: edge=(m[ys.stop-1,xs]&m[ys2.start,xs2]).any()
            if edge:
                if cnt[k][r,c]>=cnt[k][r2,c2]: drop[r2,c2]=True
                else: drop[r,c]=True
promo[drop]=''
for r in range(NR):
    for c in range(NC):
        ys,xs=blk(r,c); px=a[ys,xs].reshape(-1,3); lb=lab[ys,xs].ravel()
        k=promo[r,c]
        if k:
            m=masks[k][ys,xs].ravel(); out[r,c]=px[m].mean(0); why[r,c]=k
        elif win[r,c]>=0:
            out[r,c]=px[lb==win[r,c]].mean(0)
            sel=lb==win[r,c]
            for kk,tag in (('light','mlight'),('dark','mdark'),('brown','mbrown')):
                if masks[kk][ys,xs].ravel()[sel].mean()>0.5: why[r,c]=tag   # modus is zelf een lijn-/streepkleur: eigen kleur houden
        else: why[r,c]='bg'
# gladde toonkaart van de VULLING (les pitahaya fase 1): modelhelderheid zonder lijn-/streeppixels, genormaliseerd vervaagd (straal SIG natief)
from PIL import ImageFilter
SIG=float(sys.argv[5]) if len(sys.argv)>5 else 2.0
w=((~bg)&~dark&~light&~brown).astype(float)
gk=np.exp(-np.arange(-6,7)**2/(2*SIG**2)); gk/=gk.sum()
def bl(z):
    z=np.apply_along_axis(lambda v: np.convolve(v,gk,'same'),0,z); return np.apply_along_axis(lambda v: np.convolve(v,gk,'same'),1,z)
TL=bl(L*w)/np.maximum(bl(w),1e-3)
toon=np.zeros((NR,NC))
for r in range(NR):
    for c in range(NC):
        ys,xs=blk(r,c); f=~bg[ys,xs]
        toon[r,c]=TL[ys,xs][f].mean() if f.any() else 0
np.save(OUT,{'rgb':out.round().astype(int),'why':why,'bg':why=='bg','toon':toon},allow_pickle=True)
print('fase',PY,PX,'figuurcellen',(why!='bg').sum(),{k:(why==k).sum() for k in pref})
