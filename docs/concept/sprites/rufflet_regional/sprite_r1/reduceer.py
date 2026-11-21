# Kale 2x-reductie van natief.png: achtergrond = flood fill vanaf de rand (min>=244); per 2x2-vak dekking>=2 cellen,
# lijnregel: >=2 donkere cellen (lum<70) -> donkerste kleur; anders vlakgemiddelde -> dichtstbijzijnde modelkleur (kmeans 16).
import numpy as np, sys; from PIL import Image
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); H,W=a.shape[:2]
cand=a.min(2)>=244; bg=np.zeros((H,W),bool); st=[(y,x) for y in range(H) for x in (0,W-1)]+[(y,x) for x in range(W) for y in (0,H-1)]
while st:
    y,x=st.pop()
    if 0<=y<H and 0<=x<W and cand[y,x] and not bg[y,x]: bg[y,x]=1; st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
# ingesloten achtergrond tussen de poten (pure wit >=246, y73-83 x48-56; lijf is creme 242,242,234)
enc=(a.min(2)>=246)&~bg; enc[:70]=0; enc[85:]=0; bg|=enc
np.save("bg.npy",bg)
lum=a@[0.299,0.587,0.114]; dark=(lum<70)&~bg
# modelpalet: kmeans op de figuurpixels
X=a[~bg]; rng=np.random.default_rng(1); C=X[rng.choice(len(X),16,replace=False)]
for _ in range(40):
    l=((X[:,None]-C[None])**2).sum(-1).argmin(1)
    C=np.array([X[l==k].mean(0) if (l==k).any() else C[k] for k in range(16)])
C=C[np.argsort(C@[0.299,0.587,0.114])]; np.save('model_pal.npy',C)
def red(oy,ox):
    h,w=(H-oy)//2,(W-ox)//2; o=np.zeros((h,w),int); avg=np.zeros((h,w,3)); cov=np.zeros((h,w))
    for j in range(h):
        for i in range(w):
            sl=(slice(oy+2*j,oy+2*j+2),slice(ox+2*i,ox+2*i+2)); m=~bg[sl]; cov[j,i]=m.sum()/4
            if m.sum()<2: continue
            px=a[sl][m]; avg[j,i]=px.mean(0)
            if dark[sl].sum()>=2: v=a[sl][dark[sl]].mean(0)
            else: v=px.mean(0)
            o[j,i]=((C-v)**2).sum(1).argmin()+1
    return o,avg,cov
best=None
for oy in (0,1):
    for ox in (0,1):
        o,avg,cov=red(oy,ox); ys,xs=np.where(o>0); print(oy,ox,'bbox',xs.max()-xs.min()+1,ys.max()-ys.min()+1,'px',(o>0).sum())
        np.save(f'kaal_{oy}{ox}.npy',o)
        if (oy,ox)==(int(sys.argv[1]),int(sys.argv[2])) if len(sys.argv)>2 else (oy,ox)==(1,0):
            np.save('kaal.npy',o); np.save('avg.npy',avg); np.save('cov.npy',cov)
print(np.round(C).astype(int).tolist())
