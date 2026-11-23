# r2 kale reductie: model_r2_s<SCHUIF> -> paletindex -> zelfde schrapplekken als r1 -> 64x64 (+ RGB-model en natieve coördinaten mee)
import sys, numpy as np
sys.path.insert(0,'claydol_sprite_r1'); from klassen import klasse
RIJEN=[16,25,27,44,52,59,63,74,79]
KOLOMMEN=[15,19,32,52,60,64,68,72,80]
def kaal(schuif=2):
    k,a=klasse('claydol_sprite_r2/model_r2_s%d.png'%schuif)
    H,W=k.shape; yy,xx=np.mgrid[0:H,0:W]
    d=lambda z:np.delete(np.delete(z,RIJEN,0),KOLOMMEN,1)
    kk,aa,ny,nx=d(k),d(a),d(yy),d(xx)
    ys,xs=np.where(kk>0); sl=(slice(ys.min(),ys.max()+1),slice(xs.min(),xs.max()+1))
    kk,aa,ny,nx=kk[sl],aa[sl],ny[sl],nx[sl]; h,w=kk.shape; oy=64-h; ox=(64-w)//2
    S=np.zeros((64,64),int); A=np.full((64,64,3),255); NY=np.full((64,64),-1); NX=np.full((64,64),-1)
    S[oy:oy+h,ox:ox+w]=kk; A[oy:oy+h,ox:ox+w]=aa; NY[oy:oy+h,ox:ox+w]=ny; NX[oy:oy+h,ox:ox+w]=nx
    return S,A,NY,NX
if __name__=='__main__':
    S,A,NY,NX=kaal(); s='.123456789KABR'
    print('   '+''.join(str(x%10) for x in range(64)))
    for y in range(45): print('%2d '%y+''.join(s[v] for v in S[y]))
