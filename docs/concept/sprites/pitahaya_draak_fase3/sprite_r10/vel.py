# vel.png r10: rij 1 A | B | r9 | model op 8x; close-ups 12x: knots + been (A | r9 | model) en kop (A | B | r9 | model);
# onderaan 1x en 2x op licht en donker: A, B, r9, Salamence, Tyranitar, Sceptile (Gen 3). Gebruik: python3 vel.py [tijdelijke map]
import sys; from PIL import Image, ImageDraw; sys.path.insert(0,'../sprite_r6'); from box import mx,my
SP=sys.argv[1] if len(sys.argv)>1 else '/tmp'
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.save(SP+'/_vel10.png',transparency=0); im=Image.open(SP+'/_vel10.png')
    return im.convert('RGBA').crop((0,0,64,64))
A=rgba('pitahaya3_r10_A.png'); B=rgba('pitahaya3_r10_B.png'); C=rgba('../sprite_r9/pitahaya3_r9.png')
G=[rgba('../../../../../graphics/pokemon/%s/anim_front.png'%n) for n in ('salamence','tyranitar','sceptile')]
def model(x0,y0,x1,y1,Z):
    M=Image.open('../model/model_zonder_tong.png').convert('RGBA')
    return M.crop((int(mx(x0)),int(my(y0)),int(mx(x1)),int(my(y1)))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
def op_wit(t,x0,y0,x1,y1,Z):
    bg=Image.new('RGBA',t.size,(255,255,255,255)); bg.alpha_composite(t); return bg.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
K=4*532; vel=Image.new('RGBA',(K,2600),(200,200,200,255)); d=ImageDraw.Draw(vel)
y=14
for i,(im,t) in enumerate([(op_wit(A,0,8,64,64,8),'r10 A (3 pitjes) 8x'),(op_wit(B,0,8,64,64,8),'r10 B (vlees in schaduw) 8x'),
                           (op_wit(C,0,8,64,64,8),'r9 8x'),(model(0,8,64,64,8),'model zonder tong')]):
    vel.alpha_composite(im,(i*532,y)); d.text((i*532+4,2),t,fill=(0,0,0))
y+=56*8+30
for naam,box,lst in (('knots + been',(12,40,34,60),((A,'r10'),(C,'r9'))),('kop',(0,12,22,35),((A,'r10 A'),(B,'r10 B'),(C,'r9')))):
    x=0
    for im,t in [(op_wit(T,*box,12),naam+' '+t+' 12x') for T,t in lst]+[(model(*box,12),naam+' model')]:
        vel.alpha_composite(im,(x,y)); d.text((x+4,y-12),t,fill=(0,0,0)); x+=im.size[0]+12
    y+=(box[3]-box[1])*12+30
for j,(bgc,x) in enumerate((((255,255,255,255),10),((40,40,48,255),1060))):
    vel.paste(Image.new('RGBA',(1040,300),bgc),(x,y))
    for k,t in enumerate((A,B,C)+tuple(G)):
        vel.alpha_composite(t,(x+10+k*70,y+10)); vel.alpha_composite(t.resize((128,128),Image.NEAREST),(x+10+k*145,y+90))
d.text((10,y+285),'1x en 2x: r10 A, r10 B, r9, Salamence, Tyranitar, Sceptile (Gen 3)',fill=(0,0,0))
vel=vel.crop((0,0,K,y+300)); vel.convert('RGB').save('vel.png'); print(vel.size)
