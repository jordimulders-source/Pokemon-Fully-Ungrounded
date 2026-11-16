# Vel eindkeuring DFC: r8 | sim MOET | model (natief) op 8x met MOET-pixels gemarkeerd; Gen 3-refs op 8x; 1x/2x licht en donker.
import numpy as np;from PIL import Image,ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def t(f):
    im=Image.open(f).crop((0,0,64,64));im=im if im.mode=='P' else im.convert('P');a=im.convert('RGBA');p=im.load();q=a.load()
    for y in range(64):
        for x in range(64):
            if p[x,y]==0:q[x,y]=(0,0,0,0)
    return a
def on(im,bg,z):
    b=Image.new('RGBA',(im.width*z,im.height*z),bg);b.alpha_composite(im.resize(b.size,Image.NEAREST));return b
X0,Y0,X1,Y1=14,4,50,58;Z=8
MOET=[(26,37),(29,37),(32,37)];KAN=[(17,45),(44,47)];INFO=[(39,33),(36,34),(35,35)]
r8=t('../af/pitahaya_draak.png');sim=t('sim_moet_sprite.png')
nat=Image.open('../sprite_r7/natief.png').convert('RGBA').crop((3*X0+4,3*Y0+6,3*X1+4,3*Y1+6)).resize(((X1-X0)*Z,(Y1-Y0)*Z),Image.NEAREST)
refs=[t(R+n+'/anim_front.png') for n in('treecko','cacnea','bagon','oddish','larvitar')]
W=Image.new('RGBA',(2400,1400),(255,255,255,255));d=ImageDraw.Draw(W)
G=(205,205,205,255)
for i,(lab,im) in enumerate([('r8 (af)',on(r8.crop((X0,Y0,X1,Y1)),G,Z)),('sim MOET',on(sim.crop((X0,Y0,X1,Y1)),G,Z)),('model natief',nat)]):
    x=10+i*(288+20);W.alpha_composite(im,(x,20));d.text((x,4),lab,fill=(0,0,0))
    for pts,c in((MOET,(255,0,0)),(KAN,(0,90,255)),(INFO,(255,160,0))):
        for k,(px,py) in enumerate(pts):
            rx,ry=x+(px-X0)*Z,20+(py-Y0)*Z;d.rectangle((rx,ry,rx+Z-1,ry+Z-1),outline=c,width=2)
x=3*308+10;d.text((x,20),'rood = MOET (1->8, nek: zwart tikje -> rib)\nblauw = KAN (klauwpunten)\noranje = ter info (zwarte klont onder kin)',fill=(0,0,0))
# 1x/2x
y=480;x=3*308+10
for j,bg in enumerate([(248,248,248,255),(36,36,44,255)]):
    for k,im in enumerate([r8,sim]):
        W.alpha_composite(on(im,bg,2),(x+k*136,y+j*136));W.alpha_composite(on(im,bg,1),(x+272+k*70,y+j*136))
d.text((x,y-14),'2x: r8 | sim     1x: r8 | sim',fill=(0,0,0))
# refs 8x (bbox-crop), eigen rij
y=472+300;x=10
for im in refs:
    c=on(im.crop(im.getbbox()),G,Z);W.alpha_composite(c,(x,y));x+=c.width+10
W=W.crop(W.getbbox());W.convert('RGB').save('vel.png')
