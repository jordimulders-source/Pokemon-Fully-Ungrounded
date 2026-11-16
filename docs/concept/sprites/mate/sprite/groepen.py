# Indeling van modelpixels in kleurgroepen + palet per groep (k-means op de natieve modelpixels)
import numpy as np; from PIL import Image
def masks(a):
    a=a.astype(int); R,G,B=a[...,0],a[...,1],a[...,2]; lum=0.299*R+0.587*G+0.114*B
    mx=a.max(-1); mn=a.min(-1)
    bg=mn>=225
    blk=(lum<34)&~bg
    grey=(mx-mn<22)&(lum>=60)&~bg
    green=(G>R+6)&(G>B)&~bg&~blk&~grey
    brown=~bg&~blk&~grey&~green
    return dict(bg=bg,blk=blk,grey=grey,green=green,brown=brown),lum
def kmeans(px,k,it=40):
    l=0.299*px[:,0]+0.587*px[:,1]+0.114*px[:,2]
    c=np.array([px[(l>=np.percentile(l,q-8))&(l<=np.percentile(l,q+8))].mean(0) for q in np.linspace(12,88,k)])
    for _ in range(it):
        d=((px[:,None,:]-c[None])**2).sum(-1); lab=d.argmin(1)
        c=np.array([px[lab==i].mean(0) if (lab==i).any() else c[i] for i in range(k)])
    o=np.argsort(0.299*c[:,0]+0.587*c[:,1]+0.114*c[:,2]); return c[o].round().astype(int)
if __name__=='__main__':
    a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); m,lum=masks(a)
    for g,k in (('brown',4),('green',3),('grey',3)):
        print(g,m[g].sum(),kmeans(a[m[g]],k).tolist())
    print('blk',m['blk'].sum(),np.median(a[m['blk']],0))
