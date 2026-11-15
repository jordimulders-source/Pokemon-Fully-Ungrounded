# vel.png: v8a | v8b | v7 | model op 8x; 1x/2x/3x op licht en donker (v8a | v8b | v7); gezicht+krul 10x: v8a | v8b | Gengar
from PIL import Image, ImageDraw
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
def rgba(p): return Image.open(p).convert('RGBA')
A=rgba(D+'gengas_v8a.png'); B=rgba(D+'gengas_v8b.png'); V7=rgba(D+'../sprite_v7/gengas_v7.png'); M=rgba(D+'../model/model_64_geschrapt.png')
G=Image.open(D+'../../../../../graphics/pokemon/gengar/anim_front.png').convert('RGBA').crop((0,0,64,64))
def op(im,kleur,s):
    b=Image.new('RGBA',im.size,kleur); b.alpha_composite(im); return b.resize((im.width*s,im.height*s),Image.NEAREST)
W=max(4*528+16,16+2*3*(64+128+192+24)+64); V=Image.new('RGB',(W,1700),(235,235,235)); d=ImageDraw.Draw(V); y=8
for i,t in enumerate(('v8a 8x','v8b 8x','v7 8x','model 8x')): d.text((16+i*528,y),t,fill=(0,0,0))
y+=14
for i,im in enumerate((A,B,V7,M)): V.paste(op(im,(255,255,255,255),8),(16+i*528,y))
y+=524; x=16
for kleur in ((255,255,255,255),(40,40,48,255)):
    for s in (1,2,3):
        for im in (A,B,V7): V.paste(op(im,kleur,s),(x,y)); x+=64*s+8
        x+=16
d.text((16,y+196),'1x/2x/3x licht en donker: telkens v8a | v8b | v7',fill=(0,0,0)); y+=212
d.text((16,y),'gezicht + krul 10x: v8a | v8b | Gengar (gezicht)',fill=(0,0,0)); y+=14; x=16
for im,(x0,y0,x1,y1) in ((A,(4,20,48,50)),(B,(4,20,48,50)),(G,(10,15,54,45))):
    c=op(im,(255,255,255,255),1).crop((x0,y0,x1,y1)); c=c.resize((c.width*10,c.height*10),Image.NEAREST)
    V.paste(c,(x,y)); x+=c.width+12
y+=c.height+16
V.crop((0,0,W,y)).save(D+'vel.png'); print('vel.png')
