# Sunflora-methode: kop van het model knippen (polygoon), vergroten, terugplakken over het lijf (overlap mag, Jordi 23 nov).
from PIL import Image, ImageDraw
import sys
D='docs/concept/sprites/emolga_evo/'
# polygonen in volle 1024-coördinaten (crop-offset 150,500)
P={'r6b':[(45,60),(100,90),(140,190),(185,140),(215,60),(250,50),(255,140),(235,200),(255,260),(250,330),(205,392),(95,392),(65,330),(75,250),(55,150)],
   'r6c':[(45,40),(110,50),(130,150),(190,140),(240,60),(300,50),(300,170),(270,230),(300,290),(280,370),(230,395),(80,395),(55,330),(55,240),(40,130)]}
def maak(bron,kopbron,schaal,anker=(330,880)):
    body=Image.open(D+'gemini/'+bron+'.png').convert('RGB')
    kop=Image.open(D+'gemini/'+kopbron+'.png').convert('RGB')
    m=Image.new('L',kop.size,0); ImageDraw.Draw(m).polygon([(x+150,y+500) for x,y in P[kopbron]],fill=255)
    # alleen niet-wit binnen polygoon
    # achtergrond = wit verbonden met de rand (flood fill), niet het witte gezicht
    f=kop.convert('L').point(lambda p:255 if p>=235 else 0).convert('RGB')
    ImageDraw.floodfill(f,(0,0),(255,0,0))
    w=Image.eval(f.split()[1],lambda p:255)  # placeholder
    r,g,_=f.split()
    w=Image.merge('RGB',f.split()).point(lambda p:p)
    w=Image.eval(Image.fromarray(__import__('numpy').array(f)[:,:,1]),lambda p:p)  # groen 0 = rode achtergrond of zwart
    import numpy as np
    A=np.array(f); bg=(A[:,:,0]==255)&(A[:,:,1]==0)
    w=Image.fromarray(((~bg)*255).astype('uint8'))
    from PIL import ImageChops
    m=ImageChops.multiply(m,w)
    bb=m.getbbox(); kc=kop.crop(bb); mc=m.crop(bb)
    nw,nh=round(kc.width*schaal),round(kc.height*schaal)
    kc=kc.resize((nw,nh),Image.NEAREST); mc=mc.resize((nw,nh),Image.NEAREST)
    # anker: onderkant-midden van de kop blijft op dezelfde plek (kin), naar links/onder mag uitsteken
    cx=(bb[0]+bb[2])//2; x=cx-nw//2; y=bb[3]-nh
    out=Image.new('RGB',(1300,1150),'white'); off=(150,100)
    out.paste(body,off); out.paste(kc,(x+off[0],y+off[1]),mc)
    g=Image.eval(out.convert('L'),lambda p:255 if p<235 else 0); out=out.crop(g.getbbox())
    return out
opts=[('A_r6b_kop_1.4',maak('r6b','r6b',1.4)),('B_r6c_kop_1.15',maak('r6b','r6c',1.15))]
for n,o in opts: o.save(D+f'model/kop_opties/{n}.png')
H=max(o.height for _,o in opts); W=sum(o.width for _,o in opts)+60
v=Image.new('RGB',(W,H),'white'); x=0
for n,o in opts: v.paste(o,(x,0)); x+=o.width+60
v.save(D+'model/kop_opties/vel.png')
# 64px-proef
for n,o in opts:
    s=64/max(o.size); sm=o.resize((round(o.width*s),round(o.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(64,64),'white'); c.paste(sm,((64-sm.width)//2,(64-sm.height)//2)); c.resize((512,512),Image.NEAREST).save(D+f'model/kop_opties/{n}_64px_8x.png')
