# maakt ../vel.png: ronde 7 | ronde 8 | variant B op 4x en 1x (licht/donker), rug op 6x naast het poppetje
import os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(H,'../../../')
def ld(p):
    im=Image.open(p); idx=im.load(); a=im.convert('RGBA'); px=a.load()
    for y in range(64):
        for x in range(64):
            if idx[x,y]==0: px[x,y]=(0,0,0,0)
    return a
R=[('ronde 7',ld(os.path.join(H,'../../ronde7/nachtaap.png'))),('ronde 8',ld(os.path.join(H,'../nachtaap.png'))),('variant B',ld(os.path.join(H,'../variant_eigen_kleur/nachtaap.png')))]
pop=Image.open(os.path.join(D,'pop3d/poppetje_goedgekeurd_256.png')).convert('RGBA')
L=(236,236,230,255); DK=(40,40,48,255)
o=Image.new('RGBA',(1120,620),L); d=ImageDraw.Draw(o)
def put(im,x,y,bg,lab=None,s=1):
    im=im.resize((im.width*s,im.height*s),Image.NEAREST); b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); o.paste(b,(x,y))
    if lab: d.text((x,y+im.height+2),lab,fill=(30,30,30,255))
for i,(n,r) in enumerate(R): put(r,i*266,0,L,n+', 4x',4)
x=800
for n,r in R: put(r,x,0,L,n); put(r,x,90,DK); x+=100
for i,(n,r) in enumerate(R): put(r.crop((12,22,52,50)),i*250,280,L,'rug '+n+', 6x',6)
put(pop.crop((48,88,208,200)).resize((240,168)),750,280,(255,255,255,255),'poppetje (goedgekeurd), zelfde plek')
put(R[1][1],800,180,L,None,1); put(R[2][1],880,180,L,None,1)
o.save(os.path.join(H,'../vel.png'))
