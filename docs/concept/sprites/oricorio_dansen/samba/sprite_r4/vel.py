# vel.png r4: sprite 8x | model op dezelfde schaal en plaats (gemini_r10) ; kop 12x | Pom-Pom 12x ; poten 12x | Baile 12x ; 1x wit/donker/gevechtsgroen
import numpy as np, json; from PIL import Image, ImageDraw
spr=Image.open('samba.png').convert('RGBA')
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
pl=json.load(open('plaats.json')); F=2.9
m=Image.open('../model/gemini_r10.png').convert('RGB')
def mp(v,d,o0): return ((v-d)*F+o0)*5.12+2.08-2.56
x0=mp(0,pl['dx'],0.97); y0=mp(0,pl['dy'],0); s=F*5.12*64
mc=m.crop((int(x0),int(y0),int(x0+s),int(y0+s))).resize((512,512),Image.LANCZOS)
def f1(p): return Image.open('../../../../../../graphics/pokemon/oricorio/%sanim_front.png'%p).convert('RGBA').crop((0,0,64,64))
pom=f1('pom_pom/'); baile=f1('')
W=Image.new('RGB',(1060,30+512+30+216+30+64+20),(232,232,232)); d=ImageDraw.Draw(W)
W.paste(op(spr,'white',8),(0,30)); W.paste(mc,(540,30))
d.text((4,10),'samba r4 (8x)',fill='black'); d.text((544,10),'model gemini_r10, zelfde schaal en plaats',fill='black')
y=30+512+30
d.text((4,y-18),'kop 12x: r4 | Pom-Pom (oog + snavel pixel voor pixel)',fill='black')
W.paste(op(spr.crop((21,24,39,36)),'white',12),(0,y)); W.paste(op(pom.crop((22,16,40,28)),'white',12),(224,y))
d.text((470,y-18),'poten 12x: r4 | Baile (voet standbeen = Baile-voet, DX +5)',fill='black')
W.paste(op(spr.crop((21,48,39,63)),'white',12),(470,y)); W.paste(op(baile.crop((16,48,34,63)),'white',12),(470+224,y))
y2=y+216+30; d.text((4,y2-18),'1x: wit | donker | gevechtsgroen',fill='black')
for i,bg in enumerate([(255,255,255),(40,40,48),(152,208,160)]): W.paste(op(spr,bg,1),(i*74,y2))
W.save('vel.png'); print(W.size)
