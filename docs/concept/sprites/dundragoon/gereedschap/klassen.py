# Klassen per natieve modelpixel Dundragoon (alleen indelen van modelkleuren, geen tekenen).
# 0 bg, 1 K zwart, 2 Y geel (lijf/kop/boor/poten/hoorn?), 3 B blauw (kaak, banden, buik, oogring), 4 W vleugel/hoorn (lichtblauw-wit)
import numpy as np; from PIL import Image
NAMEN=['bg','K','Y','B','W']
def klassen(path='gereedschap/natief.png'):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]; L=.299*R+.587*G+.114*B
    c=np.zeros(a.shape[:2],int)
    bg=a.min(2)>=235
    zw=(L<40)&~bg
    geel=(R>B+35)&~bg&~zw
    blauw=(B>R+15)&~bg&~zw&~geel
    c[geel]=2; c[blauw&(L<150)]=3; c[blauw&(L>=150)]=4; c[zw]=1
    rest=~bg&(c==0)
    c[rest]=np.where(L[rest]<90,1,np.where(L[rest]<160,3,4))
    return a,c,L
if __name__=='__main__':
    a,c,L=klassen()
    for i,n in enumerate(NAMEN):
        m=c==i; print(n,m.sum(), a[m].mean(0).astype(int) if m.any() else '', 'L p10/50/90', np.percentile(L[m],[10,50,90]).astype(int) if m.any() else '')
    ch='.KYBW'
    for y in range(4,94): print('%3d '%y+''.join(ch[v] for v in c[y,3:93]))
