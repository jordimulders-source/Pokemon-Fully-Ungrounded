# Jordi (13 nov, na af): "de bovenkant van de bol is niet rond genoeg". Alleen de bovenrand van de bol (rijen 22-31) volgt een cirkel; binnenkant aangevuld met de bolkleur (14), buitenrand zwart (1). Rest diff 0.
from PIL import Image; import numpy as np
src=Image.open('af/sneeuwbolslak.png'); O=np.array(src); pal=np.array(src.getpalette()[:48]).reshape(16,3).astype(np.uint8)
def maak(cx,cy,R):
    o=O.copy()
    inside=lambda x,y:(x-cx)**2+(y-cy)**2<=R*R
    for y in range(21,32):
        for x in range(24,56):
            if inside(x,y):
                if o[y,x] in (0,1,2): o[y,x]=14
            else:
                if o[y,x]!=0: o[y,x]=0
    # buitenrand: bolpixels in zone met transparante buur -> 1
    q=o.copy()
    for y in range(21,32):
        for x in range(24,56):
            if o[y,x]!=0 and any(o[y+dy,x+dx]==0 for dy,dx in((1,0),(-1,0),(0,1),(0,-1))): q[y,x]=1
    # aansluiting op rij 32: rand blijft
    return q
res={'nu':O,'A':maak(39.5,36.5,14.0),'B':maak(39.5,36.8,14.3)}
for k,q in res.items():
    if k!='nu':
        im=Image.new('P',(64,64)); im.putpalette(src.getpalette()); im.putdata(q.reshape(-1).tolist()); im.save(f'sprite/rond/rond_{k}.png',transparency=0)
        print(k,'diff',int((q!=O).sum()), 'buiten zone', int(((q!=O)[32:]).sum()+((q!=O)[:21]).sum()))
v=Image.new('RGB',(3*528,512+80),'white')
for i,(k,q) in enumerate(res.items()):
    a=pal[q]; a[q==0]=255; im=Image.fromarray(a)
    v.paste(im.resize((512,512),Image.NEAREST),(i*528,0)); v.paste(im,(i*528,520)); v.paste(im.resize((128,128),Image.NEAREST),(i*528+80,520-48+48))
v.save('sprite/rond/vel_rond.png')
for k in ('A',):
    q=res[k]
    for y in range(21,34): print(y,''.join('%x'%v if v else '.' for v in q[y,26:56]))
