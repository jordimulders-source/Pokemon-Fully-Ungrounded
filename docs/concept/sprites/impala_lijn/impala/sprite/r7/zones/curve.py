# modelcurve: zwarte modellijn (lum<70, voorgrond) op 1024 -> 2x verkleind -> Zhang-Suen-skelet; opgeslagen als punten in sprite-64-coordinaten
import numpy as np, json, sys
from PIL import Image
sys.path.insert(0,'.')
km=json.load(open('kaal_meta.json')); x0,y0,p=km['x0'],km['y0'],km['p']
a=np.asarray(Image.open('../referenties/model_r5.png').convert('RGB')).astype(float); L=(a*[.299,.587,.114]).sum(2)
wl=np.load('witlab.npz')['a']; bg=(wl==-2)|(wl==1)
B=((L<70)&~bg)
B2=B.reshape(512,2,512,2).mean((1,3))>0.5
def thin(B):
    B=B.copy().astype(np.uint8)
    while True:
        ch=False
        for st in (0,1):
            P=np.pad(B,1); n=[P[:-2,1:-1],P[:-2,2:],P[1:-1,2:],P[2:,2:],P[2:,1:-1],P[2:,:-2],P[1:-1,:-2],P[:-2,:-2]]
            Bn=sum(x.astype(int) for x in n)
            A=sum(((n[k]==0)&(n[(k+1)%8]==1)).astype(int) for k in range(8))
            c=((n[0]*n[2]*n[4]==0)&(n[2]*n[4]*n[6]==0)) if st==0 else ((n[0]*n[2]*n[6]==0)&(n[0]*n[4]*n[6]==0))
            d=(B==1)&(Bn>=2)&(Bn<=6)&(A==1)&c
            if d.any(): B[d]=0; ch=True
        if not ch: return B
S=thin(B2)
ys,xs=np.nonzero(S)
meta=json.load(open('r6/grid.json')); OX,OY=meta['OX'],meta['OY']
pts=np.c_[(xs*2+1-x0)/p+OX,(ys*2+1-y0)/p+OY]
np.save('/tmp/claude-0/s/curve.npy',pts)
# buitenrand van het voorgrondvlak (subpixel): randpixels van fg op 1024
fg=~bg; E=fg&~(np.roll(fg,1,0)&np.roll(fg,-1,0)&np.roll(fg,1,1)&np.roll(fg,-1,1))
ys,xs=np.nonzero(E); np.save('/tmp/claude-0/s/rand.npy',np.c_[(xs+.5-x0)/p+OX,(ys+.5-y0)/p+OY])
print(len(pts))
