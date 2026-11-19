# Buikvarianten: alleen paletplekken 11-13 (buik schaduw/midden/licht) anders; pixels identiek aan ../hoatzin.png
import numpy as np; from PIL import Image, ImageDraw
src=Image.open('../hoatzin.png'); a=np.asarray(src); pal=src.getpalette()[:48]
V={'A_huidig':['#7A5270','#8E6280','#A57A98'],
   'B_poisonpaars':['#6A3A80','#8A50A6','#AE74C8'],
   'C_gifgroen_hooglicht':['#7A5270','#8E6280','#A2B862'],
   'D_diep_naar_giftig':['#4C2860','#7C4498','#B47CD6']}
hx=lambda h:[int(h[i:i+2],16) for i in (1,3,5)]
ims=[]
for naam,cols in V.items():
    p=list(pal)
    for k,h in zip((11,12,13),cols): p[k*3:k*3+3]=hx(h)
    im=Image.fromarray(a,'P'); im.putpalette(p); im.save(naam+'.png',transparency=0)
    o=np.array(p).reshape(-1,3)[a].astype('uint8'); al=(a!=0)
    rgba=np.dstack([o,al*255]).astype('uint8'); ims.append((naam,cols,Image.fromarray(rgba,'RGBA')))
    assert (np.asarray(Image.open(naam+'.png'))==a).all()
W=4*280+40; vel=Image.new('RGB',(W,256+110+90),(230,230,230)); d=ImageDraw.Draw(vel)
for i,(naam,cols,im) in enumerate(ims):
    x=20+i*280; b=Image.new('RGBA',(256,256),'white'); b.alpha_composite(im.resize((256,256),Image.NEAREST)); vel.paste(b,(x,40))
    d.text((x,8),naam,fill='black'); d.text((x,22),' '.join(cols),fill='black')
    for j,c in enumerate(cols): d.rectangle([x+j*30,300,x+j*30+26,320],fill=c)
    for j,bg in enumerate([(248,248,248),(40,40,48)]):
        bb=Image.new('RGBA',(64,64),bg+(255,)); bb.alpha_composite(im); vel.paste(bb,(x+j*72,340))
vel.save('vel.png'); print('ok')
