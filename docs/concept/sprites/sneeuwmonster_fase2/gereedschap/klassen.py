# Klassen per modelpixel (alleen indelen van modelkleuren, niets tekenen).
# 0 bg | 1 K zwart (L<55) | 2 sneeuw | 3 hout | 4 grijs (band/ogen, verzadiging<30) | 5 steen donker | 6 gloed rood/oranje | 7 gloed geel
import numpy as np; from PIL import Image
from gemeen import MODEL, STEENZONE
NAMEN=['bg','K','sneeuw','hout','grijs','steen','gloed','geel']
def klassen():
    a=np.asarray(Image.open(MODEL).convert('RGB')).astype(int)
    r,g,b=a[...,0],a[...,1],a[...,2]; L=.299*r+.587*g+.114*b; sat=a.max(2)-a.min(2)
    H,W=L.shape; wit=a.min(2)>=244; bg=np.zeros_like(wit); st=[(0,0),(H-1,0),(0,W-1),(H-1,W-1)]
    for y,x in st: bg[y,x]=True
    while st:
        y,x=st.pop()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and wit[yy,xx] and not bg[yy,xx]: bg[yy,xx]=True; st.append((yy,xx))
    c=np.full((H,W),2)
    x0,y0,x1,y1=STEENZONE; zone=np.zeros((H,W),bool); zone[y0:y1,x0:x1]=True
    warm=(r-b>60)&(r>150)
    c[(r-b>35)&~zone]=3
    c[(sat<30)&(L<185)&(L>=55)&~zone&(np.arange(H)[:,None]<230)]=4
    c[L<55]=1
    c[zone&(L<120)&~warm]=5
    c[zone&warm]=6; c[zone&warm&(g>150)]=7
    c[bg]=0
    return a,c,L
if __name__=='__main__':
    a,c,L=klassen()
    for i,n in enumerate(NAMEN):
        m=c==i; print(n,m.sum(), a[m].mean(0).astype(int) if m.any() else '')
