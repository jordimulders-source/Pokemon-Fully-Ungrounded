# vel.png r9: r9 | r8 (8x) | diffkaart (gewijzigde pixels magenta over r8); 1x en 2x op wit/donker/gevechtsgroen naast Murkrow en Umbreon
import numpy as np; from PIL import Image, ImageDraw
G=(152,208,160); GR='../../../../../../graphics/pokemon/'
def rgba(p): return Image.open(p).convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
def gen3(n):
    a=np.array(Image.open(GR+n+'/anim_front.png'))[:64]; t=Image.fromarray(a,'P')
    lines=open(GR+n+'/normal.pal').read().split('\n')[3:19]; t.putpalette([int(v) for l in lines for v in l.split()])
    t.save('/tmp/_g.png',transparency=0); return rgba('/tmp/_g.png')
A=rgba('tango.png'); R7=rgba('r8_ref.png'); MU=gen3('murkrow'); UM=gen3('umbreon')
d8=np.load('tango_r9.npy')!=np.load('tango_r8.npy')
W=Image.new('RGB',(3*522,30+512+40+150),(230,230,230)); d=ImageDraw.Draw(W)
dm=op(A,'white',8); dd=ImageDraw.Draw(dm)
for y,x in zip(*np.where(d8)): dd.rectangle([x*8,y*8,x*8+7,y*8+7],outline=(255,0,255),width=2)
for k,(im,t) in enumerate([(op(A,'white',8),'r9 tango.png'),(op(R7,'white',8),'r8'),(dm,'diff r9 t.o.v. r8 (magenta): %d px'%d8.sum())]):
    W.paste(im,(k*522,30)); d.text((k*522+4,10),t,fill='black')
y=582; d.text((4,y),'1x en 2x: r9 | Murkrow | Umbreon op wit / donker / gevechtsgroen',fill='black'); x=0
for bg in ('white',(40,40,48),G):
    for im in (A,MU,UM): W.paste(op(im,bg,1),(x,y+20)); x+=68
    x+=16
x=700
for bg in ((40,40,48),G):
    for im in (A,MU,UM): W.paste(op(im,bg,2),(x,y+16)); x+=132
W.save('vel.png'); print(W.size)
