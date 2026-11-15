# vel.png: v5 | v4 8x; v5 1x/2x op licht en donker; close-up gezicht 12x: v5 | v4 | Gengar (gezicht, geschaald naar
# dezelfde hoogte, ter vergelijking van lijnen/tinten rond oog en mond).
from PIL import Image, ImageDraw
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
def rgba(p): return Image.open(p).convert('RGBA')
V5=rgba(D+'gengas_v5.png'); V4=rgba(D+'../sprite_v4/gengas_v4.png'); M=rgba(D+'../model/model_64_geschrapt.png')
G=Image.open(D+'../../../../../graphics/pokemon/gengar/anim_front.png').convert('RGBA').crop((0,0,64,64))
def op(im,kleur,s):
    b=Image.new('RGBA',im.size,kleur); b.alpha_composite(im); return b.resize((im.width*s,im.height*s),Image.NEAREST)
W=3*512+64; V=Image.new('RGB',(W,3000),(235,235,235)); d=ImageDraw.Draw(V); y=8
for i,t in enumerate(('v5 8x','v4 8x','model 8x')): d.text((16+i*528,y),t,fill=(0,0,0))
y+=14
for i,im in enumerate((V5,V4,M)): V.paste(op(im,(255,255,255,255),8),(16+i*528,y))
y+=524; x=16
for kleur in ((255,255,255,255),(40,40,48,255)):
    for s in (1,2):
        for im in (V5,V4): V.paste(op(im,kleur,s),(x,y)); x+=64*s+8
        x+=16
d.text((x,y+8),'1x/2x licht en donker: telkens v5 | v4',fill=(0,0,0)); y+=128+18
d.text((16,y),'gezicht 12x: v5 | v4 | Gengar (gezicht, 12x)',fill=(0,0,0)); y+=14; x=16
box=(27,48,7,34)
for im,b in ((V5,box),(V4,box),(G,(24,42,14,41))):
    y0,y1,x0,x1=b; c=op(im,(255,255,255,255),1).crop((x0,y0,x1,y1)).resize(((x1-x0)*12,(y1-y0)*12),Image.NEAREST)
    V.paste(c,(x,y)); x+=c.width+12
y+=c.height+16
V.crop((0,0,W,y)).save(D+'vel.png'); print('vel.png')
