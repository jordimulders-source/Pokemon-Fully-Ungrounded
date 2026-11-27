# Gedeelde geometrie (zonder neveneffecten): zelfde transformatie als r1 (reduceer.py).
import numpy as np; from PIL import Image
import os
D=os.path.dirname(os.path.abspath(__file__))
N=np.asarray(Image.open(os.path.join(D,'../../model/r2_natief.png')).convert('RGB')).astype(float)
def _bg():
    wit=(N.sum(2)>735); bg=np.zeros_like(wit); st=[(0,0)]
    while st:
        y,x=st.pop()
        if 0<=y<100 and 0<=x<100 and wit[y,x] and not bg[y,x]:
            bg[y,x]=True; st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
    binnen=wit&~bg; lab=np.zeros(wit.shape,int); n=0
    for a,b in zip(*np.where(binnen)):
        if lab[a,b]: continue
        n+=1; st=[(a,b)]; comp=[]
        while st:
            y,x=st.pop()
            if 0<=y<100 and 0<=x<100 and binnen[y,x] and not lab[y,x]:
                lab[y,x]=n; comp.append((y,x)); st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
        if len(comp)>=8:
            for y,x in comp: bg[y,x]=True
    return bg, wit&~bg
BG,WITDETAIL=_bg()
ys,xs=np.where(~BG); X0,X1,Y0,Y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
W,H=X1-X0,Y1-Y0; F=64/max(W,H); w,h=round(W*F),round(H*F); OX=(64-w)//2; OY=64-h
def n2s(x,y):
    "natieve coord (continu) -> sprite (continu)"
    return OX+(x-X0)*F, OY+(y-Y0)*F
def s2n(i,j):
    "sprite pixel-rechthoek -> natieve rechthoek (x0,x1,y0,y1)"
    return X0+(i-OX)/F, X0+(i-OX+1)/F, Y0+(j-OY)/F, Y0+(j-OY+1)/F
