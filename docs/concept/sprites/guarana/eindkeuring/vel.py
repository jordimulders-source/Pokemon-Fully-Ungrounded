# vel.png: rij 1 ek | r4 | model op 8x (hoofdversie); rij 2 hetzelfde voor de variant met grotere ogen;
# rij 3: 2 maatstaf-sprites (Skinguin, Dundragoon) + 2 echte Gen 3 (Bellsprout, Hoppip; anim_front_gba + normal_gba.pal) op 8x;
# rij 4: ek en variant op 1x op wit en donker.   Gebruik (vanuit docs/concept/sprites/guarana): python3 eindkeuring/vel.py
import sys; sys.path.insert(0,'gereedschap'); from gemeen import model_op_schaal
from PIL import Image, ImageDraw
R='../../../../'
def rgba(png,pal=None):
    im=Image.open(png)
    if pal:
        L=open(pal).read().split('\n')[3:]; cols=[tuple(map(int,l.split())) for l in L if l.strip()]
        flat=[v for c in cols for v in c]; im=im.copy(); im.putpalette(flat+[0]*(768-len(flat)))
    im=im.crop((0,0,64,64)); a=im.convert('RGBA'); px=a.load()
    for y in range(64):
        for x in range(64):
            if im.getpixel((x,y))==0: px[x,y]=(0,0,0,0)
    return a
def op(im,bg,z): b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB').resize((64*z,64*z),Image.NEAREST)
Z=8; T=64*Z; W=Image.new('RGB',(4*T+50,3*(T+24)+200),(255,255,255)); d=ImageDraw.Draw(W)
model=model_op_schaal().convert('RGB').resize((T,T),Image.NEAREST)
rijen=[[('ek hoofdversie',rgba('eindkeuring/guarana_ek.png')),('r4 hoofdversie',rgba('sprite_r4/guarana_r4.png')),('model (op schaal)',None)],
       [('ek ogen groter',rgba('eindkeuring/guarana_ek_ogen_groter.png')),('r4 ogen groter',rgba('sprite_r4/r4_ogen_groter.png')),('model (op schaal)',None)],
       [('maatstaf Skinguin',rgba(R+'docs/concept/sprites/skinguin/af/skinguin.png')),('maatstaf Dundragoon',rgba(R+'docs/concept/sprites/dundragoon/af/dundragoon.png')),
        ('Gen 3 Bellsprout',rgba(R+'graphics/pokemon/bellsprout/anim_front_gba.png',R+'graphics/pokemon/bellsprout/normal_gba.pal')),
        ('Gen 3 Hoppip',rgba(R+'graphics/pokemon/hoppip/anim_front_gba.png',R+'graphics/pokemon/hoppip/normal_gba.pal'))]]
for r,rij in enumerate(rijen):
    y=r*(T+24)
    for i,(naam,im) in enumerate(rij):
        x=i*(T+16); d.text((x+4,y+4),naam,fill=0)
        W.paste(model if im is None else op(im,(255,255,255,255),Z),(x,y+20))
y=3*(T+24)+10; x=0
for naam in ('eindkeuring/guarana_ek.png','eindkeuring/guarana_ek_ogen_groter.png'):
    im=rgba(naam)
    for bg in ((255,255,255,255),(40,40,48,255)):
        W.paste(op(im,bg,1),(x,y)); W.paste(op(im,bg,2),(x+70,y)); x+=210
d.text((4,y+140),'1x en 2x op wit en donker: ek hoofdversie, ek ogen groter',fill=0)
W.save('eindkeuring/vel.png'); print(W.size)
