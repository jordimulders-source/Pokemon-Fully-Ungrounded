# Klassen per natieve modelpixel (geen tekenen: alleen indelen van modelkleuren).
# 0 achtergrond (bijna-wit en verbonden met de rand) | 1 K zwart | 2 vogel (blauwgrijs) | 3 wolk (grijs) | 4 geel (vonken) | 5 wit (snavel, oogglans)
import numpy as np; from PIL import Image
NAMEN=['bg','K','vogel','wolk','geel','wit']
def klassen(path='gereedschap/natief.png'):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]; L=.299*R+.587*G+.114*B
    licht=a.min(2)>=215
    # achtergrond = bijna-wit dat met de rand verbonden is (snavelwit en oogglans liggen binnen de figuur)
    bg=np.zeros(L.shape,bool); H,W=L.shape; st=[(y,x) for y in range(H) for x in (0,W-1)]+[(y,x) for x in range(W) for y in (0,H-1)]
    for y,x in st: bg[y,x]=licht[y,x]
    st=[p for p in st if bg[p]]
    while st:
        y,x=st.pop()
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and licht[yy,xx] and not bg[yy,xx]: bg[yy,xx]=True; st.append((yy,xx))
    c=np.zeros(L.shape,int)
    geel=(R>B+40)&~bg
    c[~bg]=3
    c[(B-R>=36)&~bg]=2
    c[(L>=205)&~bg]=5
    c[geel]=4
    c[(L<45)&~bg&~geel]=1
    return a,c,L
if __name__=='__main__':
    a,c,L=klassen()
    for i,n in enumerate(NAMEN):
        m=c==i; print(n,m.sum(), a[m].mean(0).astype(int) if m.any() else '', 'L p10/50/90', np.percentile(L[m],[10,50,90]).astype(int) if m.any() else '')
    ch='.KvwYW'
    for y in range(22,106): print('%3d '%y+''.join(ch[v] for v in c[y,72:166]))
