# klas2.py: twee meetkaarten (geen sprite). (1) mediaan-helderheid van het modelblok als paletklasse
#  A>=228 7>=212 6>=186 5>=162 4>=130 3>=90 2<90 ; (2) aandeel donkere lijn (lum<120) per blok, 0-9 ('.'=0)
import numpy as np, sys, os
from PIL import Image
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from bg import masker, P
c=np.asarray(Image.open(P+'referenties/model_gekozen.png').convert('RGB')).astype(float); L=c.mean(2); g=masker()
a=np.array(Image.open(P+'silhouet/silhouet.png'))[:,:,3]>0
x0,y0,s=69,240,16.648
def blk(x,y): return (slice(int(y0+(y-29)*s),int(y0+(y-28)*s)),slice(int(x0+(x-5)*s),int(x0+(x-4)*s)))
hd='   '+''.join(str(x%10) for x in range(4,60))
for mode in (0,1):
  print(hd)
  for y in range(28,63):
    r=''
    for x in range(4,60):
      sl=blk(x,y); f=~g[sl]
      if not a[y,x] and f.mean()<.2: r+=' '; continue
      v=L[sl][f] if f.any() else np.array([255.])
      if mode==0:
        m=np.median(v); ch='A' if m>=228 else '7' if m>=212 else '6' if m>=186 else '5' if m>=162 else '4' if m>=130 else '3' if m>=90 else '2'
      else:
        d=(v<120).mean()*f.mean(); ch='.' if d<.08 else str(min(9,int(d*10)))
      r+= ch if a[y,x] else ch.lower() if mode==0 and ch=='A' else ('_' if mode==0 else ch)
    print(f'{y:2d} '+r)
