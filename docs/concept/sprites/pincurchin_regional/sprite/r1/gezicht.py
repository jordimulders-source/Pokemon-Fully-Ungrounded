# Pincurchins ogen (en voor B de mond) 1-op-1 uit graphics/pokemon/pincurchin/anim_front.png (frame 1), indexen naar ons palet.
# A = schoon + 2x Pincurchin-oog; B = A + Pincurchin-mond, daarna de naadlijnen van A er weer overheen.
import numpy as np; from PIL import Image
from toon import save
pin=np.asarray(Image.open('../../../../../../graphics/pokemon/pincurchin/anim_front.png'))[:64]
# Pincurchin-index -> onze npy-waarde (K0 D1 s2 m3 l4 r5 R6 L7 | A8 '9'9 '7'10 '5'11 '8'12 'B'13)
MAP={3:0,10:8,9:9,7:10,5:11,8:12,11:13}
LIJF=6   # Pincurchins lijfkleur: niet overnemen (daar blijft ons lijf)
o=np.load('schoon.npy').copy()
def plak(o,y0,x0,sy,sx,h,w,uit=()):
    n=0
    for j in range(h):
        for i in range(w):
            v=pin[sy+j,sx+i]
            if v==0 or v==LIJF or v in uit: continue
            o[y0+j,x0+i]=MAP[v]; n+=1
    return n
# oog: Pincurchin x27-31, y39-43
for (y0,x0) in ((39,13),(39,28)): print('oog',y0,x0,plak(o,y0,x0,39,27,5,5))
A=o.copy()
# mond: Pincurchin x16-26, y37-45 -> modelmondplek (midden model x22,1 y44,0) => x17-27, y41-49
B=A.copy(); print('mond',plak(B,41,17,37,16,9,11,uit=(4,)))
# naad loopt eroverheen: naadlijnpixels (D) van A in de mondzone terugzetten
NAAD=[(y,x) for y in (46,48) for x in range(17,28) if A[y,x]==1]
for y,x in NAAD: B[y,x]=1
print('naadpixels over de mond',len(NAAD))
np.save('A.npy',A); np.save('B.npy',B); save(A,'A.png'); save(B,'B.png')
d=(A!=B); ys,xs=np.where(d); print('verschil A/B: px',d.sum(),'zone x',xs.min(),xs.max(),'y',ys.min(),ys.max())
