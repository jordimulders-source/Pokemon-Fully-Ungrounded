# meting r4 (romp): per spritecel in het hi-res model: aandeel zwart (L<70) en mediane kleur van de niet-zwarte pixels
import numpy as np; from PIL import Image
im=np.asarray(Image.open('../referenties/gemini_gekozen_r7.png').convert('RGB')).astype(float)
L=im@np.array([.299,.587,.114]); import sys
from PIL import ImageFilter
MEDF=np.asarray(Image.fromarray(np.clip(L,0,255).astype('uint8')).filter(ImageFilter.MedianFilter(25))).astype(float)
ZW=(L<float(sys.argv[1]))|((L<105)&(L<MEDF-float(sys.argv[2]) if len(sys.argv)>2 else False))
PX,FX,PY,FY=5.704,5.16,5.692,3.088; MY,MX=-21,-2
def blok(y,x):
  r0,c0=MY+3*y,MX+3*x
  return (slice(int(round(FY+r0*PY)),int(round(FY+(r0+3)*PY))),slice(int(round(FX+c0*PX)),int(round(FX+(c0+3)*PX))))
F=np.zeros((64,64)); MED=np.zeros((64,64,3)); WIT=np.zeros((64,64))
for y in range(64):
  for x in range(64):
    b=blok(y,x); z=ZW[b]
    if z.size==0: continue
    F[y,x]=z.mean(); v=im[b][~z]
    if len(v): MED[y,x]=np.median(v,0)
    WIT[y,x]=(im[b].min(-1)>=245).mean()
np.save(sys.argv[3] if len(sys.argv)>3 else 'r4/F.npy',F); np.save('r4/MED.npy',MED); np.save('r4/WIT.npy',WIT)
