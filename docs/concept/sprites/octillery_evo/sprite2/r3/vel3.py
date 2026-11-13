# r3/vel3.py : r3/vel.png. Opbouw als r2: model op spriteschaal 8x | sprite 8x | close-ups 16x (model|r2|r3) | 1x 2x 4x licht/donker | 2x tussen Gen 3
# vanuit sprite2/: python3 r3/vel3.py
import sys; sys.path.insert(0,'r3'); sys.path.insert(0,'.')
import bouw3,cfg
from PIL import Image,ImageDraw
P3=list(cfg.PAL); P2=list(P3); P2[2]=(72,16,30)
a=cfg.read('r3/raster.txt'); b=cfg.read('r2/raster.txt'); m=cfg.model64()
BG=(208,208,176,255); DK=(72,80,96,255)
S=cfg.rgba(a,BG,P3); Sd=cfg.rgba(a,DK,P3); S2=cfg.rgba(b,BG,P2)
Z=[('linker rupsband',0,43,34,62),('rechter rupsband',31,43,64,62),('mondkanon + linkeroog',15,33,36,52),('tentakels links',0,21,27,45),('kanon rechts + tentakel D',41,21,64,45)]
def cu(bx,k=12):
    w=(bx[2]-bx[0])*k; h=(bx[3]-bx[1])*k
    im=Image.new('RGB',(3*w+16,h),(255,255,255))
    for i,src in enumerate((m,S2,S)): im.paste(src.crop(bx).resize((w,h),Image.NEAREST),(i*(w+8),0))
    return im
cs=[cu(z[1:]) for z in Z]
W=max(1040,max(c.size[0] for c in cs)); H=520+sum(c.size[1]+22 for c in cs)+300+170
v=Image.new('RGB',(W,H),(255,255,255)); d=ImageDraw.Draw(v)
v.paste(m.resize((512,512),Image.NEAREST),(0,0)); v.paste(S.resize((512,512),Image.NEAREST),(520,0)); y=520
for z,c in zip(Z,cs):
    d.text((2,y+4),z[0]+' 12x: model (verkleind) | r2 | r3',fill=(0,0,0)); v.paste(c,(0,y+20)); y+=c.size[1]+22
d.text((2,y+4),'r3 op 1x, 2x, 4x: licht en donker',fill=(0,0,0)); y+=20; x=0
for im in (S,Sd):
    for k in (1,2,4):
        v.paste(im.resize((64*k,64*k),Image.NEAREST),(x,y)); x+=64*k+8
y+=262; d.text((2,y+4),'2x tussen Gen 3: Octillery, Tentacruel, Gyarados, r3, model, Kingdra, Scizor, Crawdaunt',fill=(0,0,0)); y+=20
G=lambda n:Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/%s/anim_front_gba.png'%n).convert('RGBA').crop((0,0,64,64))
def onbg(n):
    im=Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/%s/anim_front_gba.png'%n); p=im.getpalette(); im=im.crop((0,0,64,64)).convert('RGB')
    bg=tuple(p[:3]); px=im.load()
    for yy in range(64):
        for xx in range(64):
            if px[xx,yy]==bg: px[xx,yy]=BG[:3]
    return im
x=0
for it in ['octillery','tentacruel','gyarados',S,m,'kingdra','scizor','crawdaunt']:
    im=onbg(it) if isinstance(it,str) else it
    v.paste(im.resize((128,128),Image.NEAREST),(x,y)); x+=130
v.save('r3/vel.png'); print(v.size)
