# Klassen per natieve modelpixel regionale Jynx (alleen indelen van modelkleuren, geen tekenen).
# 0 bg | 1 K zwart | 2 O veren (terracotta) | 3 H haar (bruin) | 4 W gezicht (wit) | 5 M lippen (purperrood)
# 6 P mondbinnenkant/tong (roze) | 7 E ogen (iris bruin/rood) | 8 C klauwen (grijsbruin)
# Achtergrond = wit dat vanaf de beeldrand bereikbaar is (het gezicht is even wit als de achtergrond).
# Haar/veren: per samenhangend gekleurd vlak (begrensd door zwart) de meerderheid van G/R >= 0,6 (haar is geler/grijzer bruin).
import numpy as np, sys; from PIL import Image
sys.path.insert(0,'gereedschap')
NAMEN=['bg','K','O','H','W','M','P','E','C']
def _label(mask):
    from gemeen import label
    return label(mask,acht=False)
def klassen(path='gereedschap/natief.png'):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    R,G,B=a[...,0],a[...,1],a[...,2]; L=.299*R+.587*G+.114*B
    h,w=L.shape
    licht=a.min(2)>=200
    bg=np.zeros((h,w),bool); st=[(y,x) for y in range(h) for x in (0,w-1)]+[(y,x) for x in range(w) for y in (0,h-1)]
    st=[p for p in st if licht[p]]
    for p in st: bg[p]=True
    while st:
        y,x=st.pop()
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<h and 0<=xx<w and licht[yy,xx] and not bg[yy,xx]: bg[yy,xx]=True; st.append((yy,xx))
    c=np.zeros((h,w),int)
    K=(L<45)&~bg
    W=(R>185)&(G>165)&(B>150)&~bg&~K
    pink=(R>170)&(B>100)&(G<170)&~bg&~K&~W
    M=(B>G+5)&(R>B)&~bg&~K&~W&~pink
    gr=G/np.maximum(R,1)
    col=~bg&~K&~W&~M&~pink
    c[K]=1; c[W]=4; c[M]=5; c[pink]=6
    lab,n=_label(col)
    for i in range(1,n+1):
        m=lab==i
        if m.sum()<=6:            # kleine vlakjes binnen het gezicht = ogen
            c[m]=7; continue
        c[m]=3 if (gr[m]>=0.6).mean()>0.5 else 2
    yy=np.arange(h)[:,None]+np.zeros((1,w),int)
    c[(c==4)&(yy>=45)]=0          # wit tussen voeten en rok = gat in het model (achtergrond)
    c[(c==6)&(yy>=40)]=3          # los roze pixeltje in het haar (58,11) = haar
    claw=(c==2)&((R-B)<50)&(L>45)&(np.arange(h)[:,None]>=78)
    c[claw]=8
    return a,c,L
if __name__=='__main__':
    a,c,L=klassen()
    for i,n in enumerate(NAMEN):
        m=c==i; print(n,m.sum(), a[m].mean(0).astype(int) if m.any() else '', 'L p10/25/50/75/90', np.percentile(L[m],[10,25,50,75,90]).astype(int) if m.any() else '')
    ch='.KOHWMPEC'
    for y in range(9,90): print('%3d '%y+''.join(ch[v] for v in c[y,12:90]))
