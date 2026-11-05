# maakt ../vel.png: ronde 9 | ronde 10 | Espurr, kop op 8x, sprite op 1x en 3x (licht/donker)
import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'../../../../../../../')
def ld(p,pal=None):
    im=Image.open(p).crop((0,0,64,64))
    if pal:
        q=[tuple(int(v) for v in l.split()) for l in open(pal).read().split('\n')[3:19] if l.strip()]; im.putpalette([c for t in q for c in t])
    idx=im.load(); a=im.convert('RGBA'); px=a.load()
    for y in range(64):
        for x in range(64):
            if idx[x,y]==0: px[x,y]=(0,0,0,0)
    return a
r9=ld(os.path.join(H,'../../ronde9/nachtaap.png')); r10=ld(os.path.join(H,'../nachtaap.png'))
es=ld(os.path.join(R,'graphics/pokemon/espurr/anim_front.png'),os.path.join(R,'graphics/pokemon/espurr/normal.pal'))
L=(236,236,230,255); DK=(40,40,48,255)
o=Image.new('RGBA',(1000,560),L); d=ImageDraw.Draw(o)
def put(im,x,y,bg,lab=None,s=1):
    im=im.resize((im.width*s,im.height*s),Image.NEAREST); b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); o.paste(b,(x,y))
    if lab: d.text((x,y+im.height+2),lab,fill=(30,30,30,255))
put(r9.crop((2,36,26,56)),0,0,L,'kop ronde 9, 8x',8); put(r10.crop((2,36,26,56)),210,0,L,'kop ronde 10, 8x',8); put(es.crop((18,20,42,40)),420,0,L,'Espurr (Gen 3-stijl), 8x',8)
put(r10.crop((5,42,22,50)),640,0,L,'ogen ronde 10, 8x',8); put(r9.crop((5,42,22,50)),640,90,L,'ogen ronde 9, 8x',8)
x=0
for n,im in (('ronde 9',r9),('ronde 10',r10),('Espurr',es)):
    put(im,x,200,L,n+' 1x'); put(im,x,280,DK); x+=80
put(r9,260,200,L,'ronde 9, 3x',3); put(r10,460,200,L,'ronde 10, 3x',3); put(r10,660,200,DK,'ronde 10, 3x donker',3)
o.save(os.path.join(H,'../vel.png'))
