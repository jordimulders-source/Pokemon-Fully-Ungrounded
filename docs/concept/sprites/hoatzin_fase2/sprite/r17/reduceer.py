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
dark=(~bg)&(L<62)
brown=(~bg)&(R>G+25)&(R>B+25)&(L<150)&(L>=62)          # kuifstrengen (oranjebruin)
light=(~bg)&(L>=165)&(R>B-10)                           # lichte vleugelstrepen (roze-wit)
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
for r in range(NR):
    for c in range(NC):
        ys,xs=blk(r,c)
        wl=win[r,c]
        for k in pref:
            m=masks[k][ys,xs]
            if cnt[k][r,c]>=3:
                # al winnend?
                if wl>=0 and m.ravel()[lab[ys,xs].ravel()==wl].mean()>0.5 if wl>=0 and (lab[ys,xs]==wl).any() else False: break
                promo[r,c]=k; break
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
        else: why[r,c]='bg'
np.save(OUT,{'rgb':out.round().astype(int),'why':why,'bg':why=='bg'},allow_pickle=True)
print('fase',PY,PX,'figuurcellen',(why!='bg').sum(),{k:(why==k).sum() for k in pref})
