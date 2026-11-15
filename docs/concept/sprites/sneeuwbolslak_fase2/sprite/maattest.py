# Maattest fase 2: model (sprite/r8_bol_r7.png, 1024) verkleind met vlakgemiddelde (alpha >= 0.45, gaten dicht),
# kleuren naar 15 clusters (alleen preview om de maat te kiezen; geen eindsprite).
import numpy as np; from PIL import Image; from collections import deque
c=np.asarray(Image.open('sprite/r8_bol_r7.png').convert('RGB')).astype(float)
fg=c.sum(2)<735
x0,x1,y0,y1=144,973,215,809
def sil(W):
    s=(x1-x0)/W; H=int(np.ceil((y1-y0)/s))
    mean=np.zeros((H,W,3)); al=np.zeros((H,W))
    for by in range(H):
        for bx in range(W):
            ya,yb=int(y0+by*s),int(y0+(by+1)*s); xa,xb=int(x0+bx*s),int(x0+(bx+1)*s)
            f=fg[ya:yb,xa:xb]; al[by,bx]=f.mean() if f.size else 0
            if f.any(): mean[by,bx]=c[ya:yb,xa:xb][f].mean(0)
    m=al>=0.45
    bg=np.zeros_like(m); q=deque([(0,0)]); bg[0,0]=1
    mp=np.pad(m,1); bgp=np.zeros_like(mp); q=deque([(0,0)]); bgp[0,0]=1
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<mp.shape[0] and 0<=xx<mp.shape[1] and not mp[yy,xx] and not bgp[yy,xx]: bgp[yy,xx]=1; q.append((yy,xx))
    m=~bgp[1:-1,1:-1]
    return m,mean,H
def kmeans(X,k=15,it=25):
    rng=np.random.default_rng(0); C=X[rng.choice(len(X),k,replace=False)]
    for _ in range(it):
        l=((X[:,None]-C[None])**2).sum(-1).argmin(1)
        C=np.array([X[l==i].mean(0) if (l==i).any() else C[i] for i in range(k)])
    return C,l
widths=(52,56,60)
vel=Image.new('RGB',(len(widths)*528,600),'white')
for k,W in enumerate(widths):
    m,mean,H=sil(W)
    C,l=kmeans(mean[m]); img=np.full((H,W,3),255.); img[m]=C[l]
    out=np.full((64,64,3),255,np.uint8); ox=(64-W)//2; oy=64-H-4; out[oy:oy+H,ox:ox+W]=img
    im=Image.fromarray(out); vel.paste(im.resize((512,512),Image.NEAREST),(k*528,0)); vel.paste(im,(k*528,525))
    print(W,H,'px',int(m.sum()))
vel.save('sprite/maattest_vel.png')
