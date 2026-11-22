# vel.png r6: r6 | r5 | model (8x) ; poten 12x: r6 | variant B | r5 | model | Baile ; 1x wit/donker/groen naast cumbia en tango af
import numpy as np; from PIL import Image, ImageDraw
from poten_vel import maak as poten
def rgba(p): return Image.open(p).convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
r6=rgba('samba.png'); r5=rgba('r5_ref.png')
m=Image.open('../model/gemini_r10.png').convert('RGB'); x0,y0,s=19.3344,29.216,950.272
mc=m.crop((int(x0),int(y0),int(x0+s),int(y0+s))).resize((512,512),Image.LANCZOS)
cum=rgba('../../cumbia/af/cumbia.png'); tan=rgba('../../tango/af/tango.png')
P=poten(['samba.png','variant_B.png','r5_ref.png'],'poten_12x.png')
W=Image.new('RGB',(max(3*532,P.width)+10,30+512+40+P.height+40+140),(232,232,232)); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate([(op(r6,'white',8),'samba r6 (8x)'),(op(r5,'white',8),'samba r5 (8x)'),(mc,'model gemini_r10 (zelfde schaal en plaats)')]):
    W.paste(im,(i*532,30)); d.text((i*532+4,10),t,fill='black')
y=30+512+40; d.text((4,y-18),'poten 12x: r6 (variant A, gekozen) | variant B | r5 | model | Baile',fill='black'); W.paste(P,(0,y))
y2=y+P.height+40; d.text((4,y2-18),'1x: samba r6 | cumbia af | tango af op wit, donker, gevechtsgroen   (en 2x)',fill='black')
xx=0
for bg in [(255,255,255),(40,40,48),(152,208,160)]:
    for im in (r6,cum,tan): W.paste(op(im,bg,1),(xx,y2)); xx+=68
    xx+=16
xx+=20
for im in (r6,cum,tan): W.paste(op(im,(152,208,160),2),(xx,y2)); xx+=132
W.save('vel.png'); print(W.size)
