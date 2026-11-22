# vel.png r7: r7 | r6 | model (8x) ; tooiveer 12x en poot 12x: r7 | r6 | model (zelfde uitsnede) ; poten-varianten A | B ; 1x/2x naast cumbia en tango af
from PIL import Image, ImageDraw
def rgba(p): return Image.open(p).convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
m=Image.open('../model/gemini_r10.png').convert('RGB'); x0,y0,s=19.3344,29.216,950.272; k=s/64
def mcrop(box,z):
    return m.crop((int(x0+box[0]*k),int(y0+box[1]*k),int(x0+box[2]*k),int(y0+box[3]*k))).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.LANCZOS)
r7=rgba('samba.png'); r6=rgba('r6_ref.png'); B=rgba('variant_B.png')
cum=rgba('../../cumbia/af/cumbia.png'); tan=rgba('../../tango/af/tango.png')
W=Image.new('RGB',(1606,30+512+40+228+40+204+40+140),(232,232,232)); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate([(op(r7,'white',8),'samba r7 (8x)'),(op(r6,'white',8),'samba r6 (8x)'),(mcrop((0,0,64,64),8),'model gemini_r10 (zelfde schaal en plaats)')]):
    W.paste(im,(i*532,30)); d.text((i*532+4,10),t,fill='black')
y=30+512+40; tb=(10,13,29,24)
d.text((4,y-18),'meest linkse tooiveer 12x: r7 | r6 | model',fill='black')
for i,im in enumerate([op(r7.crop(tb),'white',12),op(r6.crop(tb),'white',12),mcrop(tb,12)]): W.paste(im,(i*(19*12+10),y))
y2=y+228+40; pb=(20,47,37,64)
d.text((4,y2-18),'opgetild been 12x: r7 (variant A, gekozen) | r6 | model | variant B',fill='black')
for i,im in enumerate([op(r7.crop(pb),'white',12),op(r6.crop(pb),'white',12),mcrop(pb,12),op(B.crop(pb),'white',12)]): W.paste(im,(i*(17*12+10),y2))
y3=y2+204+40; d.text((4,y3-18),'1x: samba r7 | cumbia af | tango af op wit, donker, gevechtsgroen   (en 2x)',fill='black')
xx=0
for bg in [(255,255,255),(40,40,48),(152,208,160)]:
    for im in (r7,cum,tan): W.paste(op(im,bg,1),(xx,y3)); xx+=68
    xx+=16
xx+=20
for im in (r7,cum,tan): W.paste(op(im,(152,208,160),2),(xx,y3)); xx+=132
W.save('vel.png'); print(W.size)
