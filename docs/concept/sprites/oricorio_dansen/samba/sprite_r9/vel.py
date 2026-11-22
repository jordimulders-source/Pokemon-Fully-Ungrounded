# vel.png r9: r9 | r8 (8x) | diffkaart (8x; rood = alpha gewijzigd, geel = herkleurd) ; gat tooiveer 12x: r9 | r8 | model ;
# 1x op wit, donker, gevechtsgroen naast cumbia en tango af (en 2x op gevechtsgroen)
import numpy as np
from PIL import Image, ImageDraw
def rgba(p): return Image.open(p).convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
m=Image.open('../model/gemini_r10.png').convert('RGB'); x0,y0,s=19.3344,29.216,950.272; k=s/64
def mcrop(b,z): return m.crop((int(x0+b[0]*k),int(y0+b[1]*k),int(x0+b[2]*k),int(y0+b[3]*k))).resize(((b[2]-b[0])*z,(b[3]-b[1])*z),Image.LANCZOS)
r9=rgba('samba.png'); r8=rgba('r8_ref.png'); cum=rgba('../../cumbia/af/cumbia.png'); tan=rgba('../../tango/af/tango.png')
A=np.array(Image.open('samba.png')); B=np.array(Image.open('r8_ref.png'))
D=np.zeros((64,64,3),np.uint8)+235; D[B>0]=(200,200,200); D[(A!=B)]=(240,200,0); D[(A>0)!=(B>0)]=(220,0,0)
dif=Image.fromarray(D).resize((512,512),Image.NEAREST)
W=Image.new('RGB',(3*532,30+512+40+204+40+140),(232,232,232)); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate([(op(r9,'white',8),'samba r9 (8x)'),(op(r8,'white',8),'samba r8 (8x)'),(dif,'diff r8->r9: geel herkleurd (%d), rood silhouet (%d)'%(int((A!=B).sum()),int(((A>0)!=(B>0)).sum())))]):
    W.paste(im,(i*532,30)); d.text((i*532+4,10),t,fill='black')
y=30+512+40; b=(38,10,54,27); d.text((4,y-18),'gat tooiveer (Jordi) 12x: r9 | r8 | model',fill='black')
for i,im in enumerate([op(r9.crop(b),'white',12),op(r8.crop(b),'white',12),mcrop(b,12)]): W.paste(im,(i*(16*12+10),y))
y3=y+204+40; d.text((4,y3-18),'1x: samba r9 | cumbia af | tango af op wit, donker, gevechtsgroen   (en 2x)',fill='black')
xx=0
for bg in [(255,255,255),(40,40,48),(152,208,160)]:
    for im in (r9,cum,tan): W.paste(op(im,bg,1),(xx,y3)); xx+=68
    xx+=16
for im in (r9,cum,tan): W.paste(op(im,(152,208,160),2),(xx,y3)); xx+=132
W.save('vel.png')
