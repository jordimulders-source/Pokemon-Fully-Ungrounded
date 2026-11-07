# maakt vel.png; draaien: python3 vel.py (pad-onafhankelijk)
import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'../../../../../../../')
D=os.path.join(H,'../../../')
def load_idx(path,pal=None,frame=True):
    im=Image.open(path)
    if pal:
        p=[tuple(int(v) for v in l.split()) for l in open(pal).read().split('\n')[3:19] if l.strip()]
        im.putpalette([c for q in p for c in q])
    if frame: im=im.crop((0,0,64,64))
    idx=im.load(); rgb=im.convert('RGBA'); px=rgb.load()
    for y in range(64):
        for x in range(64):
            if idx[x,y]==0: px[x,y]=(0,0,0,0)
    return rgb
sp=load_idx(os.path.join(H,'../nachtaap.png'))
f1=load_idx(os.path.join(D,'referenties/fase1_goedgekeurd.png'),os.path.join(D,'../nachtaap/ronde12/variant_spiraal/normal.pal'))
ond=Image.open(os.path.join(D,'silhouet/onderlaag_256.png')).convert('RGBA')
refs=['lairon','sableye','aipom','grumpig','mismagius']
RF=[load_idx(os.path.join(R,f'graphics/pokemon/{n}/anim_front.png'),os.path.join(R,f'graphics/pokemon/{n}/normal.pal')) for n in refs]
L=(236,236,230,255); DK=(40,40,48,255)
o=Image.new('RGBA',(1350,640),L); d=ImageDraw.Draw(o)
def put(im,x,y,bg,lab=None,s=1):
    im=im.resize((im.width*s,im.height*s),Image.NEAREST)
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); o.paste(b,(x,y))
    if lab: d.text((x,y+im.height+3),lab,fill=(30,30,30,255))
put(sp,0,0,L,'nachtaap fase 2, kleur r1, 4x',4)
put(sp,266,0,DK,'4x op donker',4)
put(ond,532,0,(255,255,255,255),'onderlaag (3D-poppetje), 4x')
put(f1,798,0,L,'fase 1 (goedgekeurd), 4x',4)
put(sp,1066,0,L,'1x'); put(sp,1140,0,DK); put(f1,1066,80,L,'fase 1, 1x')
put(sp,1150,80,L,"3x",3)
x=0
for n,r in zip(['nachtaap']+refs,[sp]+RF):
    put(r,x,290,L,n,3); x+=200
d.text((4,500),'1x op licht en donker:',fill=(30,30,30,255))
x=0
for n,r in zip(['nachtaap','fase 1']+refs,[sp,f1]+RF):
    put(r,x,515,L,n); put(r,x,585-0,DK) if False else None; x+=80
x=640
for r in [sp,f1]+RF:
    put(r,x,515,DK); x+=80
o.save(os.path.join(H,'../vel.png'))
