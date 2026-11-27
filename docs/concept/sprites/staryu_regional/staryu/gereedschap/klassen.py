# Klassen per natieve modelpixel Staryu-koekje (alleen indelen van modelkleuren, geen tekenen).
# 0 bg, 1 K zwart (buitenlijn), 2 C chocolade (incl. chipglans), 3 D deeg (incl. barstlijnen), 4 J juweel (rood)
import numpy as np; from PIL import Image
NAMEN=['bg','K','C','D','J']
def klassen(path='gereedschap/natief.png'):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]; L=.299*R+.587*G+.114*B
    c=np.zeros(a.shape[:2],int)
    bg=a.min(2)>=232
    zw=(L<38)&~bg
    juw=(R-G>70)&(B>=G-12)&~bg&~zw
    sat=(R-B)/np.maximum(R,1)
    choc=((L<70)|((L<130)&(sat<0.70))|(sat<0.45))&~bg&~zw&~juw
    deeg=~bg&~zw&~juw&~choc
    c[deeg]=3; c[choc]=2; c[juw]=4; c[zw]=1
    return a,c,L
if __name__=='__main__':
    a,c,L=klassen()
    for i,n in enumerate(NAMEN):
        m=c==i; print(n,m.sum(), a[m].mean(0).astype(int) if m.any() else '', 'L p10/50/90', np.percentile(L[m],[10,50,90]).astype(int) if m.any() else '')
    ch='.KCdJ'
    for y in range(9,89): print('%3d '%y+''.join(ch[v] for v in c[y,10:90]))
