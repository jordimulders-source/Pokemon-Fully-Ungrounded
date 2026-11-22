# Kale reductie van het r5-kophoofd: natief raster -> schaal R/D met vlakgemiddelde, donkere lijnen: donkerste wint.
# Daarna dichtstbijzijnde paletkleur (pal.py). Niets getekend.
import sys, numpy as np; from PIL import Image; from pal import PAL
R,D=int(sys.argv[1]),int(sys.argv[2])     # schaal s=R/D spritepx per natieve cel
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); m=np.load('kopmasker.npy')
ys,xs=np.where(m); a=a[ys.min():ys.max()+1, xs.min():xs.max()+1]; m=m[ys.min():ys.max()+1, xs.min():xs.max()+1]
F=np.repeat(np.repeat(a,R,0),R,1); M=np.repeat(np.repeat(m,R,0),R,1)
H,W=F.shape[0]//D+1, F.shape[1]//D+1
pad=lambda z,v: np.pad(z,((0,H*D-z.shape[0]),(0,W*D-z.shape[1]))+((0,0),)*(z.ndim-2),constant_values=v)
F=pad(F,255); M=pad(M,False)
P=np.array(PAL[1:11],float)   # kop: geen groen
lum=F@[0.3,0.59,0.11]
out=np.zeros((H,W),'uint8')
for j in range(H):
    for i in range(W):
        mm=M[j*D:(j+1)*D, i*D:(i+1)*D]
        if mm.mean()<0.5: continue
        c=F[j*D:(j+1)*D, i*D:(i+1)*D][mm]; l=lum[j*D:(j+1)*D, i*D:(i+1)*D][mm]
        dk=l<75
        col=c[dk].mean(0) if dk.mean()>=0.3 else c.mean(0)
        out[j,i]=1+int(np.argmin(((P-col)**2*[3,4,2]).sum(1)))
np.save('kop_kaal.npy',out); print('kop sprite',W,H)
im=Image.fromarray(out,'P'); im.putpalette([v for c in PAL for v in c]); im.save('kop_kaal.png',transparency=0)
Image.open('kop_kaal.png').convert('RGBA').resize((W*8,H*8),Image.NEAREST).save('kop_kaal_8x.png')
