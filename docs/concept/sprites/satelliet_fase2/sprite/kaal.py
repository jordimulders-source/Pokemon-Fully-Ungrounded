# Kale reductie op 64 px breed: per spritepixel het blok modelpixels (14,56 px = ±1,42 natieve px).
# Dunne klassen (1 natieve px = 0,69 spritepx breed) winnen als ze >= TL van het HELE blok beslaan (TL ~ helft van 0,69:
# dan wordt een modellijn precies 1 spritepixel, zonder breuk). Volgorde: omlijning > raster > pupil/iris > paars.
# Anders: transparant als bg >= TA, en anders de meest voorkomende klasse.
import numpy as np, sys; from PIL import Image
k=np.load('klassen2.npy'); PAL=np.load('pal.npy')
TA=float(sys.argv[1]); TL=float(sys.argv[2]); UIT=sys.argv[3]
PRIO=[1,11,15,9,14,13,12,8,7,6]
from cfg import X0,X1,Y0,Y1,W,s,H,T,TOP
from cfg import F as SCHAAL
ECX,ECY=T(20,24)
o=np.zeros((H,W),int); F=np.zeros((H,W,16))
for j in range(H):
  for i in range(W):
    y0,y1=int(round(Y0+j*s)),int(round(Y0+(j+1)*s)); x0,x1=int(round(X0+i*s)),int(round(X0+(i+1)*s))
    b=k[y0:y1,x0:x1].ravel(); c=np.bincount(b,minlength=16)/b.size; F[j,i]=c
    win=[q for q in PRIO if c[q]>=TL]
    # paneelvulling 9 telt alleen als dunne klasse in het oog (pupil): elders gewoon mode
    if win and win[0]==9:
        ey=(i+.5-ECX-.5)**2+(j+.5-ECY-.5)**2<=(6*SCHAAL)**2
        if not ey: win=[q for q in win if q!=9]
    if win: o[j,i]=win[0]; continue
    if c[0]>=TA: continue
    cc=c.copy(); cc[0]=0; o[j,i]=cc.argmax()
np.save(UIT+'.npy',o); np.save(UIT+'_F.npy',F)
full=np.zeros((64,64),int); full[TOP:TOP+H]=o
im=Image.fromarray(full.astype('uint8'),'P'); pal=[int(v) for c in PAL for v in c]; im.putpalette(pal+[0]*(768-len(pal))); im.save(UIT+'.png',transparency=0)
im.convert('RGB').resize((512,512),Image.NEAREST).save(UIT+'_8x.png'); print(H,(o>0).sum(),(o==1).sum())
