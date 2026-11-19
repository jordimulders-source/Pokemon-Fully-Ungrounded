# Snavel van Soulibri r1 verlengen met zijn eigen pixels: tip verschuiven langs de periode (16,16) en het gat vullen met kopieën van één periodeplak. Niets getekend.
from PIL import Image
import numpy as np, sys
src=Image.open('r1_bijna.png').convert('RGB'); a=np.array(src)
nw=(a.astype(int).sum(2)<720)
H,W=nw.shape
beak=nw.copy(); beak[:, 78:]=False; beak[:430]=False
c=40; P=16
for k in [int(x) for x in sys.argv[1:]]:
    pad=P*k
    out=np.full((H,W+pad,3),255,np.uint8)
    out[:, pad:]=a
    # wis de oude tip (x<c) in het nieuwe beeld
    ys,xs=np.where(beak & (np.arange(W)[None,:]<c))
    out[ys,xs+pad]=255
    # tip verschoven
    out[np.clip(ys+P*k,0,H-1), xs+pad-P*k]=a[ys,xs]
    # periodeplak [c,c+P) herhalen
    ys2,xs2=np.where(beak & (np.arange(W)[None,:]>=c) & (np.arange(W)[None,:]<c+P))
    for j in range(1,k+1):
        out[np.clip(ys2+P*j,0,H-1), xs2+pad-P*j]=a[ys2,xs2]
    Image.fromarray(out).save(f'r1_snavel_k{k}.png')
    print(k, out.shape)
