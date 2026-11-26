# Vel: rij 1 = model (verkleind tot 4x-spritemaat) | 0 | A | B | C op 4x; rij 2 = poncho-uitsnede 8x van 0/A/B/C;
# rij 3 = 1x en 2x op licht en donker: Lotad, Lombre, Ludicolo 0/A/B/C.
import numpy as np; from PIL import Image, ImageDraw
from gemeen import rgb
W=(255,255,255); DK=(40,44,52)
def png(p,bg):
    im=Image.open(p)
    a=np.array(im); pal=np.array(im.getpalette()[:48]).reshape(16,3)
    r=pal[a].astype('uint8'); r[a==0]=bg; return Image.fromarray(r)
V=['0','A','B','C']; S=4
model=Image.open('../../r6/gemini_r6.png').convert('RGB').resize((64*S,64*S),Image.LANCZOS)
rij1=[model]+[png('ludicolo_gaucho_%s.png'%v,W).resize((64*S,64*S),Image.NEAREST) for v in V]
rij2=[png('ludicolo_gaucho_%s.png'%v,W).crop((6,26,50,58)).resize((44*8//1,32*8),Image.NEAREST) for v in V]
LOT='../../../af/lotad_gaucho.png'; LOM='../../../lombre/af/lombre_gaucho.png'
fam=[LOT,LOM]+['ludicolo_gaucho_%s.png'%v for v in V]
H=64*S+24+32*8+24+64*2*2+40
c=Image.new('RGB',(max(5*64*S+4*8,4*(44*8+8)),H),'white'); d=ImageDraw.Draw(c)
x=0
for t,im in zip(['model r6','0','A','B','C'],rij1): c.paste(im,(x,16)); d.text((x+4,2),t,fill=(0,0,0)); x+=64*S+8
y=16+64*S+8; x=0
for t,im in zip(V,rij2): c.paste(im,(x,y+14)); d.text((x+4,y),'poncho '+t+' (8x)',fill=(0,0,0)); x+=im.width+8
y+=14+32*8+12; x=0
d.text((0,y),'1x en 2x op licht en donker: Lotad, Lombre, Ludicolo 0 A B C',fill=(0,0,0)); y+=14
for bg in (W,DK):
    xx=0
    for p in fam:
        im=png(p,bg); c.paste(im,(xx,y)); c.paste(im.resize((128,128),Image.NEAREST),(xx+66,y)); xx+=200
    y+=132
c=c.crop((0,0,c.width,y)); c.save('vel.png'); print(c.size)
