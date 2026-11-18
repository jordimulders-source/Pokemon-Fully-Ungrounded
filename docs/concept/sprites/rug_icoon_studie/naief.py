"""Echte icoon/rug naast een kale verkleining/vergroting van de front: wat doet Game Freak extra?
python3 naief.py uit.png soort ... (GBA-set; of een pad naar een eigen front-png)"""
import os,sys,numpy as np
from PIL import Image,ImageDraw
G='graphics/pokemon'
def rgba(p):
    im=Image.open(p).convert('RGBA'); a=np.array(im); ix=np.array(Image.open(p))
    a[ix==0,3]=0; return Image.fromarray(a)
def crop(im):
    return im.crop(im.getbbox())
Z=4; rows=[]
for sp in sys.argv[2:]:
    if sp.endswith('.png'): fr=rgba(sp).crop((0,0,64,64)); ic=None; name=os.path.basename(os.path.dirname(os.path.dirname(sp)))
    else:
        d=os.path.join(G,sp); fr=rgba(d+'/anim_front_gba.png').crop((0,0,64,64)); ic=crop(rgba(d+'/icon_gba.png').crop((0,0,32,32))); name=sp
    f=crop(fr); th=ic.size[1] if ic else max(15,round(0.0+ (15+ (f.size[1]-30)*10/30))) if False else (ic.size[1] if ic else round(15+(min(max(f.size[1],30),60)-30)/3))
    s=th/f.size[1]; small=f.resize((max(1,round(f.size[0]*s)),th),Image.BOX)
    al=np.array(small); al[...,3]=np.where(al[...,3]>100,255,0); small=Image.fromarray(al)
    rows.append((name,[x for x in [f,ic,small] if x is not None]))
W=60+max(sum(p.size[0]*Z+12 for p in ps) for _,ps in rows); H=sum(max(p.size[1] for p in ps)*Z+12 for _,ps in rows)
img=Image.new('RGB',(W,H),(232,232,224)); dr=ImageDraw.Draw(img); y=0
for n,ps in rows:
    dr.text((2,y+2),n,fill=0); x=60; h=max(p.size[1] for p in ps)*Z
    for p in ps:
        q=p.resize((p.size[0]*Z,p.size[1]*Z),Image.NEAREST); img.paste(q,(x,y+h-q.size[1]),q); x+=q.size[0]+12
    y+=h+12
img.save(sys.argv[1])
