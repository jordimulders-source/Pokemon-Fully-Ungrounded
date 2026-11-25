# Klassen per natieve modelpixel Capykart r17 (alleen indelen van modelkleuren, geen tekenen).
# 0 bg | 1 K zwart | 2 bruin (vacht + hout, één modelkleurgroep) | 3 hoepel grijs | 4 geel | 5 rood | 6 blauw | 7 groen | 8 wit (oogglans)
import numpy as np; from PIL import Image
NAMEN=['bg','K','bruin','hoepel','geel','rood','blauw','groen','wit']
def klassen(path='sprite/r17/natief.png'):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]; L=.299*R+.587*G+.114*B
    c=np.zeros(a.shape[:2],int)
    bg=a.min(2)>=225
    zw=(L<50)&~bg
    grijs=(abs(R-G)<20)&(abs(G-B)<25)&~bg&~zw
    groen=(G>R)&(G>B)&~bg&~zw&~grijs
    blauw=(B>R+15)&~bg&~zw&~grijs&~groen
    geel=(R>190)&(G>170)&(B<130)&~bg&~zw
    rood=(R>170)&(R-G>90)&(B<120)&~bg&~zw&~geel
    c[~bg]=2; c[grijs]=3; c[geel]=4; c[rood]=5; c[blauw]=6; c[groen]=7; c[zw]=1
    wit=(a.min(2)>=180)&~bg; c[wit]=8
    return a,c,L
if __name__=='__main__':
    a,c,L=klassen()
    for i,n in enumerate(NAMEN):
        m=c==i
        if m.any(): print(n,m.sum(),a[m].mean(0).astype(int),'L p10/50/90',np.percentile(L[m],[10,50,90]).astype(int))
    ch='.K~hYRBGw'
    for y in range(10,84): print('%3d '%y+''.join(ch[v] for v in c[y,11:86]))
