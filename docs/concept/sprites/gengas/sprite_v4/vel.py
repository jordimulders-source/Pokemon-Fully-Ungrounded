# vel.png: v4 | v3 | model 8x; close-ups 12x (v4 | v3 | model): lichtvlek, en de plekken waar r -> m ging (kop + linkeroor).
from PIL import Image, ImageDraw
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
def rgba(p): return Image.open(p).convert('RGBA')
ims=[rgba(D+'gengas_v4.png'),rgba(D+'../sprite_v3/gengas_v3.png'),rgba(D+'../model/model_64_geschrapt.png')]
def op(im,s):
    b=Image.new('RGBA',im.size,(255,255,255,255)); b.alpha_composite(im); return b.resize((im.width*s,im.height*s),Image.NEAREST)
W=3*512+64; V=Image.new('RGB',(W,2000),(235,235,235)); d=ImageDraw.Draw(V); y=8
for i,t in enumerate(('v4 8x','v3 8x','model_64_geschrapt 8x')): d.text((16+i*528,y),t,fill=(0,0,0))
y+=14
for i,im in enumerate(ims): V.paste(op(im,8),(16+i*528,y))
y+=524
for naam,(y0,y1,x0,x1) in (('lichtvlek 12x: v4 | v3 | model',(12,26,12,30)),('selout r->m: bovenkant kop en linkeroor 12x: v4 | v3 | model',(4,18,10,38))):
    d.text((16,y),naam,fill=(0,0,0)); y+=14; x=16
    for im in ims:
        c=op(im,1).crop((x0,y0,x1,y1)).resize(((x1-x0)*12,(y1-y0)*12),Image.NEAREST); V.paste(c,(x,y)); x+=c.width+12
    y+=c.height+16
V.crop((0,0,W,y)).save(D+'vel.png'); print('vel.png')
