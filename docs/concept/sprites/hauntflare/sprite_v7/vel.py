# vel.png: per kandidaat hele sprite 6x, gezicht 12x, 1x; onderaan v6, Haunter en Gengar ter vergelijking
import os
from PIL import Image, ImageDraw
D=os.path.dirname(os.path.abspath(__file__)); H=os.path.dirname(D); R=os.path.abspath(H+'/../../../..')
def rgba(f,crop64=True):
    im=Image.open(f)
    if crop64: im=im.crop((0,0,64,64))
    im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg.convert('RGB')
rijen=[('A: oog A (8 kol.) + mond M1 (1 lager), tong',D+'/kandidaat_A.png',(12,16,44,42)),
       ('C: oog C (8 kol., 1 rij minder) + mond M2 (2 lager), tong',D+'/kandidaat_C.png',(12,16,44,42)),
       ('C_donker: als C, opening helemaal donkerrood',D+'/kandidaat_C_donker.png',(12,16,44,42)),
       ('v6 (uitgangspunt)',H+'/sprite_v6/hauntflare_v6.png',(12,16,44,42)),
       ('Haunter Gen 3',R+'/graphics/pokemon/haunter/anim_front.png',(6,24,38,50)),
       ('Gengar Gen 3',R+'/graphics/pokemon/gengar/anim_front.png',(10,18,42,44))]
W6=384; WZ=32*12; HZ=26*12; pad=10; lab=20
c=Image.new('RGB',(W6+WZ+64+4*pad,len(rijen)*(W6+lab+pad)),'white'); d=ImageDraw.Draw(c)
for i,(t,f,box) in enumerate(rijen):
    y=i*(W6+lab+pad); im=rgba(f)
    d.text((pad,y+4),t,fill='black')
    c.paste(im.resize((W6,W6),Image.NEAREST),(pad,y+lab))
    c.paste(im.crop(box).resize((WZ,HZ),Image.NEAREST),(2*pad+W6,y+lab))
    c.paste(im,(3*pad+W6+WZ,y+lab))
c.save(D+'/vel.png'); print(c.size)
