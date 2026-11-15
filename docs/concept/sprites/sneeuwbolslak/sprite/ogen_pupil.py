# Jordi op r2: "op de ogen na ben ik tevreden, die zijn een beetje te groot deel van de oogballen nu lijkt" -> pupil kleiner, verder diff 0.
# A: pupil 2 px (verticaal), B: pupil 1 px. Weggehaalde pupilpixels krijgen het oogwit (index 6).
from PIL import Image; import numpy as np
src=Image.open('maker/r2.png'); o=np.array(src)
var={'A':[(11,34),(19,34)],'B':[(11,34),(19,34),(12,33),(20,33)]}
pal=np.array(src.getpalette()[:48]).reshape(16,3).astype(np.uint8)
tiles=[]
for k,px in var.items():
    q=o.copy()
    for x,y in px: assert q[y,x]==1; q[y,x]=6
    im=Image.new('P',(64,64)); im.putpalette(src.getpalette()); im.putdata(q.reshape(-1).tolist()); im.save(f'maker/r3_{k}.png',transparency=0)
    print(k,'diff',int((q!=o).sum()))
def rgb(q):
    a=pal[q]; a[q==0]=255; return Image.fromarray(a)
qs=[o]+[np.array(Image.open(f'maker/r3_{k}.png')) for k in var]
v=Image.new('RGB',(3*528,512+150),'white')
for i,q in enumerate(qs):
    v.paste(rgb(q).resize((512,512),Image.NEAREST),(i*528,0))
    v.paste(rgb(q),(i*528,520)); v.paste(rgb(q).resize((128,128),Image.NEAREST),(i*528+80,520))
    # oog-close-up
    v.paste(rgb(q).crop((9,30,23,39)).resize((14*16,9*16),Image.NEAREST),(i*528+240,520-8+16))
v.save('maker/vel_r3.png')
