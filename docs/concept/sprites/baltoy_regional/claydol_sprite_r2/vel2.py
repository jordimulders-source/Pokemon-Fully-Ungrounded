# vel.png r2: r2 | r1 | model (geschrapt) op 8x; gezicht 12x (r2 | r1 | model); krans-bolletjes 12x (r2 | asset); 1x op licht/donker; varianten schuif 1/2/3 op 4x
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'claydol_sprite_r2'); sys.path.insert(0,'claydol_sprite_r1')
from kaal2 import kaal; from klassen import PAL
P=np.array(PAL,'uint8')
def rgba(S):
    a=np.zeros((64,64,4),'uint8'); a[:,:,:3]=P[S]; a[:,:,3]=np.where(S>0,255,0); return Image.fromarray(a,'RGBA')
def op(im,bg=(255,255,255),s=1):
    c=Image.new('RGBA',im.size,bg+(255,)); c.alpha_composite(im); c=c.convert('RGB'); return c.resize((im.width*s,im.height*s),Image.NEAREST)
r2=rgba(np.load('claydol_sprite_r2/sprite.npy')); r1=Image.open('claydol_sprite_r1/claydol_r1.png'); r1.load(); r1=r1.convert('RGBA')
S,A,NY,NX=kaal(int(sys.argv[1]) if len(sys.argv)>1 else 2); m=np.zeros((64,64,4),'uint8'); m[:,:,:3]=A; m[:,:,3]=np.where(S>0,255,0); model=Image.fromarray(m,'RGBA')
Wd=3*512+4*20; V=Image.new('RGB',(Wd,2000),(236,236,236)); d=ImageDraw.Draw(V)
y=8
for i,(n,im) in enumerate([('r2',r2),('r1',r1),('model r2 (ogen+neus 2 px rechts), geschrapt',model)]):
    d.text((20+i*532,y),n,fill='black'); V.paste(op(im,s=8),(20+i*532,y+14))
y+=14+512+20; box=(8,12,52,34)
for i,(n,im) in enumerate([('gezicht 12x r2',r2),('r1',r1),('model',model)]):
    d.text((20+i*560,y),n,fill='black'); V.paste(op(im.crop(box),s=12),(20+i*560,y+14))
y+=14+22*12+20
d.text((20,y),'krans-bolletjes 12x: r2 linksboven (x2-30,y0-16) | rechts (x36-63,y0-16) | assets stip/streep',fill='black')
V.paste(op(r2.crop((2,0,30,16)),s=12),(20,y+14)); V.paste(op(r2.crop((36,0,63,16)),s=12),(20+28*12+20,y+14))
for i,f in enumerate(['asset_stip','asset_streep']):
    a=np.load('claydol_sprite_r2/%s.npy'%f); Z=np.zeros((64,64),int); Z[:a.shape[0],:a.shape[1]]=a
    V.paste(op(rgba(Z).crop((0,0,a.shape[1],a.shape[0])),s=12),(20+55*12+60+i*(a.shape[1]*12+20),y+14))
y+=14+16*12+20
d.text((20,y),'1x licht/donker',fill='black')
for i,bg in enumerate([(248,248,240),(200,224,248),(40,40,48),(24,64,40)]): V.paste(op(r2,bg),(20+i*74,y+14))
y+=14+64+20
d.text((20,y),'ogen + neus naar rechts: 1 | 2 (gekozen) | 3 natieve px, 4x en 1x',fill='black')
for i,suf in enumerate(['_s1','','_s3']):
    im=rgba(np.load('claydol_sprite_r2/sprite%s.npy'%suf)); V.paste(op(im,s=4),(20+i*(256+90),y+14)); V.paste(op(im),(20+i*(256+90)+262,y+14))
y+=14+256+20
V.crop((0,0,Wd,y)).save('claydol_sprite_r2/vel.png')
op(r2,s=8).save('claydol_sprite_r2/claydol_r2_8x.png')
