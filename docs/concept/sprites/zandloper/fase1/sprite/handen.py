# Handen terug op het raster (RotSprite): r3-hand op zijn eigen natieve raster -> Scale2x x3 -> 44 graden draaien
# (zoals plak_handen.py) -> stemmen op het spriteraster (pitch T) -> op de plek van de modelhand.
import sys; from gemeen import *
G='../gemini/'
r3=np.asarray(Image.open(G+'r3.png').convert('RGB'))
def natief_r3(box):
    x0,y0,x1,y1=box; best=None
    sub=r3[y0:y1,x0:x1].astype(int)
    # fase zoeken met pitch 10.24
    gx=np.abs(np.diff(sub,axis=1)).sum(2).sum(0); gy=np.abs(np.diff(sub,axis=0)).sum(2).sum(1)
    def ph(g):
        return max(np.arange(0,NP,0.25),key=lambda p:g[np.clip(np.round(np.arange(p,len(g)-1,NP)).astype(int),0,len(g)-1)].mean())
    px,py=ph(gx),ph(gy)
    xs=np.arange(px+NP/2+0.5,x1-x0,NP); ys=np.arange(py+NP/2+0.5,y1-y0,NP)
    out=np.zeros((len(ys),len(xs)),int)
    for j,y in enumerate(ys):
        for i,x in enumerate(xs):
            c=np.median(sub[int(y)-2:int(y)+3,int(x)-2:int(x)+3].reshape(-1,3),axis=0)
            out[j,i]=0 if c.min()>232 else klasse(c[None])[0]
    out[np.isin(out,[2,15])]=11; out[np.isin(out,[3,4,5,6])]=12   # zand-/grijsklassen in hout = houttinten
    return out
def scale2x(A):
    H,W=A.shape; P=np.pad(A,1,mode='edge'); O=np.zeros((2*H,2*W),int)
    B=P[:-2,1:-1];D=P[1:-1,:-2];F=P[1:-1,2:];Hh=P[2:,1:-1];E=A
    c=(B!=Hh)&(D!=F)
    O[0::2,0::2]=np.where(c&(D==B),D,E); O[0::2,1::2]=np.where(c&(B==F),F,E)
    O[1::2,0::2]=np.where(c&(D==Hh),D,E); O[1::2,1::2]=np.where(c&(Hh==F),F,E)
    return O
def draai(A,hoek):
    im=Image.fromarray(A.astype('uint8'),'L').rotate(hoek,resample=Image.NEAREST,expand=True,fillcolor=0)
    return np.array(im).astype(int)
def omlaag(A,f):
    H=int(np.ceil(A.shape[0]/f)); W=int(np.ceil(A.shape[1]/f)); O=np.zeros((H,W),int)
    for j in range(H):
        for i in range(W):
            b=A[int(round(j*f)):int(round((j+1)*f)),int(round(i*f)):int(round((i+1)*f))].ravel()
            h=np.bincount(b,minlength=16)/max(1,len(b))
            if h[0]>0.5: continue
            h[0]=0; O[j,i]=1 if h[1]>=0.3 else h.argmax()
    return O
def hand(box,hoek=-44):
    N=natief_r3(box); U=scale2x(scale2x(scale2x(N)))       # 8x
    R=draai(U,hoek); f=8*(geo()['T']/NP)
    return N,omlaag(R,f)
if __name__=='__main__':
    for nm,box in [('L',(280,525,425,640)),('R',(615,380,735,505))]:
        N,h=hand(box); print(nm,N.shape,h.shape)
        for r in h: print(''.join(CH[v] for v in r))
