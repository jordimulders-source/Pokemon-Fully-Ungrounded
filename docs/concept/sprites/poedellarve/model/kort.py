# Variant: achterlijf horizontaal ingedrukt, kop/voorlijf (x >= X1) onveranderd.
import numpy as np, sys
from PIL import Image
src=np.asarray(Image.open('../referenties/jordi_gemini.png')).astype(float)
X0,X1=235,int(sys.argv[2]) if len(sys.argv)>2 else 500
s=float(sys.argv[1])
H,W,_=src.shape
out=np.zeros_like(src); out[:]=src[5,5]
# doel-x -> bron-x
newX0=X1-(X1-X0)*s
for xn in range(W):
    if xn>=X1: xs=xn
    elif xn>=newX0: xs=X1-(X1-xn)/s
    else: xs=X0-(newX0-xn)  # links van het dier: achtergrond
    xi=int(round(xs))
    if 0<=xi<W: out[:,xn]=src[:,xi]
Image.fromarray(out.astype('uint8')).save(f'kort_{int(s*100)}.png')
