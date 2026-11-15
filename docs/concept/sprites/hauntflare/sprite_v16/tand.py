# B_K2 + 1 pixel bij de rechter boventand (Jordi: "die tand die echt een 90 graden pixelhoek heeft ... 1 pixel bij kleuren")
from PIL import Image, ImageDraw, ImageFont; import numpy as np
im=Image.open('sprite_v16/optie_B_K2.png'); pal=im.getpalette(); B=np.array(im)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',18)
opts=[('nu (B + K2)',None),('T1: (31,33) roze',(31,33)),('T2: (29,34) roze',(29,34))]
v=Image.new('RGB',(3*380+40,330),'white'); d=ImageDraw.Draw(v)
for i,(n,p) in enumerate(opts):
    a=B.copy()
    if p: a[p[1],p[0]]=7
    o=Image.fromarray(a,'P'); o.putpalette(pal); o.save(f'sprite_v16/tand_{i}.png',transparency=0)
    r=Image.open(f'sprite_v16/tand_{i}.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(r); r=bg.convert('RGB')
    z=r.crop((22,29,38,39)).resize((352,220),Image.NEAREST); x=20+i*380
    dz=ImageDraw.Draw(z)
    if p: dz.rectangle([(p[0]-22)*22,(p[1]-29)*22,(p[0]-22)*22+21,(p[1]-29)*22+21],outline=(0,120,255),width=3)
    v.paste(z,(x,30)); d.text((x,5),n,fill='black',font=f); v.paste(r,(x,260))
v.save('sprite_v16/tand_opties.png')
