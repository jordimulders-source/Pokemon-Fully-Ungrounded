import numpy as np
from PIL import Image, ImageDraw
def rgba(p): return Image.open(p).convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
r10=rgba('samba.png'); r9=rgba('r9_ref.png'); cum=rgba('../../cumbia/af/cumbia.png'); tan=rgba('../../tango/af/tango.png')
A=np.array(Image.open('samba.png')); B=np.array(Image.open('r9_ref.png'))
D=np.zeros((64,64,3),np.uint8)+235; D[B>0]=(200,200,200); D[A!=B]=(240,200,0)
W=Image.new('RGB',(3*532,30+512+40+70),(232,232,232)); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate([(op(r10,'white',8),'samba r10 (8x)'),(op(r9,'white',8),'samba r9 (8x)'),(Image.fromarray(D).resize((512,512),Image.NEAREST),'diff r9->r10 (%d px, silhouet 0)'%int((A!=B).sum()))]):
    W.paste(im,(i*532,30)); d.text((i*532+4,10),t,fill='black')
y=30+512+40; d.text((4,y-18),'1x: r10 | cumbia | tango op wit, donker, gevechtsgroen',fill='black'); xx=0
for bg in [(255,255,255),(40,40,48),(152,208,160)]:
    for im in (r10,cum,tan): W.paste(op(im,bg,1),(xx,y)); xx+=68
    xx+=16
W.save('vel.png')
