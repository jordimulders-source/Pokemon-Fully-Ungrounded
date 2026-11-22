# vel.png r11: kop 12x C | D | E | r10A | model; buik 12x r11 | r10A; hele sprite 4x C | D | E | r10A;
# 1x en 2x op licht en donker: C, D, E, r10A, Salamence, Tyranitar, Sceptile. Gebruik: python3 vel.py [tijdelijke map]
import sys; from PIL import Image, ImageDraw; sys.path.insert(0,'../sprite_r6'); from box import mx,my
SP=sys.argv[1] if len(sys.argv)>1 else '/tmp'
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.save(SP+'/_vel11.png',transparency=0); im=Image.open(SP+'/_vel11.png')
    return im.convert('RGBA').crop((0,0,64,64))
S={n:rgba('pitahaya3_r11_%s.png'%n) for n in 'CDE'}; R=rgba('../sprite_r10/pitahaya3_r10_A.png')
G=[rgba('../../../../../graphics/pokemon/%s/anim_front.png'%n) for n in ('salamence','tyranitar','sceptile')]
def model(x0,y0,x1,y1,Z):
    M=Image.open('../model/model_zonder_tong.png').convert('RGBA')
    return M.crop((int(mx(x0)),int(my(y0)),int(mx(x1)),int(my(y1)))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
def op_wit(t,x0,y0,x1,y1,Z):
    bg=Image.new('RGBA',t.size,(255,255,255,255)); bg.alpha_composite(t); return bg.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
K=1400; vel=Image.new('RGBA',(K,2000),(200,200,200,255)); d=ImageDraw.Draw(vel); y=14
rijen=[('kop 12x',(2,20,16,34),[(S['C'],'C'),(S['D'],'D'),(S['E'],'E'),(R,'r10A')]),
       ('buik 12x',(15,29,32,44),[(S['C'],'r11'),(R,'r10A')])]
for naam,box,lst in rijen:
    x=0
    for im,t in [(op_wit(T,*box,12),t) for T,t in lst]+[(model(*box,12),'model')]:
        vel.alpha_composite(im,(x,y)); d.text((x+4,y-12),naam+' '+t,fill=(0,0,0)); x+=im.size[0]+10
    y+=(box[3]-box[1])*12+30
x=0
for T,t in ((S['C'],'C'),(S['D'],'D'),(S['E'],'E'),(R,'r10A')):
    vel.alpha_composite(op_wit(T,0,10,64,64,5),(x,y)); d.text((x+4,y-12),t+' 5x',fill=(0,0,0)); x+=330
y+=54*5+30
for bgc,x in (((255,255,255,255),10),((40,40,48,255),700)):
    vel.paste(Image.new('RGBA',(680,300),bgc),(x,y))
    for k,t in enumerate((S['C'],S['D'],S['E'],R)+tuple(G)):
        vel.alpha_composite(t,(x+8+k*66,y+10))
    for k,t in enumerate((S['C'],S['D'],S['E'],R)):
        vel.alpha_composite(t.resize((128,128),Image.NEAREST),(x+8+k*140,y+90))
d.text((10,y+285),'1x: C, D, E, r10A, Salamence, Tyranitar, Sceptile | 2x: C, D, E, r10A',fill=(0,0,0))
vel=vel.crop((0,0,K,y+300)); vel.convert('RGB').save('vel.png'); print(vel.size)
