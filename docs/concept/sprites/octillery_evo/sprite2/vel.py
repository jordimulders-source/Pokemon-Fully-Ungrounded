# vel.py rN : rN/vel.png = model op spriteschaal 8x | sprite 8x | close-ups 16x (model|sprite) | 1x en 2x licht/donker + Gen 3
import cfg,sys
from PIL import Image,ImageDraw
r=sys.argv[1]; a=cfg.read(r+'/raster.txt'); m=cfg.model64()
BG=(208,208,176,255); DK=(72,80,96,255)
S=cfg.rgba(a,BG); Sd=cfg.rgba(a,DK)
Z=[('kop',22,22,46,42),('mondkanon',17,37,34,52),('linker rupsband',0,44,34,63),('rechter rupsband',32,46,64,63),('rechter tentakels',41,21,64,50)]
W=1040+16; rows=[]
def cu(b,k=16):
    w=(b[2]-b[0])*k; h=(b[3]-b[1])*k
    im=Image.new('RGB',(2*w+8,h),(255,255,255))
    im.paste(m.crop(b).resize((w,h),Image.NEAREST),(0,0)); im.paste(S.crop(b).resize((w,h),Image.NEAREST),(w+8,0)); return im
top=Image.new('RGB',(W,520),(255,255,255)); top.paste(m.resize((512,512),Image.NEAREST),(0,0)); top.paste(S.resize((512,512),Image.NEAREST),(520,0))
cs=[cu(z[1:]) for z in Z]
H=520+sum(c.size[1]+22 for c in cs)+290
v=Image.new('RGB',(W,H),(255,255,255)); d=ImageDraw.Draw(v); v.paste(top,(0,0)); y=520
for z,c in zip(Z,cs):
    d.text((2,y+4),z[0]+' 16x: model (verkleind) | sprite',fill=(0,0,0)); v.paste(c,(0,y+20)); y+=c.size[1]+22
d.text((2,y+4),'1x en 2x: sprite licht/donker | model verkleind | Gen 3: Octillery, Tentacruel, Gyarados, Kingdra, Scizor',fill=(0,0,0)); y+=20
G=[Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/%s/anim_front_gba.png'%n).convert('RGB').crop((0,0,64,64)) for n in ['octillery','tentacruel','gyarados','kingdra','scizor']]
x=0
for im in [S,Sd,m]+G:
    v.paste(im.resize((128,128),Image.NEAREST),(x,y)); v.paste(im,(x,y+134)); x+=132
v.save(r+'/vel.png'); print(v.size)
