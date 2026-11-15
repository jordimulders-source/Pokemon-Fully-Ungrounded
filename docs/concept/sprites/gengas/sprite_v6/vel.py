# vel.png: v6 | v5 | model op 8x; 1x/2x/3x op licht en donker (v6 | v5); close-up gezicht 12x: v6 | v5 | Gengar
# (Gengar-uitsnede = dezelfde pixels, verschoven -5,+3/+6 t.o.v. v6; uitsnede x 18-39, y 25-41).
from PIL import Image, ImageDraw
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
def rgba(p): return Image.open(p).convert('RGBA')
V6=rgba(D+'gengas_v6.png'); V5=rgba(D+'../sprite_v5/gengas_v5.png'); M=rgba(D+'../model/model_64_geschrapt.png')
G=Image.open(D+'../../../../../graphics/pokemon/gengar/anim_front.png').convert('RGBA').crop((0,0,64,64))
def op(im,kleur,s):
    b=Image.new('RGBA',im.size,kleur); b.alpha_composite(im); return b.resize((im.width*s,im.height*s),Image.NEAREST)
W=3*528+16+300; V=Image.new("RGB",(max(W,16+2*(64+128+192)+3*16*2+3*48+200),2000),(235,235,235)); d=ImageDraw.Draw(V); y=8
for i,t in enumerate(('v6 8x','v5 8x','model 8x')): d.text((16+i*528,y),t,fill=(0,0,0))
y+=14
for i,im in enumerate((V6,V5,M)): V.paste(op(im,(255,255,255,255),8),(16+i*528,y))
y+=524; x=16
for kleur in ((255,255,255,255),(40,40,48,255)):
    for s in (1,2,3):
        for im in (V6,V5): V.paste(op(im,kleur,s),(x,y)); x+=64*s+8
        x+=16
d.text((16,y+200),'1x/2x/3x licht en donker: telkens v6 | v5',fill=(0,0,0)); y+=216
d.text((16,y),'gezicht 12x: v6 | v5 | Gengar',fill=(0,0,0)); y+=14; x=16
for im,(x0,y0,x1,y1) in ((V6,(7,27,35,48)),(V5,(7,27,35,48)),(G,(12,24,40,45))):
    c=op(im,(255,255,255,255),1).crop((x0,y0,x1,y1)); c=c.resize((c.width*12,c.height*12),Image.NEAREST)
    V.paste(c,(x,y)); x+=c.width+12
y+=c.height+16
V.crop((0,0,W,y)).save(D+'vel.png'); print('vel.png')
