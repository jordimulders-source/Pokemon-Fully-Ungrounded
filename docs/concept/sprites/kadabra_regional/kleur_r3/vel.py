# vel.py -> vel.png: per onderdeel model | r2 | varianten op 12x, elk ook 1x en 3x op licht en donker; onderaan de beste combinatie naast r2, de echte Kadabra en de charlatan-Alakazam
import numpy as np, pal
from PIL import Image, ImageDraw
from zij import model, sprite
L=(248,248,240); Dk=(40,40,56); BG=(152,208,160)
R2=pal.load('basis_r2.txt'); BEST=pal.load('raster.txt')
V=Image.new('RGB',(1840,2600),'white'); D=ImageDraw.Draw(V)
def blok(y,titel,box,namen,z=12):
    D.text((8,y),titel,fill=(0,0,0)); y+=16; w=(box[2]-box[0])*z; h=(box[3]-box[1])*z; x=8
    D.text((x,y),'model',fill=(0,0,0)); V.paste(model(*box,z,False),(x,y+14)); x+=w+10
    for nm,fn in [('r2','basis_r2.txt')]+[(n,'var_'+n+'.txt') for n in namen]:
        R=pal.load(fn); D.text((x,y),nm,fill=(0,0,0)); V.paste(sprite(R,*box,z),(x,y+14)); yy=y+14+h+4
        for i,bg in enumerate((L,Dk)):
            V.paste(pal.rgb(R,bg),(x+i*68,yy)); V.paste(pal.rgb(R,bg).resize((192,192),0),(x+i*196,yy+68))
        x+=max(w,392)+14
    return y+14+h+4+68+192+16
y=blok(4,'1. VOORHOOFD: rode schoppen (12x; daaronder 1x en 3x op licht en donker)',(19,13,34,26),['schoppen_1','schoppen_2','schoppen_3'])
y=blok(y,'2. OGEN: pupillen',(19,17,36,27),['oog_1','oog_2','oog_3'])
y=blok(y,'3. KAART met kaarthand',(0,13,14,34),['kaart_A','kaart_B','kaart_C'])
def echt(fn,bg):
    q=Image.open(fn).crop((0,0,64,64)); p=q.convert('RGBA'); arr=np.asarray(q)
    if q.mode=='P' and 'transparency' not in q.info: p.putalpha(Image.fromarray(((arr!=arr[0,0])*255).astype('uint8')))
    c=Image.new('RGBA',(64,64),bg+(255,)); c.alpha_composite(p); return c.convert('RGB')
KAD='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/kadabra/anim_front_gba.png'; ALA='../../alakazam_regional/af/alakazam_charlatan.png'
D.text((8,y),'BESTE COMBINATIE (schoppen_3 + oog_3 + kaart_B), 8x | r2, 8x',fill=(0,0,0)); y+=16
V.paste(pal.rgb(BEST,BG).resize((512,512),0),(8,y)); V.paste(pal.rgb(R2,BG).resize((512,512),0),(530,y))
x0=1060
for r,(bg,lab) in enumerate(((L,'licht'),(Dk,'donker'))):
    yy=y+r*262; D.text((x0,yy),'3x en 1x op '+lab+': beste | r2',fill=(0,0,0))
    V.paste(pal.rgb(BEST,bg).resize((192,192),0),(x0,yy+14)); V.paste(pal.rgb(R2,bg).resize((192,192),0),(x0+200,yy+14))
    V.paste(pal.rgb(BEST,bg),(x0+410,yy+14)); V.paste(pal.rgb(R2,bg),(x0+480,yy+14))
y+=530
for r,(bg,lab) in enumerate(((L,'licht'),(Dk,'donker'))):
    D.text((8+r*850,y),'1x en 3x op '+lab+': echte Kadabra | r2 | beste | charlatan-Alakazam',fill=(0,0,0))
    ims=[echt(KAD,bg),pal.rgb(R2,bg),pal.rgb(BEST,bg),echt(ALA,bg)]; x=8+r*850
    for im in ims: V.paste(im,(x,y+16)); x+=66
    x=8+r*850
    for im in ims: V.paste(im.resize((192,192),0),(x,y+86)); x+=198
V=V.crop((0,0,1840,y+290)); V.save('vel.png'); print(V.size)
