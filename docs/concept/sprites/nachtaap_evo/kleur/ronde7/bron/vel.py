# maakt ../vel.png: ronde 5 | 6 | 7 op 4x en 1x (licht/donker), rug op 6x naast de onderlaag
import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(H,'../../../')
def ld(p):
    im=Image.open(p); idx=im.load(); a=im.convert('RGBA'); px=a.load()
    for y in range(64):
        for x in range(64):
            if idx[x,y]==0: px[x,y]=(0,0,0,0)
    return a
R=[(n,ld(os.path.join(H,f'../../{n}/nachtaap.png'))) for n in ('ronde5','ronde6','ronde7')]
ond=Image.open(os.path.join(D,'silhouet/onderlaag_256.png')).convert('RGBA')
L=(236,236,230,255); DK=(40,40,48,255)
o=Image.new('RGBA',(1100,560),L); d=ImageDraw.Draw(o)
def put(im,x,y,bg,lab=None,s=1):
    im=im.resize((im.width*s,im.height*s),Image.NEAREST); b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); o.paste(b,(x,y))
    if lab: d.text((x,y+im.height+2),lab,fill=(30,30,30,255))
for i,(n,r) in enumerate(R): put(r,i*266,0,L,n+', 4x',4)
put(R[2][1],800,0,DK,'ronde7 op donker',4) if False else None
x=800
for n,r in R: put(r,x,0,L,n[-1]); put(r,x,80,DK); x+=76
put(R[2][1],800,170,DK,'ronde 7, 1x op donker',1)
put(R[2][1].crop((12,22,52,44)),0,280,L,'rug ronde 6, 6x',6) if False else None
put(R[1][1].crop((12,22,52,44)),0,280,L,'rug ronde 6, 6x',6)
put(R[2][1].crop((12,22,52,44)),250,280,L,'rug ronde 7, 6x',6)
put(ond.crop((48,88,208,176)).resize((240,132)),500,280,(255,255,255,255),'onderlaag (poppetje), zelfde plek')
put(R[2][1],760,280,L,'ronde 7, 3x',3)
put(R[2][1],760,280+200,DK,None,1)
o.save(os.path.join(H,'../vel.png'))
