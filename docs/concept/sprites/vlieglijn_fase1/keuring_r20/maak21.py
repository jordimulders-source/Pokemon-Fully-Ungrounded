# keuring r20 -> kandidaat r21: alleen tint-/lijnindex op bestaande pixels, silhouet gelijk.
import shutil
from PIL import Image, ImageDraw
import refs
SRC='../sprite_r20/vlieg_r20.png'
W={ # (x,y): (oud,nieuw,regel)
 (53,19):(10,9,'geen lichte kleur op de buitenrand: vleugelpunt krijgt de selout (9) zoals de rest van de bovenrand'),
 (54,20):(6,9,'vreemde tint (grijs 6) in de vleugelgroep, cluster van 1 px: wordt selout 9 van de punt'),
 (7,23):(5,1,'open rand: lichte tint op de buitenrand van de sprietpunt -> omlijning'),
 (29,44):(9,1,'open rand middenpoot (kabelglans grenst aan achtergrond) -> omlijning'),
 (30,44):(3,9,'kabelglans loopt door (29,43)->(30,44)->(30,45), geen gat in de binnenlijn'),
 (23,40):(1,9,'klont zwart / dubbele lijn x23-24 r39-40: pootkabel loopt door tot de lijfomlijning'),
 (34,30):(2,3,'tintvlakje < 3 px (index 2) in de achterlijfschaduw -> 3'),
 (34,31):(2,3,'idem'),
}
im=Image.open(SRC); px=im.load()
for (x,y),(o,n,r) in W.items():
    assert px[x,y]==o,(x,y,px[x,y]); px[x,y]=n
im.save('vlieg_r21.png',transparency=0); shutil.copy('../sprite_r20/normal.pal','normal.pal')
def rgba(p,bg=None):
    pal=p.getpalette(); q=p.load(); o=Image.new('RGBA',p.size,bg or (0,0,0,0)); oo=o.load()
    for y in range(p.height):
        for x in range(p.width):
            if q[x,y]: oo[x,y]=tuple(pal[3*q[x,y]:3*q[x,y]+3])+(255,)
    return o
a=Image.open(SRC); b=Image.open('vlieg_r21.png')
A,B=rgba(a),rgba(b)
Image.alpha_composite(Image.new('RGBA',(64,64),(255,255,255,255)),B).resize((512,512),Image.NEAREST).save('vlieg_r21_8x.png')
sa=a.load(); sb=b.load()
diff=[(x,y) for y in range(64) for x in range(64) if sa[x,y]!=sb[x,y]]
sil=[(x,y) for y in range(64) for x in range(64) if (sa[x,y]==0)!=(sb[x,y]==0)]
print('gewijzigd',len(diff),diff); print('silhouetverschil',sil)
for k,(o,n,r) in W.items(): print(k,o,'->',n,r)
# vel
c=Image.new('RGBA',(512*2+30+300,512+260),(255,255,255,255)); d=ImageDraw.Draw(c)
for i,(im8,t) in enumerate(((A,'r20'),(B,'r21 (keuring)'))):
    c.alpha_composite(im8.resize((512,512),Image.NEAREST),(i*522,20)); d.text((i*522+4,4),t+' 8x',fill=(0,0,0,255))
    for (x,y) in diff:
        X=i*522+x*8; Y=20+y*8; d.rectangle([X-1,Y-1,X+8,Y+8],outline=(255,0,0,255))
ninj=refs.load('ninjask'); volb=refs.load('volbeat')
y0=560
for row,bg in enumerate(((255,255,255,255),(40,40,48,255))):
    Y=y0+row*100; d.rectangle([0,Y-6,c.width,Y+90],fill=bg)
    for k,s in enumerate((A,B,ninj,volb)):
        c.alpha_composite(s,(20+k*90,Y)); c.alpha_composite(s.resize((128,128),Image.NEAREST).resize((64,64)) if False else s,(20+k*90,Y))
d.text((4,y0-20),'1x: r20 | r21 | ninjask | volbeat (licht/donker)',fill=(0,0,0,255))
# 2x refs rechts
c.alpha_composite(ninj.resize((128,128),Image.NEAREST),(1060,40)); c.alpha_composite(volb.resize((128,128),Image.NEAREST),(1060,200))
c.alpha_composite(B.resize((128,128),Image.NEAREST),(1060,360)); d.text((1060,24),'2x: ninjask / volbeat / r21',fill=(0,0,0,255))
c.convert('RGB').save('vel.png')
