# vel.png r9: rij 1 r9 | r8 | model op 8x; close-ups 12x (knots + schutblad, staart, scheen + verre been): r9 | r8 | model;
# rij 3 1x en 2x op licht en donker: r9, r8, Salamence, Tyranitar, Sceptile (Gen 3). Gebruik: python3 vel.py [tijdelijke map]
import sys; from PIL import Image, ImageDraw; sys.path.insert(0,'../sprite_r6'); from box import mx,my
SP=sys.argv[1] if len(sys.argv)>1 else '/tmp'
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.save(SP+'/_vel9.png',transparency=0); im=Image.open(SP+'/_vel9.png')
    return im.convert('RGBA').crop((0,0,64,64))
A=rgba('pitahaya3_r9.png'); C=rgba('../sprite_r8/pitahaya3_r8.png')
G=[rgba('../../../../../graphics/pokemon/%s/anim_front.png'%n) for n in ('salamence','tyranitar','sceptile')]
def model(x0,y0,x1,y1,Z):
    M=Image.open('../model/model_zonder_tong.png').convert('RGBA')
    return M.crop((int(mx(x0)),int(my(y0)),int(mx(x1)),int(my(y1)))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
def op_wit(t,x0,y0,x1,y1,Z):
    bg=Image.new('RGBA',t.size,(255,255,255,255)); bg.alpha_composite(t); return bg.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
W=3*532; vel=Image.new('RGBA',(W,2400),(200,200,200,255)); d=ImageDraw.Draw(vel)
y=14
for i,(im,t) in enumerate([(op_wit(A,0,8,64,64,8),'r9 8x'),(op_wit(C,0,8,64,64,8),'r8 8x'),(model(0,8,64,64,8),'model zonder tong, zelfde uitsnede')]):
    vel.alpha_composite(im,(i*532,y)); d.text((i*532+4,2),t,fill=(0,0,0))
y+=56*8+30
for naam,box in (('knots + schutblad',(10,44,34,62)),('staart',(30,40,63,63)),('scheen + verre been',(16,40,50,58))):
    x=0; h=0
    for im,t in ((op_wit(A,*box,12),naam+' r9 12x'),(op_wit(C,*box,12),naam+' r8'),(model(*box,12),naam+' model')):
        if x+im.size[0]>W: x=0; y+=h+30; h=0
        vel.alpha_composite(im,(x,y)); d.text((x+4,y-12),t,fill=(0,0,0)); x+=im.size[0]+12; h=max(h,im.size[1])
    y+=h+30
for j,(bgc,x) in enumerate((((255,255,255,255),10),((40,40,48,255),800))):
    vel.paste(Image.new('RGBA',(770,300),bgc),(x,y))
    for k,t in enumerate((A,C)+tuple(G)):
        vel.alpha_composite(t,(x+10+k*70,y+10)); vel.alpha_composite(t.resize((128,128),Image.NEAREST),(x+10+k*150,y+90))
d.text((10,y+285),'1x en 2x: r9, r8, Salamence, Tyranitar, Sceptile (Gen 3)',fill=(0,0,0))
vel=vel.crop((0,0,W,y+300)); vel.convert('RGB').save('vel.png'); print(vel.size)
