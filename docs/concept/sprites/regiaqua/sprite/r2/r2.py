# r2 = r1 + keurpunten 1-4 (alleen tinten/stippen, geen vorm). Draai vanuit regiaqua/sprite/.
from PIL import Image
import numpy as np
r1=Image.open('r1/regiaqua_r1.png'); kaal=Image.open('r1/kaal.png').convert('RGB')
pal=r1.getpalette()[:48]; cols=[tuple(pal[i*3:i*3+3]) for i in range(16)]
a=np.array(r1)
def idx(c):
    return min(range(len(cols)),key=lambda i:sum((x-y)**2 for x,y in zip(cols[i],c)))
lijn=idx((10,38,68)); print('lijn',lijn,cols[lijn])
for x,y in [(15,30),(16,31),(18,37),(19,38),(9,31)]:
    print((x,y),cols[a[y,x]]); a[y,x]=lijn
# 3: onderste stippen een rij lager
st=idx((0,206,188)); hl=idx((176,255,236))
for x0 in (25,30):
    blok=a[34:36,x0:x0+2].copy()
    for yy in (34,):
        for xx in (x0,x0+1): a[yy,xx]=3  # omringende watertoon (r1 rij 33/36 = index 3)
    a[35:37,x0:x0+2]=blok
# 4: stipkleur feller
pal=list(r1.getpalette()); pal[st*3:st*3+3]=[24,236,210]
out=Image.fromarray(a.astype('uint8'),'P'); out.putpalette(pal)
out.save('r2/regiaqua_r2.png',transparency=0)
rgb=np.array(out.convert('RGB')); rgb[np.array(out)==0]=255
Image.fromarray(rgb).resize((512,512),Image.NEAREST).save('r2/regiaqua_r2_8x.png')
d=np.argwhere(np.array(out)!=np.array(r1)); print('diff px',len(d),d.tolist())
