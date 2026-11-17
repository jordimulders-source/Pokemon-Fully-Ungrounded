# Modellijnen: natieve zwarte pixels (groep 1, geen pit) -> Zhang-Suen-skelet -> per skeletpixel geprojecteerd naar het spriteraster
# (methode spooktrein fase 3, sprite_r18/lijnen.py). Levert per spritepixel het aantal skeletpixels en de componentlengte.
import numpy as np
def zhang(m):
    m=m.copy().astype(np.uint8)
    while True:
        ch=False
        for st in (0,1):
            P=np.pad(m,1)
            p2,p3,p4,p5,p6,p7,p8,p9=P[:-2,1:-1],P[:-2,2:],P[1:-1,2:],P[2:,2:],P[2:,1:-1],P[2:,:-2],P[1:-1,:-2],P[:-2,:-2]
            B=p2+p3+p4+p5+p6+p7+p8+p9
            seq=[p2,p3,p4,p5,p6,p7,p8,p9,p2]
            A=sum(((seq[i]==0)&(seq[i+1]==1)).astype(int) for i in range(8))
            if st==0: c=(p2*p4*p6==0)&(p4*p6*p8==0)
            else: c=(p2*p4*p8==0)&(p2*p6*p8==0)
            d=(m==1)&(B>=2)&(B<=6)&(A==1)&c
            if d.any(): m[d]=0; ch=True
        if not ch: return m.astype(bool)
def componenten(m):
    H,W=m.shape; lab=np.zeros((H,W),int); n=0; size={}
    for y0,x0 in zip(*np.where(m)):
        if lab[y0,x0]: continue
        n+=1; st=[(y0,x0)]; lab[y0,x0]=n; c=0
        while st:
            y,x=st.pop(); c+=1
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    yy,xx=y+dy,x+dx
                    if 0<=yy<H and 0<=xx<W and m[yy,xx] and not lab[yy,xx]: lab[yy,xx]=n; st.append((yy,xx))
        size[n]=c
    return lab,size
def projecteer(g,geo,maskextra=None):
    """g: natieve groepen; geo uit *_info.npz. Retourneert (aantal skeletpx per spritepx, max componentlengte per spritepx, skelet)."""
    S,OX,OY,bx0,by0=geo[:5]; ymin,xmin,Y0,X0,U=[int(v) for v in geo[5:]]
    m=(g==1) if maskextra is None else maskextra
    sk=zhang(m); lab,size=componenten(sk)
    cnt=np.zeros((64,64),int); ln=np.zeros((64,64),int)
    for ny,nx in zip(*np.where(sk)):
        X=int(np.floor((nx+.5-(bx0-S+OX))/S))-xmin+X0; Y=int(np.floor((ny+.5-(by0-S+OY))/S))-ymin+Y0
        if 0<=X<64 and 0<=Y<64: cnt[Y,X]+=1; ln[Y,X]=max(ln[Y,X],size[lab[ny,nx]])
    return cnt,ln,sk
