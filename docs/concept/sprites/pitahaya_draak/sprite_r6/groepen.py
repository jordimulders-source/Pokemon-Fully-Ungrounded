# Natieve modelpixels indelen in kleurgroepen + per groep tonen (k-means, op echte modelkleuren gezet).
# Gedeeld door half3.py en de meetscripts. Niets getekend: alleen classificatie van modelpixels.
import numpy as np; from PIL import Image; from collections import deque
def laad(pad='natief.png'):
    a=np.asarray(Image.open(pad).convert('RGB')).astype(int); H,W=a.shape[:2]
    R,G,B=a[...,0],a[...,1],a[...,2]; lum=0.299*R+0.587*G+0.114*B
    bg0=(a.min(2)>=200)&((a.max(2)-a.min(2))<40)
    bg=np.zeros_like(bg0); q=deque((y,x) for y in range(H) for x in (0,W-1) if bg0[y,x])
    for y,x in q: bg[y,x]=1
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and bg0[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
    fg=~bg
    g=np.zeros((H,W),int)            # 0 bg, 1 zwart, 2 roze, 3 kin(mauve), 4 groen, 5 amber, 6 wit
    sat=(a.max(2)-a.min(2))/np.maximum(a.max(2),1)
    g[fg&(lum<42)]=1
    rest=fg&(g==0)
    wit=rest&(lum>=200)&(sat<0.2); g[wit]=6
    rest=fg&(g==0)
    amb=rest&(R>G)&(G>B+12)&(R>140); g[amb]=5
    rest=fg&(g==0)
    gr=rest&(G>=R); g[gr]=4
    rest=fg&(g==0)
    kin=rest&(R>G)&(np.abs(G-B)<=10)&(lum>95); g[kin]=3
    g[fg&(g==0)]=2
    return a,lum,g
def tonen(a,lum,g,grp,K):
    px=a[g==grp].astype(float); l2=px@[0.299,0.587,0.114]
    cen=np.array([px[np.argsort(l2)[int(q*(len(px)-1))]] for q in np.linspace(0.05,0.95,K)])
    for _ in range(50):
        lab=((px[:,None]-cen[None])**2).sum(2).argmin(1)
        cen=np.array([px[lab==k].mean(0) if (lab==k).any() else cen[k] for k in range(K)])
    uq=np.unique(a[g==grp],axis=0); cen=np.array([uq[((uq-c)**2).sum(1).argmin()] for c in cen])
    return cen[np.argsort(cen@[0.299,0.587,0.114])]
if __name__=='__main__':
    a,lum,g=laad()
    K={1:(20,16,24),2:(216,84,128),3:(180,108,108),4:(72,120,72),5:(230,160,40),6:(255,255,255)}
    o=np.full(a.shape,240); 
    for k,c in K.items(): o[g==k]=c
    Image.fromarray(o.astype('uint8')).crop((45,20,155,180)).resize((440,640),Image.NEAREST).save('groepen.png')
    for k in range(1,7): print(k,(g==k).sum())
    for grp,K2 in ((2,4),(3,2),(4,4),(5,2)): print(grp,tonen(a,lum,g,grp,K2).tolist())
