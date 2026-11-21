# vel.png: sprite 8x | model op dezelfde schaal (8x van 0,75 natief) ; close-up kop 12x naast Pa'u ; kleurstrip ; 1x licht/donker
import numpy as np, json; from PIL import Image, ImageDraw
from palet import pal, VARIANT
o=np.load('cumbia_kls.npy').astype('uint8')
def rgba(p):
    a=np.zeros((64,64,4),'uint8')
    for i,c in enumerate(p):
        if i: a[o==i,:3]=c; a[o==i,3]=255
    return Image.fromarray(a)
def op(im,bg,z):
    b=Image.new('RGB',(im.width*z,im.height*z),bg); r=im.resize(b.size,Image.NEAREST); b.paste(r,(0,0),r); return b
spr=rgba(pal('B_midden'))
# model op dezelfde schaal: natief (100x100) * 0.75 * 8 = 6 px per natieve pixel, uitlijnen via plaatsing
# model op dezelfde schaal: natieve bbox geschaald naar de sprite-bbox (8x)
na=np.asarray(Image.open('natief.png').convert('RGB')); bgm=na.min(2)>=225; yy,xx=np.where(~bgm)
nb=Image.fromarray(na).crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1))
sy,sx=np.where(o>0)
m=nb.resize(((sx.max()-sx.min()+1)*8,(sy.max()-sy.min()+1)*8),Image.NEAREST)
mod=Image.new('RGB',(512,512),'white'); mod.paste(m,(sx.min()*8,sy.min()*8))
W=Image.new('RGB',(512*2+30+ 64*12*0+20, 512+40+420+40+200),(230,230,230)); d=ImageDraw.Draw(W)
W.paste(op(spr,(255,255,255),8),(0,30)); d.text((4,4),'cumbia r1 (8x, kleur B_midden)',fill='black')
W.paste(mod,(530,30)); d.text((534,4),'model gemini_r2, zelfde schaal',fill='black')
# close-up kop 12x: sprite rij 2..24, kol 14..42 ; Pa'u kop
y=560; d.text((4,y-18),'kop 12x  |  Pa\'u (Gen 3, bron oog) 12x  |  model kop',fill='black')
kop=op(spr.crop((14,2,42,24)),(255,255,255),12); W.paste(kop,(0,y))
pau=Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/oricorio/pau/anim_front.png').convert('RGBA').crop((18,8,46,30))
W.paste(op(pau,(255,255,255),12),(350,y))
mk=Image.open('../model/gemini_r2.png').convert('RGB').crop((260,110,640,410)).resize((340,268))
W.paste(mk,(700,y))
# kleurstrip + 1x
y2=y+290; d.text((4,y2-18),'kleurvarianten blauw (A licht / B midden = cumbia.png / C donker / modelkleur) op 2x en 1x licht/donker',fill='black')
x=0
for v in list(VARIANT)+['model']:
    s=rgba(pal(v)); W.paste(op(s,(255,255,255),2),(x,y2)); d.text((x+2,y2+130),v,fill='black')
    W.paste(op(s,(255,255,255),1),(x+130,y2)); W.paste(op(s,(40,40,48),1),(x+130,y2+66))
    p=pal(v)
    for k,i in enumerate(range(2,10)): d.rectangle([x+k*24,y2+146,x+k*24+22,y2+168],fill=p[i])
    x+=260
W.save('vel.png'); print(W.size)
