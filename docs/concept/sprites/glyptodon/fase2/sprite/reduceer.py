# Verkleining natief (100x100) -> 64x64: oppervlaktegewogen per spritepixel.
# Geeft per pixel: alpha (niet-wit), kfrac (lijn), gemiddelde kleur zonder lijn, en per bronklasse de fractie.
import sys; sys.path.insert(0,'../gereedschap')
import numpy as np
from kaart import klasse
X0,X1,Y0,Y1=5,95,7,88          # natieve bbox (x 5..94, y 7..87)
W=62; s=(X1-X0)/W; LEFT=1; BOT=62
H=int(np.ceil((Y1-Y0)/s)); TOP=BOT+1-H
def stats(nat):
    cls=np.array([[klasse(nat[y,x]) for x in range(100)] for y in range(100)])
    A=np.zeros((64,64)); K=np.zeros((64,64)); C=np.zeros((64,64,3)); F={}
    for sy in range(64):
        for sx in range(64):
            ya=Y0+(sy-TOP)*s; xa=X0+(sx-LEFT)*s
            tot=0; nk=0; nw=0; col=np.zeros(3); cw=0; fr={}
            for y in range(int(np.floor(ya)),int(np.ceil(ya+s))):
                for x in range(int(np.floor(xa)),int(np.ceil(xa+s))):
                    if not(0<=y<100 and 0<=x<100): wy=0
                    w=max(0,min(y+1,ya+s)-max(y,ya))*max(0,min(x+1,xa+s)-max(x,xa))
                    if w<=0: continue
                    tot+=w
                    if not(0<=y<100 and 0<=x<100): continue
                    c=cls[y,x]
                    if c=='.': continue
                    nw+=w; fr[c]=fr.get(c,0)+w
                    if c=='K': nk+=w
                    else: col+=w*nat[y,x]; cw+=w
            A[sy,sx]=nw/tot; K[sy,sx]=nk/tot
            if cw: C[sy,sx]=col/cw
            F[(sy,sx)]={k:v/tot for k,v in fr.items()}
    return A,K,C,F
if __name__=='__main__':
    nat=np.load(sys.argv[1]).astype(float)
    A,K,C,F=stats(nat)
    np.savez(sys.argv[2],A=A,K=K,C=C)
    print('TOP',TOP,'H',H,'s',s)
