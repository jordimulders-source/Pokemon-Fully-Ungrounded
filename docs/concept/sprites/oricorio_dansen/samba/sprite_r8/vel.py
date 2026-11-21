# vel.png r8: r8 | r7 (8x) ; tooiveer 12x: r8 | r7 | model ; 1x/2x naast cumbia en tango af
from PIL import Image, ImageDraw
def rgba(p): return Image.open(p).convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
m=Image.open('../model/gemini_r10.png').convert('RGB'); x0,y0,s=19.3344,29.216,950.272; k=s/64
def mcrop(b,z): return m.crop((int(x0+b[0]*k),int(y0+b[1]*k),int(x0+b[2]*k),int(y0+b[3]*k))).resize(((b[2]-b[0])*z,(b[3]-b[1])*z),Image.LANCZOS)
r8=rgba('samba.png'); r7=rgba('r7_ref.png'); cum=rgba('../../cumbia/af/cumbia.png'); tan=rgba('../../tango/af/tango.png')
W=Image.new('RGB',(1074,30+512+40+156+40+140),(232,232,232)); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate([(op(r8,'white',8),'samba r8 (8x)'),(op(r7,'white',8),'samba r7 (8x)')]): W.paste(im,(i*532,30)); d.text((i*532+4,10),t,fill='black')
y=30+512+40; b=(38,12,52,25); d.text((4,y-18),'tweede tooiveer van rechts onder 12x: r8 | r7 | model',fill='black')
for i,im in enumerate([op(r8.crop(b),'white',12),op(r7.crop(b),'white',12),mcrop(b,12)]): W.paste(im,(i*(14*12+10),y))
y3=y+156+40; d.text((4,y3-18),'1x: samba r8 | cumbia af | tango af op wit, donker, gevechtsgroen   (en 2x)',fill='black')
xx=0
for bg in [(255,255,255),(40,40,48),(152,208,160)]:
    for im in (r8,cum,tan): W.paste(op(im,bg,1),(xx,y3)); xx+=68
    xx+=16
for im in (r8,cum,tan): W.paste(op(im,(152,208,160),2),(xx,y3)); xx+=132
W.save('vel.png')
