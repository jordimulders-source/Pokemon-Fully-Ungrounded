# vel.png: sprite 8x | model 8x; daaronder 1x en 2x op licht en donker; close-ups 12x (sprite | model).
from PIL import Image, ImageDraw
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
def rgba(p): return Image.open(p).convert('RGBA')
S=rgba(D+'gengas_v2.png'); M=rgba(D+'../model/model_64_geschrapt.png'); R3=rgba(D+'../sprite_r3/gengas_r3.png')
import numpy as np
m=np.asarray(M).copy(); w=(m[...,:3].min(2)>=232)
# modelachtergrond (wit, buitenkant) transparant maken voor de 1x/2x-weergave is niet nodig: model alleen op wit
def op(im,kleur,s):
    b=Image.new('RGBA',im.size,kleur); b.alpha_composite(im); return b.resize((im.width*s,im.height*s),Image.NEAREST)
LICHT=(255,255,255,255); DONKER=(40,40,48,255)
W=64*8*2+48; regels=[]
V=Image.new('RGB',(W,4000),(235,235,235)); d=ImageDraw.Draw(V); y=10
d.text((16,y),'Gengas v2: sprite (gengas_v2.png) 8x',fill=(0,0,0)); d.text((64*8+40,y),'model_64_geschrapt.png 8x',fill=(0,0,0)); y+=16
V.paste(op(S,LICHT,8),(16,y)); V.paste(op(M,LICHT,8),(64*8+32,y)); y+=64*8+16
x=16
for kleur in (LICHT,DONKER):
    for s in (1,2):
        V.paste(op(S,kleur,s),(x,y)); x+=64*s+16
d.text((x+8,y+8),'1x en 2x op licht en donker',fill=(0,0,0)); y+=128+20
def crop(im,box,s=12,kleur=LICHT):
    y0,y1,x0,x1=box; return op(im,kleur,1).crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST)
# gezicht: r3 | hybride | model (model op zijn eigen plek, zelfde uitsnede)
box=(26,48,5,36)
d.text((16,y),'gezicht 12x: r3 (positie) | v2 hybride | model (grootte)',fill=(0,0,0)); y+=14
x=16
for im in (R3,S,M):
    c=crop(im,box); V.paste(c,(x,y)); x+=c.width+12
y+=c.height+16
delen=[('linkeroor',(3,30,6,26)),('onder het rechteroor',(10,32,40,60)),('wervel',(26,44,32,50)),('lichtvlek',(12,26,12,30)),
       ('maan boven',(0,11,23,39)),('maan links',(39,53,0,12)),('maan rechts',(18,33,50,64)),('maan rechtsonder',(48,64,38,57))]
x=16; rowh=0
for naam,box in delen:
    a=crop(S,box); b=crop(M,box); bw=a.width*2+8
    if x+bw>W-8: x=16; y+=rowh+18; rowh=0
    d.text((x,y),naam+' 12x: v2 | model',fill=(0,0,0))
    V.paste(a,(x,y+14)); V.paste(b,(x+a.width+8,y+14)); x+=bw+24; rowh=max(rowh,a.height+14)
y+=rowh+16
V.crop((0,0,W,y)).save(D+'vel.png'); print('vel.png',W,y)
