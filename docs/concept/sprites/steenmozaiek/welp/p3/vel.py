# vel.png: boven A | B | C | r11 | model op 8x (model op het spriteraster); onder 1x en 3x naast Growlithe, Vulpix en de volwassen vorm.
from PIL import Image, ImageDraw
G='../../../../../../graphics/pokemon/'
def rgba(f,crop=None):
    q=Image.open(f); im=q.convert('RGBA')
    if q.mode=='P':
        px=im.load(); a=q.load()
        for y in range(im.height):
            for x in range(im.width):
                if a[x,y]==0: px[x,y]=(0,0,0,0)
    if crop: im=im.crop(crop)
    bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg
def model64(z=8):
    m=Image.open('../../referenties/model_welp_gekozen.png').convert('RGBA'); k=16.896
    X=lambda x:99.3+(x-7)*k; Y=lambda y:191.5+(y-18)*k
    W=Image.new('RGBA',(int(64*k)+2,int(64*k)+2),(255,255,255,255)); W.paste(m,(int(-X(0)),int(-Y(0))))
    return W.resize((64*z,64*z),Image.LANCZOS)
S=['welp_p3.png','../p2/welp_p2.png']
L=['p3','p2','model']
z=8; top=[rgba(f).resize((512,512),Image.NEAREST) for f in S]+[model64()]
ref=[rgba(G+'growlithe/anim_front_gba.png',(0,0,64,64)),rgba(G+'vulpix/anim_front_gba.png',(0,0,64,64)),rgba('../../af/steenjaguar.png')]
een=[rgba(f) for f in S]+ref
W=3*520+10; H=512+30+80+64*3+40
V=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(V)
for i,im in enumerate(top): V.paste(im,(10+i*520,26)); d.text((14+i*520,6),L[i],fill=(0,0,0,255))
y=26+512+20; d.text((14,y-14),'1x: p3 p2 | Growlithe Vulpix volwassen',fill=(0,0,0,255))
for i,im in enumerate(een): V.paste(im,(10+i*70,y))
y2=y+80; d.text((14,y2-12),'3x',fill=(0,0,0,255))
for i,im in enumerate(een): V.paste(im.resize((192,192),Image.NEAREST),(10+i*200,y2))
V.save('vel.png')
# schouder op 16x naast het model (x22-44, y33-56)
import sys; sys.path.insert(0,'../p1')
import zie
box=(22,33,44,56); z=16
A=zie.grid(zie.spr('welp_p3.png',box,z),box,z); M=zie.grid(zie.orig(box,z),box,z)
V2=Image.new('RGBA',(V.width,V.height+A.height+30),(255,255,255,255)); V2.paste(V,(0,0)); d2=ImageDraw.Draw(V2)
d2.text((14,V.height+6),'schouder 16x: p3 | model',fill=(0,0,0,255))
V2.paste(A,(10,V.height+24)); V2.paste(M,(10+A.width+12,V.height+24)); V2.save('vel.png')
