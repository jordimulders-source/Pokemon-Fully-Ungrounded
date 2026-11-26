# snelle preview: varianten naast elkaar op schaal s (+ model)
import sys,numpy as np; from PIL import Image
from palet import PAL
s=int(sys.argv[1]); names=sys.argv[2:-1]; outp=sys.argv[-1]
z=np.load('reductie.npz'); xs,ys=z['xs'],z['ys']
ims=[]
for n in names:
    a=np.load(n); o=np.zeros(a.shape+(3,),'uint8'); o[:]=255
    for k in range(1,16): o[a==k]=PAL[k]
    ims.append(Image.fromarray(o).resize((a.shape[1]*s,a.shape[0]*s),Image.NEAREST))
H,W=a.shape
mod=Image.open('../referenties/gemini_gekozen_v1.png').convert('RGB').crop((int(xs[0]),int(ys[0]),int(xs[W]),int(ys[H]))).resize((W*s,H*s),Image.LANCZOS)
ims.append(mod)
cv=Image.new('RGB',(sum(i.size[0]+10 for i in ims),H*s),'white'); x=0
for i in ims: cv.paste(i,(x,0)); x+=i.size[0]+10
cv.save(outp)
