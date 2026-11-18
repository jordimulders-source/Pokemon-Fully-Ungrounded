# vel.png r13: kop 12x (x0-22, y18-36) F | G | H | r12 | model; hele sprite 6x; 1x en 2x op licht en donker.
# 1x en 2x op licht en donker naast Salamence, Tyranitar, Sceptile. Gebruik: python3 vel.py [tijdelijke map]
import sys; from PIL import Image, ImageDraw; sys.path.insert(0,'../sprite_r6'); from box import mx,my
SP=sys.argv[1] if len(sys.argv)>1 else '/tmp'
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.save(SP+'/_vel13.png',transparency=0); im=Image.open(SP+'/_vel13.png')
    return im.convert('RGBA').crop((0,0,64,64))
L=[(rgba('pitahaya3_r13_%s.png'%n),n) for n in 'FGH']+[(rgba('../sprite_r12/pitahaya3_r12.png'),'r12')]
G=[rgba('../../../../../graphics/pokemon/%s/anim_front.png'%n) for n in ('salamence','tyranitar','sceptile')]
def op_wit(t,x0,y0,x1,y1,Z):
    bg=Image.new('RGBA',t.size,(255,255,255,255)); bg.alpha_composite(t); return bg.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
M=Image.open('../model/model_zonder_tong.png').convert('RGBA').crop((int(mx(0)),int(my(18)),int(mx(22)),int(my(36)))).resize((264,216),Image.LANCZOS)
K=1600; vel=Image.new('RGBA',(K,1500),(200,200,200,255)); d=ImageDraw.Draw(vel); y=14; x=0
for T,t in L:
    vel.alpha_composite(op_wit(T,0,18,22,36,12),(x,y)); d.text((x+4,y-12),'kop 12x '+t,fill=(0,0,0)); x+=274
vel.alpha_composite(M,(x,y)); d.text((x+4,y-12),'model',fill=(0,0,0)); y+=216+30; x=0
for T,t in L:
    vel.alpha_composite(op_wit(T,0,10,64,64,6),(x,y)); d.text((x+4,y-12),t+' 8x',fill=(0,0,0)); x+=390
y+=54*6+20
for bgc,x in (((255,255,255,255),10),((40,40,48,255),800)):
    vel.paste(Image.new('RGBA',(780,250),bgc),(x,y))
    for k,(T,t) in enumerate(L): vel.alpha_composite(T,(x+8+k*66,y+10)); vel.alpha_composite(T.resize((128,128),Image.NEAREST),(x+8+k*135,y+90))
    for k,T in enumerate(G): vel.alpha_composite(T,(x+8+(k+4)*66,y+10))
d.text((10,y+235),'1x: F, G, H, r12, Salamence, Tyranitar, Sceptile | 2x: F, G, H, r12',fill=(0,0,0))
vel=vel.crop((0,0,K,y+250)); vel.convert('RGB').save('vel.png'); print(vel.size)
