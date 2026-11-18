"""Studievel: front, back, icoon (2 frames) en overworld (6 frames) naast elkaar.
Gebruik: python3 vel.py uit.png [--set gba] soort1 soort2 ...  (vanuit de repo-root)
Eigen sprites: soort=map met front.png/back.png/icon.png/overworld.png."""
import os,sys,numpy as np
from PIL import Image,ImageDraw
G='graphics/pokemon'
def pal(p):
    L=open(p).read().split('\n'); return [tuple(int(v) for v in L[3+k].split()[:3]) for k in range(int(L[2]))]
def rgba(path,palette=None):
    im=Image.open(path); a=np.array(im)
    if palette is None:
        p=im.getpalette()[:48]; palette=[tuple(p[3*k:3*k+3]) for k in range(16)]
    palette=list(palette)+[(0,0,0)]*16
    out=np.zeros(a.shape+(4,),np.uint8)
    for k in range(16):
        m=a==k
        if k: out[m]=palette[k]+(255,)
    return Image.fromarray(out)
def find(d,names):
    for n in names:
        if os.path.exists(os.path.join(d,n)): return os.path.join(d,n)
args=sys.argv[2:]; gba='--set' in args
if gba: i=args.index('--set'); args=args[:i]+args[i+2:]
Z=3; BG=(232,232,224)
rows=[]
for sp in args:
    d=os.path.join(G,sp) if os.path.isdir(os.path.join(G,sp)) else sp
    sfx='_gba' if gba else ''
    np_=find(d,['normal%s.pal'%sfx,'normal.pal']); P=pal(np_) if np_ else None
    fr=find(d,['anim_front%s.png'%sfx,'front%s.png'%sfx,'anim_front.png','front.png'])
    bk=find(d,['back%s.png'%sfx,'back.png'])
    ic=find(d,['icon%s.png'%sfx,'icon.png']); ow=find(d,['overworld.png'])
    owp=find(d,['overworld_normal.pal'])
    parts=[]
    if fr: parts.append(rgba(fr,P).crop((0,0,64,64)))
    if bk: parts.append(rgba(bk,P))
    if ic:
        I=rgba(ic,pal('graphics/pokemon/icon_palettes/pal%d.pal'%0) if False else None)
        parts+= [I.crop((0,0,32,32)),I.crop((0,32,32,64))]
    if ow:
        O=rgba(ow,pal(owp) if owp else None); fs=O.size[1]
        parts+=[O.crop((k*fs,0,(k+1)*fs,fs)) for k in range(6)]
    rows.append((os.path.basename(d.rstrip('/')),parts))
W=max(sum(p.size[0]*Z+8 for p in ps)+90 for _,ps in rows)
H=sum(max(p.size[1] for p in ps)*Z+8 for _,ps in rows)
img=Image.new('RGB',(W,H),BG); dr=ImageDraw.Draw(img); y=0
for name,ps in rows:
    dr.text((4,y+4),name,fill=(0,0,0)); x=90; h=max(p.size[1] for p in ps)*Z
    for p in ps:
        q=p.resize((p.size[0]*Z,p.size[1]*Z),Image.NEAREST)
        dr.rectangle((x-1,y+h-q.size[1]-1+4,x+q.size[0],y+h+4),outline=(200,200,190))
        img.paste(q,(x,y+h-q.size[1]+4),q); x+=q.size[0]+8
    y+=h+8
img.save(sys.argv[1]); print(sys.argv[1],img.size)
