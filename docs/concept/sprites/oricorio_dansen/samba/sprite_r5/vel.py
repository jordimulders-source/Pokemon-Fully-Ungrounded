# vel.png r5: r5 | r4 | model (8x, zelfde schaal en plaats) ; poten 12x: r5 | r4 | Baile ; diffkaart t.o.v. r4 (kleur anders = geel,
# silhouet erbij = groen, silhouet eraf = rood) ; 1x op wit/donker/gevechtsgroen: samba r5 | cumbia af | tango af
import numpy as np; from PIL import Image, ImageDraw
def rgba(p): return Image.open(p).convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
r5=rgba('samba.png'); r4=rgba('r4_ref.png')
m=Image.open('../model/gemini_r10.png').convert('RGB'); x0,y0,s=19.3344,29.216,950.272
mc=m.crop((int(x0),int(y0),int(x0+s),int(y0+s))).resize((512,512),Image.LANCZOS)
baile=rgba('../../../../../../graphics/pokemon/oricorio/anim_front.png').crop((0,0,64,64))
cum=rgba('../../cumbia/af/cumbia.png'); tan=rgba('../../tango/af/tango.png')
W=Image.new('RGB',(3*532+10,30+512+40+228+40+256+40+90),(232,232,232)); d=ImageDraw.Draw(W)
for i,(im,t) in enumerate([(op(r5,'white',8),'samba r5 (8x)'),(op(r4,'white',8),'samba r4 (8x)'),(mc,'model gemini_r10 (zelfde schaal en plaats)')]):
    W.paste(im,(i*532,30)); d.text((i*532+4,10),t,fill='black')
y=30+512+40
d.text((4,y-18),'poten 12x: r5 | r4 | Baile (standbeen en voeten = Baile-pixels in samba-palet; opgetild been nu dun en schuin)',fill='black')
W.paste(op(r5.crop((21,48,40,63)),'white',12),(0,y)); W.paste(op(r4.crop((21,48,40,63)),'white',12),(240,y)); W.paste(op(baile.crop((16,47,35,62)),'white',12),(480,y))
# diffkaart
a=np.array(Image.open('samba.png')); b=np.array(Image.open('r4_ref.png'))
g=np.array(Image.open('samba.png').convert('L').convert('RGB'))//2+100
g[(a!=b)&(a>0)&(b>0)]=(240,200,0); g[(a>0)&(b==0)]=(0,170,0); g[(a==0)&(b>0)]=(220,0,0); g[(a==0)&(b==0)]=(255,255,255)
dk=Image.fromarray(g.astype(np.uint8)).resize((256,256),Image.NEAREST)
sil=np.full((64,64,3),255,np.uint8); sil[(a>0)&(b>0)]=(200,200,200); sil[(a>0)&(b==0)]=(0,170,0); sil[(a==0)&(b>0)]=(220,0,0)
sk=Image.fromarray(sil).resize((256,256),Image.NEAREST)
W.paste(dk,(760,y)); W.paste(sk,(1030,y))
d.text((760,y-18),'diff t.o.v. r4: geel = andere kleur, groen = erbij, rood = eraf | alleen silhouet',fill='black')
y2=y+256+40; d.text((4,y2-18),'1x: samba r5 | cumbia af | tango af  op wit, donker, gevechtsgroen   (en 2x)',fill='black')
xx=0
for bg in [(255,255,255),(40,40,48),(152,208,160)]:
    for im in (r5,cum,tan): W.paste(op(im,bg,1),(xx,y2)); xx+=68
    xx+=16
xx+=20
for im in (r5,cum,tan): W.paste(op(im,(152,208,160),2),(xx,y2)); xx+=132
W.save('vel.png'); print(W.size)
