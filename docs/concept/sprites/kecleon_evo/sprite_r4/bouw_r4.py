# r4 = model OVERNEMEN: verkleind model (sprite_r1/model_verkleind63.png, door rijen/kolommen te schrappen),
# alleen groene pixels omgezet naar de oranje modeltint met gelijke lichtheid; verder niets veranderd.
# Daarna alleen technisch: palet naar 15 kleuren + transparant.
import numpy as np, colorsys
from PIL import Image
m=np.asarray(Image.open('../sprite_r1/model_verkleind63.png').convert('RGBA')).astype(int)
rgb=m[...,:3]; al=m[...,3]>0
def hls(p): return colorsys.rgb_to_hls(*(p/255))
H=np.zeros(al.shape); L=np.zeros(al.shape); S=np.zeros(al.shape)
for y in range(63):
  for x in range(63):
    h,l,s=hls(rgb[y,x]); H[y,x]=h*360; L[y,x]=l; S[y,x]=s
groen=al&(H>=65)&(H<=160)&(L>0.18)
# oranje modeltinten: lijfpixels van r1 (tint 5-35, niet roze), zelfde model
r1=np.asarray(Image.open('../model/r1_nat100.png').convert('RGB')).astype(int).reshape(-1,3)
oranje=[]
for p in r1:
  h,l,s=hls(p); h*=360
  if (h<35 or h>350) and s>0.35 and 0.25<l<0.75 and not (l>0.62 and (h>340 or h<12)): oranje.append((l,tuple(p)))
oranje.sort(); Ls=np.array([o[0] for o in oranje])
out=rgb.copy()
for y,x in zip(*np.where(groen)):
  i=np.argmin(np.abs(Ls-L[y,x])); out[y,x]=oranje[i][1]
img=Image.fromarray(np.dstack([out,np.where(al,255,0)]).astype('uint8'),'RGBA')
# palet: 15 kleuren uit de pixels zelf (median cut), transparant = index 0
q=Image.fromarray(out.astype('uint8')).quantize(15,method=Image.Quantize.MEDIANCUT)
pal=q.getpalette()[:45]; idx=np.asarray(q)+1; idx[~al]=0
P=Image.fromarray(idx.astype('uint8'),'P'); P.putpalette([152,208,248]+pal+[0]*(768-48))
P.save('kecleon_evo_r4.png',transparency=0)
P.convert('RGBA').resize((512,512),Image.NEAREST).save('kecleon_evo_r4_8x.png')
img.resize((512,512),Image.NEAREST).save('voor_palet_8x.png')
print('groene pixels omgezet:',groen.sum())
