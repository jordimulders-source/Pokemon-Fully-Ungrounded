# Vileplume r19: twee reparaties op r18 (keuring r18/KEURING.md); rest pixel voor pixel r18.
import sys; sys.path.insert(0,'gereedschap')
from gemeen import *
from PIL import ImageDraw
src=Image.open('r18/vileplume_r18.png'); pal=src.getpalette()[:48]; PAL=[tuple(pal[i*3:i*3+3]) for i in range(16)]
a18=np.array(src); o=a18.copy()
assert (o[52:57,26]==1).all(); o[52:57,26]=6          # 1. linkerpoot x26 y52-56: 1 -> 6
o[52,36]=0; o[52,37:40]=[6,9,6]                         # 2. rechterpoot y52 = model (gelijk aan y53)
assert (o[52,37:40]==o[53,37:40]).all()
m=np.zeros(o.shape,bool); m[52:57,26]=True; m[52,36:40]=True
assert (o[~m]==a18[~m]).all(), 'buiten de reparaties veranderd'
print('pixels anders dan r18:',(o!=a18).sum())
opslaan(o,PAL,'r19/vileplume_r19.png')
rgb(o,PAL).resize((512,512),Image.NEAREST).save('r19/r19_8x.png')
Z=12; x0,y0,x1,y1=20,38,44,64
uit=lambda a: rgb(a,PAL).crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
tegels=[('r19',uit(o)),('r18',uit(a18)),('model',model_crop(x0,y0,x1,y1,Z))]
w=(x1-x0)*Z; vel=Image.new('RGB',(3*w+24,(y1-y0)*Z+18),'white'); dr=ImageDraw.Draw(vel)
for i,(nm,t) in enumerate(tegels): vel.paste(t,(i*(w+12),18)); dr.text((i*(w+12),3),nm,fill='black')
vel.save('r19/poten_12x.png')
