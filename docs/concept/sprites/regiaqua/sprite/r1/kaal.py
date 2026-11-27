# Kale reductie: natief raster (81x65 figuur) -> sprite 62 breed, oppervlakteweging per spritepixel.
# Klassen per natieve pixel: achtergrond, zwart, stip, toon 0..6 (gemeen.toon). Per spritepixel 8x8 subpunten.
# Regels: achtergrond als figuur < 50 %; anders de klasse met het grootste gewogen aandeel
# (zwart x1,4, lichte tonen 4-6 x1,6, stip x2: dunne lijnen en strepen uit het model blijven scherp i.p.v. uitgemiddeld).
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from PIL import Image; import gemeen as g
a,fig,L,dot,blk=g.natief()
T=g.toon(L)
K=np.full(fig.shape,-1); K[fig]=T[fig]; K[blk]=7; K[dot]=8     # -1 bg, 0..6 toon, 7 zwart, 8 stip
X0,X1,Y0,Y1=8,89,17,82          # natieve figuurbox (81x65)
W=62; s=W/(X1-X0)               # 0,765
H=int(round((Y1-Y0)*s))         # 50
OX=1; OY=61-H+1                 # links 1 px marge (62 breed in 64), onderkant op rij 61 (zoals Regice)
WT=np.array([1,1,1,1,1.6,1.6,1.6,1.4,2.0])
def reduceer():
    out=np.zeros((64,64),int)-1; frac=np.zeros((64,64))
    N=8; sub=(np.arange(N)+0.5)/N
    for j in range(H):
        for i in range(W):
            xs=X0+(i+sub)/s; ys=Y0+(j+sub)/s
            ks=K[np.clip(ys.astype(int),0,K.shape[0]-1)[:,None],np.clip(xs.astype(int),0,K.shape[1]-1)[None,:]].ravel()
            f=(ks>=0).mean()
            if f<0.5: continue
            c=np.bincount(ks[ks>=0],minlength=9)*WT
            out[OY+j,OX+i]=c.argmax(); frac[OY+j,OX+i]=f
    return out
def naar_sprite(xn,yn): return OX+(xn+0.5-X0)*s, OY+(yn+0.5-Y0)*s
if __name__=='__main__':
    k=reduceer(); np.save(os.path.join(g.D,'kaal.npy'),k)
    ys,xs=np.where(k>=0); print('bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max(),'n',len(xs))
