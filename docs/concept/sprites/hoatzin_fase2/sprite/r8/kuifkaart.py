# kuifkaart: aandeel bruin (strengen) per spritecel, gemeten op het volle 1024-model; uitvoer kuif_t.npy (bruin, donker, licht)
import numpy as np; from PIL import Image
M=np.asarray(Image.open('../../MODEL.png').convert('RGB')).astype(float)
R,G,B=M[...,0],M[...,1],M[...,2]; L=M.mean(2)
br=(R-B>=25)&(R>G+8)&(L<200)            # bruin (rood boven blauw, geen mauve)
s=2.8888889; x0=32; y0=8
def cel(cx,cy):
    a=((x0+(cx-6)*s)*5.12-0.12,(y0+(cy-1)*s)*5.12-0.12); b=((x0+(cx-5)*s)*5.12-0.12,(y0+cy*s)*5.12-0.12)
    return slice(int(round(a[1])),int(round(b[1]))),slice(int(round(a[0])),int(round(b[0])))
out=np.zeros((3,64,64))
for cy in range(64):
  for cx in range(64):
    sl=cel(cx,cy)
    if sl[0].start<0 or sl[1].start<0 or sl[0].stop>1024 or sl[1].stop>1024: continue
    m=br[sl]
    if m.size==0: continue
    out[0,cy,cx]=m.mean()
    out[1,cy,cx]=(m&(L[sl]<75)).mean()
    out[2,cy,cx]=(m&(L[sl]>=95)).mean()
np.save('kuif_t.npy',out)
# extra: gemiddelde helderheid van de bruine modelpixels per cel (kuif_L.npy)
KL=np.zeros((64,64))
for cy in range(64):
  for cx in range(64):
    sl=cel(cx,cy)
    if sl[0].start<0 or sl[1].start<0 or sl[0].stop>1024 or sl[1].stop>1024: continue
    m=br[sl]
    if m.sum()>=3: KL[cy,cx]=L[sl][m].mean()
np.save('kuif_L.npy',KL)
