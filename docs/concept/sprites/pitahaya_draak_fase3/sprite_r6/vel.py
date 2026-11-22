# vel.png r6: rij 1 r6 | r5 | model op 8x; rij 2 close-ups 12x (arm/hand, keel, kop: r6 naast model); rij 3 buik-variant 8x
# naast r6 zonder tong 8x; rij 4 1x en 2x op licht en donker (r6, zonder tong, buik) naast Salamence en Tyranitar (Gen 3).
import sys,numpy as np; from PIL import Image, ImageDraw; sys.path.insert(0,'.'); from box import mx,my
SP=sys.argv[1] if len(sys.argv)>1 else '/tmp'
def rgba(p,crop64=False):
    im=Image.open(p)
    if im.mode=='P':
        im.save(SP+'/_vel5.png',transparency=0); im=Image.open(SP+'/_vel5.png')
    im=im.convert('RGBA'); return im.crop((0,0,64,64)) if crop64 else im
A=rgba('pitahaya3_r6.png'); B=rgba('pitahaya3_r6_zonder_tong.png'); C=rgba('pitahaya3_r6_buik.png'); R5=rgba('../sprite_r5/pitahaya3_r5.png'); C5=rgba('../sprite_r5/pitahaya3_r5_buik.png')
G=[rgba('../../../../../graphics/pokemon/%s/anim_front.png'%n,True) for n in ('salamence','tyranitar')]
def model(x0,y0,x1,y1,Z,pad='../model/model.png'):
    M=Image.open(pad).convert('RGBA'); return M.crop((int(mx(x0)),int(my(y0)),int(mx(x1)),int(my(y1)))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
def op_wit(t,x0,y0,x1,y1,Z):
    bg=Image.new('RGBA',t.size,(255,255,255,255)); bg.alpha_composite(t); return bg.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
W=3*532; vel=Image.new('RGBA',(W,2000),(200,200,200,255)); d=ImageDraw.Draw(vel)
y=14
for i,(im,t) in enumerate([(op_wit(A,0,8,64,64,8),'r6 (met tong) 8x'),(op_wit(R5,0,8,64,64,8),'r5 (vorige ronde) 8x'),(model(0,8,64,64,8),'model, zelfde uitsnede')]):
    vel.alpha_composite(im,(i*532,y)); d.text((i*532+4,2),t,fill=(0,0,0))
y+=56*8+30; x=0
for naam,box in (('arm/hand',(26,32,42,50)),('keel',(10,26,24,37)),('kop',(0,12,22,30))):
    for im,t in ((op_wit(A,*box,12),naam+' r6 12x'),(model(*box,12),naam+' model')):
        if x+im.size[0]>W: x=0; y+=hmax+30
        vel.alpha_composite(im,(x,y)); d.text((x+4,y-12),t,fill=(0,0,0)); x+=im.size[0]+12; hmax=max(im.size[1],locals().get('hmax',0))
y+=hmax+30
for i,(im,t) in enumerate([(op_wit(C,0,8,64,64,8),'r6 BUIK (Jordi: vruchtvlees, wit met zwarte spikkels) 8x'),(op_wit(C,12,26,36,46,18),'buik close-up r6 18x'),(op_wit(C5,12,26,36,46,18),'buik close-up r5 18x')]):
    vel.alpha_composite(im,(i*532,y)); d.text((i*532+4,y-12),t,fill=(0,0,0))
y+=max(56*8,20*18)+30
for j,(bgc,x) in enumerate((((255,255,255,255),10),((40,40,48,255),800))):
    vel.paste(Image.new('RGBA',(770,290),bgc),(x,y))
    for k,t in enumerate((A,B,C,G[0],G[1])):
        vel.alpha_composite(t,(x+10+k*70,y+10)); vel.alpha_composite(t.resize((128,128),Image.NEAREST),(x+10+k*150,y+90))
d.text((10,y+275),'1x en 2x: r6, r6 zonder tong, r6 buik, Salamence, Tyranitar (Gen 3)',fill=(0,0,0))
vel=vel.crop((0,0,W,y+295)); vel.convert('RGB').save('vel.png'); print(vel.size)
