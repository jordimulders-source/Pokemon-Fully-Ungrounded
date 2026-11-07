# Variant (Jordi 7 nov: "het stuk onder het hoofd moet korter, hij moet niet smaller"):
# de band onder de kop (y YA..YB: borst en voorpootjes) verticaal ingedrukt met factor s.
# Kop, sprieten en bolletjes erboven schuiven onvervormd omlaag; voetjes/onderrand (y >= YB) onveranderd.
# Per kolom: volle indrukking voor x >= XR (kop/voorlijf), geen voor x <= XL (achterlijf blijft precies zo), lineair ertussen.
import numpy as np, sys
from PIL import Image
src=np.asarray(Image.open('../referenties/jordi_gemini.png')).astype(int)
s=float(sys.argv[1]); YA,YB=578,690; XL,XR=int(sys.argv[2]),int(sys.argv[3])
H,W,_=src.shape; band=YB-YA
out=np.empty_like(src); out[:]=src[5,5]
for x in range(W):
    t=min(1,max(0,(x-XL)/(XR-XL))); sx=1-(1-s)*t
    nb=band*sx; shift=band-nb
    for yn in range(H):
        if yn>=YB: ys=yn
        elif yn>=YB-nb: ys=YB-(YB-yn)/sx
        else: ys=yn-shift
        yi=int(round(ys))
        if 0<=yi<H: out[yn,x]=src[yi,x]
Image.fromarray(out.astype('uint8')).save(f'laag_{int(s*100)}.png')
