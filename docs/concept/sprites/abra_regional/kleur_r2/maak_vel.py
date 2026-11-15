# maak_vel.py: abra_r2_8x.png, vel.png (r2 8x | r1 8x | model zelfde schaal | 1x/2x licht/donker), closeup.png (kop en handen 12x naast het model)
from PIL import Image, ImageDraw; import numpy as np
S='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/e768f5de-0252-58bb-8bc9-76aca5f6423c/scratchpad/'
def rgba(p):
    im=Image.open(p); im.save(S+'_v.png',transparency=0); return Image.open(S+'_v.png').convert('RGBA')
def op(img,kl):
    b=Image.new('RGBA',img.size,kl); b.alpha_composite(img); return b.convert('RGB')
r2=rgba('abra_r2.png'); r1=rgba('../kleur_r1/abra_r1.png')
r2.resize((512,512),Image.NEAREST).save('abra_r2_8x.png')
nat=Image.open('../kleur_r1/natief.png').convert('RGB')
# model op dezelfde schaal: spritepixel (x,y) = natief (2x-1,2y-14); 64x64-vlak = natief (-1,-14)..(127,114)
mod=Image.new('RGB',(128,128),'white'); mod.paste(nat,(1,14)); mod=mod.resize((512,512),Image.LANCZOS)
klein=Image.new('RGB',(512,512),(200,200,200))
for k,kl in enumerate([(248,248,248,255),(40,40,48,255),(144,200,144,255)]):
    klein.paste(op(r2,kl),(16+k*80,16)); klein.paste(op(r2,kl).resize((128,128),Image.NEAREST),(16+k*164,120))
v=Image.new('RGB',(4*532,560),'white'); d=ImageDraw.Draw(v)
for k,(x,t) in enumerate(((op(r2,(255,255,255,255)).resize((512,512),Image.NEAREST),'r2 8x'),(op(r1,(255,255,255,255)).resize((512,512),Image.NEAREST),'r1 8x'),(mod,'model, zelfde schaal'),(klein,'r2 1x en 2x op licht/donker/groen'))):
    v.paste(x,(k*532,40)); d.text((k*532+8,12),t,fill=(0,0,0))
v.save('vel.png')
# close-ups 12x: kop (x 15-46, y 14-41) en handen (x 14-42, y 42-59)
Z=12; rows=[]
for (x0,y0,x1,y1) in ((15,14,46,41),(14,42,42,59)):
    sp=op(r2,(255,255,255,255)).crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
    m=mod.resize((64*Z,64*Z),Image.LANCZOS).crop((x0*Z,y0*Z,x1*Z,y1*Z))
    rows.append((sp,m))
W=max(a.width for a,b in rows)*2+20; Hh=sum(a.height for a,b in rows)+20
c=Image.new('RGB',(W,Hh),'white'); y=0
for a,b in rows: c.paste(a,(0,y)); c.paste(b,(a.width+20,y)); y+=a.height+20
c.save('closeup.png')
