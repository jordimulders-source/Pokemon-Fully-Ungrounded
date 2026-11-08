# Eindkeuring nachtaap fase 3: vergelijkingsvel + uitsneden (wijzigt de sprite niet)
from PIL import Image, ImageDraw
import os
R='/home/user/Pokemon-Fully-Ungrounded/'
AF=R+'docs/concept/sprites/nachtaap_fase3/af/'
G=R+'graphics/pokemon/'
def rgba(path):
    im=Image.open(path)
    if im.mode=='P':
        im=im.crop((0,0,64,64)); px=im.load(); out=Image.new('RGBA',(64,64),(0,0,0,0)); o=out.load()
        pal=im.getpalette()
        for y in range(64):
            for x in range(64):
                i=px[x,y]
                if i: o[x,y]=tuple(pal[3*i:3*i+3])+(255,)
        return out
    return im.convert('RGBA').crop((0,0,64,64))
def ref(n):
    for f in ('anim_front_gba.png','anim_front.png'):
        if os.path.exists(G+n+'/'+f): return rgba(G+n+'/'+f)
ons=rgba(AF+'nachtaap_fase3.png')
basis=rgba(R+'docs/concept/sprites/nachtaap_fase3/kleur/ronde7c/nachtaap_fase3.png')
fase2=rgba(R+'docs/concept/sprites/nachtaap_evo/af/nachtaap_evo.png')
refs=['primeape','slaking','vigoroth','grumpig','aipom','ambipom','monferno','infernape','furret','dusclops','alakazam','medicham']
row=[('fase3',ons),('fase2',fase2)]+[(n,ref(n)) for n in refs]
BG=[(248,248,248),(40,44,52)]
W=len(row)*(64*3+8)+8
H=2*(64*3+8)+2*(64+8)+40
vel=Image.new('RGB',(W,H),BG[0]); d=ImageDraw.Draw(vel)
y=4
for bg in BG:
    d.rectangle((0,y,W,y+64*3+8),fill=bg)
    for i,(n,s) in enumerate(row):
        vel.paste(s.resize((192,192),Image.NEAREST),(8+i*200,y+4),s.resize((192,192),Image.NEAREST))
    y+=64*3+8
for bg in BG:
    d.rectangle((0,y,W,y+72),fill=bg)
    for i,(n,s) in enumerate(row):
        vel.paste(s,(8+i*200+64,y+4),s)
    y+=72
for i,(n,s) in enumerate(row): d.text((8+i*200+4,y+4),n,fill=(0,0,0))
vel.save(AF+'vel.png')
def crop8(img,box,bg,name):
    c=img.crop(box); w,h=c.size; o=Image.new('RGB',(w*8,h*8),bg); c8=c.resize((w*8,h*8),Image.NEAREST); o.paste(c8,(0,0),c8)
    dd=ImageDraw.Draw(o)
    for gx in range(0,w*8,8): dd.line((gx,0,gx,h*8),fill=(200,200,200) if bg[0]>128 else (70,70,70))
    for gy in range(0,h*8,8): dd.line((0,gy,w*8,gy),fill=(200,200,200) if bg[0]>128 else (70,70,70))
    o.save(AF+'eindkeuring/'+name)
crop8(ons,(14,22,48,50),BG[0],'rug8_licht.png')   # x14-47, y22-49
crop8(ons,(14,22,48,50),BG[1],'rug8_donker.png')
crop8(basis,(14,22,48,50),BG[0],'rug8_basis_ronde7c.png')
crop8(ons,(0,0,64,64),BG[0],'zoom8_licht.png')
crop8(ons,(0,0,64,64),BG[1],'zoom8_donker.png')
# 1x rug naast Furret/Dusclops op 4x
cmp=Image.new('RGB',(3*256+16,256),BG[0])
for i,s in enumerate([ons,ref('furret'),ref('dusclops')]):
    s4=s.resize((256,256),Image.NEAREST); cmp.paste(s4,(i*264,0),s4)
cmp.save(AF+'eindkeuring/rug_vs_furret_dusclops4.png')
