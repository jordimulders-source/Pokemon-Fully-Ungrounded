# Bron per frame: natief raster -> (paletindex, modeltoon) op 64x64.
# frame 1: natieve cel = spritepixel (15,5 px raster). frame 2: natief 10,24 px raster, verkleind door hele rijen/kolommen
# te schrappen (factor S2, zie NOTITIES), zodat elke spritepixel een echte modelpixel is.
import json,numpy as np; from PIL import Image
from palet import nearest
NAT={'f1':'natief_f1.png','f2':'natief_f2.png'}
S2=0.76
def laad(n):
    a=np.asarray(Image.open(NAT[n]).convert('RGB')).astype(float)
    bg=a.min(axis=2)>=242
    for _ in range(2):   # grijze anti-aliasrand van Gemini (onverzadigd, licht, aan de buitenkant) = achtergrond
        p=np.pad(bg,1,constant_values=True); nb=p[:-2,1:-1]|p[2:,1:-1]|p[1:-1,:-2]|p[1:-1,2:]
        bg|= nb&(a.min(axis=2)>=170)&((a[...,2]-a[...,1])<=15)
    m=~bg; ys,xs=np.where(m); a=a[ys.min():ys.max()+1, xs.min():xs.max()+1]; m=m[ys.min():ys.max()+1, xs.min():xs.max()+1]
    lum=a@[0.3,0.6,0.1]; ni=np.where(m, nearest(a), 0); ni[(lum<23)&m]=1
    return ni.astype(int),a,m,lum
def bron(n):
    P=json.load(open('plaats.json')); ni,a,m,lum=laad(n); info=None
    if n=='f2':
        from schrap import schrap
        H,W=ni.shape; kx,wx=schrap(ni,a,m,round(W*S2),1); ky,wy=schrap(ni,a,m,round(H*S2),0)
        ni=ni[np.ix_(ky,kx)]; lum=lum[np.ix_(ky,kx)]; info=dict(weg_x=[int(v) for v in wx],weg_y=[int(v) for v in wy],natief=(W,H))
    I=np.zeros((64,64),int); L=np.zeros((64,64)); h,w=ni.shape; ox,oy=P[n]
    I[oy:oy+h,ox:ox+w]=ni; L[oy:oy+h,ox:ox+w]=lum
    return I,L,info
if __name__=='__main__':
    from schoon import save
    for n in ('f1','f2'):
        I,L,info=bron(n); save(I,'onderlaag_%s.png'%n); ys,xs=np.where(I>0)
        print(n,'figuur %dx%d'%(xs.max()-xs.min()+1,ys.max()-ys.min()+1),'bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max(),info or '')
