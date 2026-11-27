# Klassen per natieve modelpixel Staryu-koekje (alleen indelen van modelkleuren, geen tekenen).
# 0 bg, 1 K zwart (buitenlijn), 2 C chocolade (incl. chipglans), 3 D deeg (incl. barstlijnen), 4 J juweel (rood)
import numpy as np; from PIL import Image
NAMEN=['bg','K','C','D','J']
def klassen(path='gereedschap/natief.png',r2=False):
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
    if r2: c=naden_uit(c)
    return a,c,L
def naden_uit(c):
    # r2 (keuring r1 punt 3): donkere naden/randjes vallen door lage verzadiging in de chocoladeklasse. Gemeten: echte chips zijn
    # componenten (chocolade + binnen-zwart) van 29-55 natieve px; al het andere is <= 5 px. Componenten < 15 px buiten het juweelvak -> deeg.
    from gemeen import label
    c=c.copy(); H,W=c.shape
    bgn=np.zeros(c.shape,bool)
    for v,u in zip(*np.where(c==1)):
        if (c[max(0,v-1):v+2,max(0,u-1):u+2]==0).any(): bgn[v,u]=True
    lab,n=label(((c==2)|(c==1))&~bgn)
    for i in range(1,n+1):
        m=lab==i; p=np.argwhere(m); vv,uu=p.mean(0)
        if m.sum()>=15 or (40<=vv<=57 and 37<=uu<=56): continue
        c[m&(c==2)]=3; c[m&(c==1)]=3
    return c
if __name__=='__main__':
    a,c,L=klassen()
    for i,n in enumerate(NAMEN):
        m=c==i; print(n,m.sum(), a[m].mean(0).astype(int) if m.any() else '', 'L p10/50/90', np.percentile(L[m],[10,50,90]).astype(int) if m.any() else '')
    ch='.KCdJ'
    for y in range(9,89): print('%3d '%y+''.join(ch[v] for v in c[y,10:90]))
