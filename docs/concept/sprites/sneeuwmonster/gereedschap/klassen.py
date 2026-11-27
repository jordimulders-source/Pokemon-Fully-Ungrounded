# Klassen per natieve modelpixel sneeuwmonster (alleen indelen van modelkleuren, geen tekenen).
# 0 bg | 1 K zwart/omlijning (L<45) | 2 S steen (grijs, verzadiging <25) | 3 B blauwe sneeuwlijn (L<175) | 4 W sneeuw
import numpy as np; from PIL import Image
NAMEN=['bg','K','S','B','W']
def klassen(path='gereedschap/natief.png'):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    L=.299*a[...,0]+.587*a[...,1]+.114*a[...,2]; sat=a.max(2)-a.min(2)
    # achtergrond = vrijwel wit en verbonden met de rand (wit hooglicht binnen de figuur blijft sneeuw)
    wit=a.min(2)>=246; H,W=wit.shape; bg=np.zeros_like(wit); st=[(0,0)]; bg[0,0]=True
    while st:
        y,x=st.pop()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and wit[yy,xx] and not bg[yy,xx]: bg[yy,xx]=True; st.append((yy,xx))
    c=np.full(a.shape[:2],4)
    c[bg]=0
    c[~bg&(L<175)&(sat>=25)]=3
    c[~bg&(L<160)&(sat<25)]=2
    c[~bg&(L<45)]=1
    return a,c,L
if __name__=='__main__':
    a,c,L=klassen()
    for i,n in enumerate(NAMEN):
        m=c==i; print(n,m.sum(), a[m].mean(0).astype(int) if m.any() else '')
    ch='.KSBW'
    for y in range(14,84): print('%3d '%y+''.join(ch[v] for v in c[y,25:73]))
