# Klassen per natieve modelpixel: . achtergrond, K zwart, o donkere olijflijn, Y geel licht, y geel donker, B blauw, b blauw donker, R rood, W wit
from PIL import Image; import numpy as np
def klas(a):
    a=a.astype(int); R,G,B=a[...,0],a[...,1],a[...,2]; L=0.299*R+0.587*G+0.114*B
    c=np.full(a.shape[:2],'.',dtype='<U1')
    fig=a.min(2)<215
    c[fig&(L<45)]='K'
    olive=fig&(L>=45)&(R>B+25)&(L<110)
    c[olive]='o'
    yel=fig&(R>140)&(G>110)&(R>B+60)
    c[yel&(L<175)]='y'; c[yel&(L>=175)]='Y'
    blue=fig&(B>R+25)&(L>=45)
    c[blue&(L<88)]='b'; c[blue&(L>=88)]='B'
    c[fig&(R>G+60)&(R>B+50)&(L>=45)]='R'
    c[fig&(a.min(2)>=150)&(L>=180)]='W'
    c[fig&(c=='.')]='?'
    # wit binnen de figuur (ogen) is niet met de buitenkant verbonden -> W
    bg=(c=='.'); H,W=bg.shape; seen=np.zeros_like(bg); st=[(0,0)]
    while st:
        y,x=st.pop()
        if 0<=y<H and 0<=x<W and bg[y,x] and not seen[y,x]:
            seen[y,x]=True; st+= [(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
    c[bg&~seen]='W'
    return c
if __name__=='__main__':
    import sys
    c=klas(np.asarray(Image.open(sys.argv[1]).convert('RGB')))
    y0,y1=int(sys.argv[2]),int(sys.argv[3])
    print('   '+''.join(str(x%10) for x in range(25,80)))
    for y in range(y0,y1): print('%2d '%y+''.join(c[y,25:80]))
