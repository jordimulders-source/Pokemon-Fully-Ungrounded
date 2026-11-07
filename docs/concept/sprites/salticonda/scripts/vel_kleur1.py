"""Vel kleurronde 1: A en E op 4x en 1x, licht en donker, met pre-evolutie en 5 referenties."""
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'
D=R+'docs/concept/sprites/salticonda/'
def ld(f):
    p=Image.open(f).crop((0,0,64,64)); m=p.point(lambda v: 0 if v==0 else 255, mode='L') if False else None
    P=p.load(); im=p.convert('RGBA'); Q=im.load()
    for x in range(64):
        for y in range(64):
            if P[x,y]==0: Q[x,y]=(0,0,0,0)
    return im
A=ld(D+'kleur1/salticonda_A.png'); E=ld(D+'kleur1/salticonda_E.png')
pre=ld(D+'../silicobra_uyuni/af/silicobra_uyuni.png')
refs=[(n,ld(R+'graphics/pokemon/%s/anim_front.png'%n)) for n in ['hippowdon','torkoal','camerupt','sandaconda','wailord']]
LIGHT=(236,232,222,255); DARK=(44,44,52,255)
W,H=1320,900
vel=Image.new('RGBA',(W,H),LIGHT); d=ImageDraw.Draw(vel)
d.rectangle([0,450,W,H],fill=DARK)
def txt(x,y,s,c=(30,30,30,255)): d.text((x,y),s,fill=c)
for row,(y0,col) in enumerate([(0,(30,30,30,255)),(450,(230,230,230,255))]):
    txt(10,y0+6,'A (silhouet ronde 1)',col); txt(280,y0+6,'E (silhouet ronde 2)',col)
    vel.alpha_composite(A.resize((256,256),Image.NEAREST),(10,y0+22))
    vel.alpha_composite(E.resize((256,256),Image.NEAREST),(280,y0+22))
    x=560
    for lab,im in [('A',A),('E',E),('Silicobra-U',pre)]:
        vel.alpha_composite(im,(x,y0+40)); txt(x,y0+108,lab,col); x+=80
    x=560
    for lab,im in [('A',A),('E',E),('Silicobra-U',pre)]:
        vel.alpha_composite(im.resize((128,128),Image.NEAREST),(x,y0+130)); x+=140
    txt(10,y0+290,'Referenties 1x en 2x',col)
    x=10
    for lab,im in [('A',A),('E',E)]+refs:
        vel.alpha_composite(im,(x,y0+310)); vel.alpha_composite(im.resize((128,128),Image.NEAREST),(x+66,y0+306)); txt(x,y0+376,lab,col); x+=196 if False else 0
        x+=0
    # leg de referenties netjes in een rij
vel=Image.new('RGBA',(W,H),LIGHT); d=ImageDraw.Draw(vel); d.rectangle([0,450,W,H],fill=DARK)
for y0,col in [(0,(30,30,30,255)),(450,(230,230,230,255))]:
    txt(10,y0+6,'A (silhouet ronde 1)  4x',col); txt(280,y0+6,'E (silhouet ronde 2)  4x',col)
    vel.alpha_composite(A.resize((256,256),Image.NEAREST),(10,y0+22))
    vel.alpha_composite(E.resize((256,256),Image.NEAREST),(280,y0+22))
    txt(560,y0+6,'1x: A, E, Silicobra-Uyuni (pre-evo)',col)
    x=560
    for im in [A,E,pre]: vel.alpha_composite(im,(x,y0+24)); x+=72
    txt(560,y0+96,'2x: A, E, pre-evo, Hippowdon, Torkoal, Camerupt, Sandaconda, Wailord',col)
    x=560
    for i,im in enumerate([A,E,pre]+[r[1] for r in refs]):
        if i==4: x=560
        yy=y0+112 if i<4 else y0+250
        vel.alpha_composite(im.resize((128,128),Image.NEAREST),(x,yy)); x+=136
    txt(10,y0+290,'1x naast de referenties',col)
    x=10
    for im in [A,E,pre]+[r[1] for r in refs]: vel.alpha_composite(im,(x,y0+306)); x+=70
vel.save(D+'kleur1/vel.png')
