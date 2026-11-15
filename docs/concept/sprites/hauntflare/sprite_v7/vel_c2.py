# vel_c2.png: C2 | C | v6 — gezicht 12x, hele sprite 6x, 1x
import os
from PIL import Image, ImageDraw
D=os.path.dirname(os.path.abspath(__file__)); H=os.path.dirname(D)
fs=[('C2',D+'/kandidaat_C2.png'),('C',D+'/kandidaat_C.png'),('v6',H+'/sprite_v6/hauntflare_v6.png')]
box=(12,16,44,42); WZ,HZ=32*12,26*12; W6=384; pad=12
c=Image.new('RGB',(3*(W6+pad)+pad,20+HZ+pad+W6+pad+64+pad),'white'); d=ImageDraw.Draw(c)
for i,(t,f) in enumerate(fs):
    im=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(im); bg=bg.convert('RGB')
    x=pad+i*(W6+pad); d.text((x,4),t,fill='black')
    c.paste(bg.crop(box).resize((WZ,HZ),Image.NEAREST),(x,20))
    c.paste(bg.resize((W6,W6),Image.NEAREST),(x,20+HZ+pad))
    c.paste(bg,(x,20+HZ+pad+W6+pad))
c.save(D+'/vel_c2.png')
