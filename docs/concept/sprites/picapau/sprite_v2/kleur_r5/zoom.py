"""zoom.png: 10x render | r3 | r4 met raster + coördinaten (werkvel)."""
import sys
from PIL import Image, ImageDraw
import os; Z=int(os.environ.get("Z","10"))
def spr(p):
    im=Image.open(p).convert('RGBA'); px=im.load()
    for y in range(64):
        for x in range(64):
            if px[x,y][:3]==(152,208,160): px[x,y]=(0,0,0,0)
    return im
x0,y0,x1,y1=[int(v) for v in (sys.argv[1:5] if len(sys.argv)>4 else (10,0,54,60))]
ren=Image.open('../../blender/B1/b1.png').convert('RGBA').resize((64*Z,64*Z),Image.LANCZOS)
ims=[ren,spr('../kleur_r4/picapau.png').resize((64*Z,64*Z),Image.NEAREST),spr('picapau.png').resize((64*Z,64*Z),Image.NEAREST)]
W=(x1-x0)*Z;H=(y1-y0)*Z
v=Image.new('RGBA',(3*(W+30),H+20),(225,225,225,255));d=ImageDraw.Draw(v)
for i,im in enumerate(ims):
    ox=i*(W+30)+20
    v.alpha_composite(im.crop((x0*Z,y0*Z,x1*Z,y1*Z)),(ox,15))
    for x in range(x0,x1+1):
        X=ox+(x-x0)*Z; d.line([(X,15),(X,15+H)],fill=(80,80,200) if x%5==0 else (190,190,190))
        if x%5==0: d.text((X+1,2),str(x),fill=(0,0,150))
    for y in range(y0,y1+1):
        Y=15+(y-y0)*Z; d.line([(ox,Y),(ox+W,Y)],fill=(80,80,200) if y%5==0 else (190,190,190))
        if y%5==0: d.text((ox-18,Y),str(y),fill=(0,0,150))
v.save(sys.argv[5] if len(sys.argv)>5 else 'zoom.png')
