# vel.py -> vel.png: schoppen-positie (met middellijn, naast de Kadabra-sprites), ogen (met diff tegen r2), schuine kaart, beste combinatie
import numpy as np, pal
from PIL import Image, ImageDraw
from zij import model, sprite
L=(248,248,240); Dk=(40,40,56); BG=(152,208,160); LIJN=(0,160,255)
R2=pal.load('basis_r2.txt'); BEST=pal.load('raster.txt')
V=Image.new('RGB',(2100,3000),'white'); D=ImageDraw.Draw(V)
KAD='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/kadabra/anim_front_gba.png'; ALA='../../alakazam_regional/af/alakazam_charlatan.png'
def echt(fn,bg):
    q=Image.open(fn).crop((0,0,64,64)); p=q.convert('RGBA'); arr=np.asarray(q)
    if q.mode=='P' and 'transparency' not in q.info: p.putalpha(Image.fromarray(((arr!=arr[0,0])*255).astype('uint8')))
    c=Image.new('RGBA',(64,64),bg+(255,)); c.alpha_composite(p); return c.convert('RGB')
def lijn(im,pts,box,z):
    d=ImageDraw.Draw(im); d.line([((x-box[0])*z,(y-box[1])*z) for x,y in pts],fill=LIJN,width=1); return im
def klein(R,x,y):
    for i,bg in enumerate((L,Dk)):
        V.paste(pal.rgb(R,bg),(x+i*68,y)); V.paste(pal.rgb(R,bg).resize((192,192),0),(x+i*196,y+68))
MID=[(30,14.5),(25.5,21.5),(25,29)]          # middellijn van onze kop: midden tussen de oorbases -> neusrug op ooghoogte -> snuitpunt
# 1. positie
y=4; D.text((8,y),'1. SCHOPPEN OP HET HOOFD: positie. Blauwe lijn = middellijn van de kop (midden oorbases -> neusrug -> snuit). 12x; daaronder 1x en 3x op licht en donker',fill=(0,0,0)); y+=16
z=12; x=8
kb=(12,4,42,30); im=lijn(echt(KAD,BG).crop(kb).resize((30*z,26*z),0),[(29,13.5),(27.5,21.5),(27.5,28)],kb,z)
D.text((x,y),'echte Kadabra (Gen 3)',fill=(0,0,0)); V.paste(im,(x,y+14)); x+=30*z+10
ra=Image.open('../referenties/kadabra_sprite_a.png').convert('RGBA'); bgim=Image.new('RGBA',ra.size,BG+(255,)); bgim.alpha_composite(ra); c=bgim.convert('RGB').crop((110,90,320,300)).resize((312,312),0)
s=312/210; d2=ImageDraw.Draw(c); d2.line([((px*7.5)*s,(py*7.5)*s) for px,py in [(12.5,7.3),(10.8,16.5),(10.6,25)]],fill=LIJN,width=1)
D.text((x,y),'Kadabra, referentie Jordi (a)',fill=(0,0,0)); V.paste(c,(x,y+14)); x+=322
hb=(16,8,42,31)
D.text((x,y),'model',fill=(0,0,0)); V.paste(model(*hb,z,False),(x,y+14)); x+=26*z+10
y+=14+26*z+10; x=8
for nm in ['pos_P1','pos_P2','pos_P3','pos_P4','pos_P5']:
    R=pal.load('var_'+nm+'.txt'); D.text((x,y),nm,fill=(0,0,0)); V.paste(lijn(sprite(R,*hb,z),MID,hb,z),(x,y+14)); klein(R,x,y+14+23*z+4); x+=400
y+=14+23*z+4+68+192+16
# 2. ogen
D.text((8,y),'2. OGEN: r2 | oog_1 (alleen pupil, 4 px) | oog_3 (8 px). Roze = pixels anders dan r2',fill=(0,0,0)); y+=16; ob=(18,16,36,28); x=8
for nm,R in [('r2',R2),('oog_1',pal.load('var_oog_1.txt')),('oog_3',pal.load('var_oog_3.txt'))]:
    D.text((x,y),nm,fill=(0,0,0)); V.paste(sprite(R,*ob,z),(x,y+14))
    df=pal.rgb(R,BG).convert('L').convert('RGB'); px=df.load()
    for yy in range(64):
        for xx in range(64):
            if R[yy][xx]!=R2[yy][xx]: px[xx,yy]=(255,0,200)
    V.paste(df.crop(ob).resize((18*z,12*z),0),(x+18*z+6,y+14)); klein(R,x,y+14+12*z+4); x+=2*18*z+30
y+=14+12*z+4+68+192+16
# 3. kaart
D.text((8,y),'3. KAART, schuin (1 px opzij per 3 rijen, hoek van het model): model | r2 | K1 | K2 | K3',fill=(0,0,0)); y+=16; cb=(0,13,15,34); x=8
D.text((x,y),'model',fill=(0,0,0)); V.paste(model(*cb,z,False),(x,y+14)); x+=15*z+10
for nm,R in [('r2',R2)]+[(n,pal.load('var_kaart_'+n+'.txt')) for n in ('K1','K2','K3')]:
    D.text((x,y),nm,fill=(0,0,0)); V.paste(sprite(R,*cb,z),(x,y+14)); klein(R,x,y+14+21*z+4); x+=400
y+=14+21*z+4+68+192+16
# 4. beste
D.text((8,y),'BESTE COMBINATIE (pos_P1 + oog_1 + kaart_K2), 8x | r2, 8x',fill=(0,0,0)); y+=16
V.paste(pal.rgb(BEST,BG).resize((512,512),0),(8,y)); V.paste(pal.rgb(R2,BG).resize((512,512),0),(530,y)); x0=1060
for r,(bg,lab) in enumerate(((L,'licht'),(Dk,'donker'))):
    yy=y+r*262; D.text((x0,yy),'3x en 1x op '+lab+': echte Kadabra | beste | charlatan-Alakazam',fill=(0,0,0))
    ims=[echt(KAD,bg),pal.rgb(BEST,bg),echt(ALA,bg)]
    for i,im in enumerate(ims): V.paste(im.resize((192,192),0),(x0+i*198,yy+14)); V.paste(im,(x0+600+i*68,yy+14))
V=V.crop((0,0,2100,y+530)); V.save('vel.png'); print(V.size)
