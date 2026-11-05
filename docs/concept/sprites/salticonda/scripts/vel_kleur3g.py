"""Vel 3f vs 3g: 4x en 1x op licht/donker, pre-evolutie, 8x-uitsneden (ringen, onderrand, staart, Electric-glans)."""
from PIL import Image, ImageDraw
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/'
f=Image.open(D+'salticonda/kleur3f/salticonda.png'); g=Image.open(D+'salticonda/kleur3g/salticonda.png'); p=Image.open(D+'silicobra_uyuni/af/silicobra_uyuni.png')
def rgba(im):
    a=im.convert('RGBA'); px=a.load(); src=im.load()
    for y in range(64):
        for x in range(64):
            if src[x,y]==0: px[x,y]=(0,0,0,0)
    return a
F,G,P=rgba(f),rgba(g),rgba(p)
L,Dk=(238,238,232),(36,36,44)
W=1500; H=1240; v=Image.new('RGB',(W,H),(250,250,250)); d=ImageDraw.Draw(v)
def put(im,x,y,s,bg):
    t=Image.new('RGB',(64*s,64*s),bg); t.paste(im.resize((64*s,64*s),Image.NEAREST),(0,0),im.resize((64*s,64*s),Image.NEAREST)); v.paste(t,(x,y))
d.text((10,5),'Salticonda 3f (links) en 3g (rechts), 4x en 1x op licht en donker; pre-evolutie Uyuni-Silicobra 1x/2x',fill=0)
for j,(bg) in enumerate((L,Dk)):
    y=25+j*270
    for i,(im,n) in enumerate(((F,'3f'),(G,'3g'))):
        put(im,10+i*350,y,4,bg); put(im,280+i*350,y,1,bg); d.text((280+i*350,y+70),n,fill=0)
    put(P,720,y,2,bg); put(P,860,y,1,bg); put(G,860,y+80,1,bg)
    d.text((720,y+135),'Uyuni-Silicobra 2x / 1x; 3g 1x',fill=0)
# 8x-uitsneden (3g-coordinaten; 3f 2 px hoger)
C=[('ringen: halsband + ring 2',(10,21,52,39)),('ring 3',(2,44,54,53)),('onderrand',(0,52,40,63)),('staart + zoutkegel',(46,40,64,60)),('Electric-glans halsband',(14,20,36,28))]
y=580; x=10
for n,(x0,y0,x1,y1) in C:
    s=8 if (x1-x0)<=22 else 5
    w=(x1-x0)*s; h=(y1-y0)*s
    if x+2*w+30>W: x=10; y+=hh+40
    d.text((x,y),n+' (%dx; boven 3f, onder 3g)'%s if 0 else n+' (%dx; links 3f, rechts 3g)'%s,fill=0)
    for k,(im,off) in enumerate(((F,2),(G,0))):
        c=im.crop((x0,y0-off,x1,y1-off)).resize((w,h),Image.NEAREST); t=Image.new('RGB',(w,h),L); t.paste(c,(0,0),c); v.paste(t,(x+k*(w+10),y+15))
    hh=h+15; x+=2*w+40
v.save(D+'salticonda/kleur3g/vel.png')
