# Variant: achterlijf ingedrukt (factor s), maar bolletjes en pootjes houden hun ronde vorm (onvervormd teruggeplakt).
import numpy as np, sys
from PIL import Image
src=np.asarray(Image.open('../referenties/jordi_gemini.png')).astype(int)
s=float(sys.argv[1]); X0,X1=235,500
H,W,_=src.shape; bg=src[5,5]
newX0=X1-(X1-X0)*s
def fwd(x): return x if x>=X1 else X1-(X1-x)*s
out=np.zeros_like(src); out[:]=bg
for xn in range(W):
    xs=xn if xn>=X1 else (X1-(X1-xn)/s if xn>=newX0 else -1)
    if 0<=xs<W: out[:,xn]=src[:,int(round(xs))]
green=lambda c:(c[...,1]>c[...,0]+25)&(c[...,1]>c[...,2]+25)
# bolletjes boven (x0,x1,y0,y1) en pootjes onder
boxes=[(290,338,545,592),(348,406,500,560),(426,465,460,508),(268,332,690,748),(363,428,694,750)]
for x0,x1,y0,y1 in boxes:
    patch=src[y0:y1,x0:x1]; m=~green(patch)
    cx=(x0+x1)/2; dx=int(round(fwd(cx)-cx))
    reg=out[y0:y1,x0+dx:x1+dx]; reg[m]=patch[m]
Image.fromarray(out.astype('uint8')).save(f'kort2_{int(s*100)}.png')
