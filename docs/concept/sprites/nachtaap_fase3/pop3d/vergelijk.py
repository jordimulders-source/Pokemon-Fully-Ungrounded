"""Vast vergelijkingsvel (SPRITE_WERKWIJZE, "Vóór elk vel naar Jordi"): referentiesprites naast het poppetje op
eindvormmaat + groot. Draaien vanuit de repo-root: python3 docs/concept/sprites/nachtaap_fase3/pop3d/vergelijk.py uit.png"""
import sys, os; sys.path.insert(0,'docs/concept/sprites/nachtaap_fase3/pop3d')
import muriqui3d as M, pop3d as P
from PIL import Image, ImageDraw, ImageFont
import numpy as np
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
v=P.view(M.muriqui(40,pose="krabbel",yaw=40,gebaar="B"),40,6,size=240)   # pas aan per poppetje
a=np.array(v.convert('L'))<250; ys,xs=np.where(a)
crop=v.crop((xs.min()-2,ys.min()-2,xs.max()+3,ys.max()+3))
w,h=crop.size; k=62/max(w,h); sp=crop.resize((max(1,round(w*k)),max(1,round(h*k))),Image.LANCZOS)
cells=[]
for p,n in [('mr_mime','Mr. Mime'),('machamp','Machamp'),('dusknoir','Dusknoir')]:
    fn=f'graphics/pokemon/{p}/anim_front.png'
    pal=Image.open(fn); idx=np.array(pal)[:64,:64]
    im=pal.convert('RGBA').crop((0,0,64,64)); arr=np.array(im); arr[idx==0,3]=0; cells.append((Image.fromarray(arr),n))
sp64=Image.new('RGBA',(64,64),(255,255,255,0)); sp64.paste(sp,((64-sp.size[0])//2,(64-sp.size[1])//2))
cells.append((sp64,'poppetje op eindvormmaat'))
S=5; W=64*S
sh=Image.new('RGB',(len(cells)*(W+8)+8+W+8,W+60),(246,246,248)); d=ImageDraw.Draw(sh)
d.text((8,8),'Handen vergelijken (5×): echte sprites naast het poppetje op eindvormmaat; rechts het poppetje groot',fill=(0,0,0),font=f)
for i,(im,n) in enumerate(cells):
    x=8+i*(W+8); y=32
    d.rectangle((x,y,x+W-1,y+W-1),fill=(255,255,255))
    b=im.resize((W,W),Image.NEAREST); sh.paste(b,(x,y),b); d.text((x,y+W+4),n,fill=(0,0,0),font=f)
sh.paste(v.resize((W,W)),(8+len(cells)*(W+8),32))
sh.save(sys.argv[1])
