# Eindkeuring r7b: 8 MOET-pixels (sprite/keuring/EINDKEURING_r7b.md) -> sprite/maker/raster_af.txt, af/sneeuwbolslak_fase2.png (+ _8x).
import numpy as np; from PIL import Image
R=[list(l.rstrip('\n')) for l in open('sprite/maker/raster_r7b.txt')]
im=Image.open('sprite/maker/r7b.png'); I=np.array(im)
m={}
for y in range(64):
    for x in range(64): m.setdefault(R[y][x],int(I[y,x]))
MOET=[((27,38),'c','e')]+[((x,38),'b','e') for x in (28,29,30,31)]+[((x,38),'b','c') for x in (32,33)]+[((33,34),'b','e')]
for (x,y),oud,nieuw in MOET:
    assert R[y][x]==oud,(x,y,R[y][x]); R[y][x]=nieuw
open('sprite/maker/raster_af.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
O=np.array([[m[R[y][x]] for x in range(64)] for y in range(64)],np.uint8)
out=Image.fromarray(O,'P'); out.putpalette(im.getpalette()); out.save('af/sneeuwbolslak_fase2.png',transparency=0)
pal=np.array(im.getpalette()[:768]).reshape(-1,3).astype(np.uint8)
rgb=pal[O]; rgb[O==0]=255
Image.fromarray(rgb).resize((512,512),Image.NEAREST).save('af/sneeuwbolslak_fase2_8x.png')
print('kleuren',len(set(O.ravel())),'ok')
