# Mediaan-tinten per kleurgroep (zonder omlijning en randpixels), in 3 helderheidsbanden (k-means op L).
import sys, numpy as np; sys.path.insert(0,'gereedschap'); from klassen import klassen
def kern(c,k):
    m=c==k; mm=m.copy()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)): mm&=np.roll(m,(dy,dx),(0,1))
    return mm
def banden(a,L,m,n=3):
    v=L[m]; cs=np.quantile(v,np.linspace(0.15,0.85,n))
    for _ in range(30):
        lab=np.argmin(np.abs(v[:,None]-cs[None]),1); cs=np.array([v[lab==i].mean() if (lab==i).any() else cs[i] for i in range(n)])
    px=a[m]; out=[]
    for i in np.argsort(cs): out.append((tuple(int(x) for x in np.median(px[lab==i],0)),int((lab==i).sum())))
    return out
for pad,naam in (('natief_r5.png','r5'),('natief_r7.png','r7')):
    a,c,L=klassen(pad); H,W=c.shape; yy,xx=np.mgrid[0:H,0:W]
    kop=(xx>=60)&(xx<=115)&(yy<=65) if naam=='r5' else (xx>=35)&(xx<=70)&(yy>=35)&(yy<=78)
    print('==',naam)
    print('goud',banden(a,L,kern(c,4)))
    print('wit',banden(a,L,kern(c,5)))
    print('rood kop',banden(a,L,kern(c,3)&kop))
    print('rood pennen',banden(a,L,kern(c,3)&~kop,2) if (kern(c,3)&~kop).sum()>20 else '-')
    if (kern(c,6)).sum()>20: print('oranje',banden(a,L,kern(c,6),2))
    print('donker',banden(a,L,kern(c,2),2))
    print('lijn',banden(a,L,c==1,2))
