# Kale reductie: natief raster (130x98 figuur, cel 5,86 px) -> sprite 62 breed (schaal 0,477), 8x8 subpunten per spritepixel.
# Regels: achtergrond als figuur < 50 %; anders het deel met het grootste aandeel; kleur = per natieve pixel de dichtstbijzijnde
# kleur uit het deelpalet (gemeen.SUB), dan de kleur met het grootste gewogen aandeel (detailtinten zwaarder, zodat
# vlekken, band, kratertjes, ringbanden en lichtranden scherp blijven i.p.v. uit te middelen).
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; import gemeen as g
a,deel,dot=g.natief()
C=np.zeros(deel.shape,int)
cache={}
for y,x in zip(*np.where(deel>=0)):
    k=deel[y,x]; key=(k,tuple(a[y,x]))
    if key not in cache: cache[key]=g.dichtst(a[y,x],g.SUB[g.NAMEN[k]])
    C[y,x]=cache[key]
C[dot]=8
X0,X1,Y0,Y1=60,190,23,121
W=62; s=W/(X1-X0)
H=int(round((Y1-Y0)*s))        # 47
OX=1; OY=61-H+1                # onderkant op rij 61
# detailtinten winnen vanaf een drempel (zoals "zwart wint vanaf 30 %" bij Dundragoon): kratertjes, vlekken, band, streep
VOORRANG={0:[(2,0.35),(6,0.35)],3:[(1,0.3),(10,0.35)],4:[(13,0.3)],1:[(8,0.4)],5:[(13,0.35)],6:[(15,0.4)]}
WT=np.ones(16); WT[[2,6,5,15,13]]=1.35; WT[8]=2.0; WT[1]=0.8
def reduceer():
    out=np.zeros((64,64),int); dl=np.full((64,64),-1)
    N=8; sub=(np.arange(N)+0.5)/N
    for j in range(H):
        for i in range(W):
            xs=np.clip((X0+(i+sub)/s).astype(int),0,deel.shape[1]-1); ys=np.clip((Y0+(j+sub)/s).astype(int),0,deel.shape[0]-1)
            dd=deel[ys[:,None],xs[None,:]].ravel(); cc=C[ys[:,None],xs[None,:]].ravel()
            if (dd>=0).mean()<0.5 and not ((dd==2).mean()>=0.3 and np.isin(cc[dd==2],[1,6,13]).mean()>=0.6): continue
            k=np.bincount(dd[dd>=0],minlength=7).argmax()
            c=np.bincount(cc[dd==k],minlength=16)*WT
            for kl_,dr in VOORRANG.get(k,[]):
                if (cc[dd==k]==kl_).mean()>=dr: c=np.zeros(16); c[kl_]=1; break
            if k==2:   # Saturnus: de dunne ring (zwart/donker/grijs) wint vanaf 30 % zodat hij doorloopt
                r=np.isin(cc,[1,6,13])&(dd==2)
                if r.mean()>=0.3: c=np.bincount(cc[r],minlength=16)*WT
            out[OY+j,OX+i]=c.argmax(); dl[OY+j,OX+i]=k
    return out,dl
def naar_sprite(xn,yn): return OX+(xn+0.5-X0)*s, OY+(yn+0.5-Y0)*s
if __name__=='__main__':
    k,dl=reduceer(); np.save(os.path.join(g.D,'kaal.npy'),k); np.save(os.path.join(g.D,'kaal_deel.npy'),dl)
    ys,xs=np.where(k>0); print('bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max(),'n',len(xs))
    from scipy import ndimage
    lab,n=ndimage.label(k>0,np.ones((3,3))); print('losse delen (8-samenhang)',n)
    import pal; pal.opslaan(k,os.path.join(g.D,'kaal.png'))
