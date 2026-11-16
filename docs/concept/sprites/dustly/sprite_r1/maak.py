# Schrijft dustly_trouw/A/B/C (64x64, geïndexeerd, index 0 transparant, zelfde indexkaart) + 8x + vel.png + lijn.png
import sys; sys.path.insert(0,'sprite_r1'); import numpy as np; from PIL import Image, ImageDraw; import pal; from render import img
o=np.load('sprite_r1/trouw_idx.npy').astype('uint8')
def save(P,name):
    p=Image.fromarray(o,'P'); fl=[v for c in P for v in c]; p.putpalette(fl+[0]*(768-len(fl))); p.save(f'sprite_r1/{name}.png',transparency=0)
    q=Image.open(f'sprite_r1/{name}.png'); assert (np.asarray(q)==o).all()
    img(o,P,8).save(f'sprite_r1/{name}_8x.png')
for P,n in ((pal.TROUW,'dustly_trouw'),(pal.A,'dustly_A'),(pal.B,'dustly_B'),(pal.C,'dustly_C')): save(P,n)
# vel: model (uitsnede) 8x | trouw 8x | A 8x ; daaronder A op 1x/2x licht en donker
m=Image.open('gemini/r6_a.png').convert('RGB').crop((150,150,880,880)).resize((512,512),Image.LANCZOS)
LICHT,DONKER=(248,248,240),(40,40,48)
cells=[m,img(o,pal.TROUW,8,LICHT),img(o,pal.A,8,LICHT)]
lab=['model r6_a','trouw (modelkleuren)','A (warm, gekozen)']
W=3*512+4*16; out=Image.new('RGB',(W,512+32+16+160),(255,255,255)); d=ImageDraw.Draw(out)
for i,c in enumerate(cells): out.paste(c.convert('RGB'),(16+i*528,24)); d.text((16+i*528,6),lab[i],fill=(0,0,0))
x=16; y=24+512+16
for bgc in (LICHT,DONKER):
    for s in (1,2):
        for P in (pal.TROUW,pal.A):
            c=img(o,P,s,bgc).convert('RGB'); out.paste(c,(x,y)); x+=c.width+8
    x+=24
out.save('sprite_r1/vel.png')
# lijnvel: Hauntflare | Gengas | Dustly A op 4x
H=Image.open('../hauntflare/af/hauntflare.png'); G=Image.open('../gengas/af/gengas.png')
def rgba(im):
    im=im.convert('RGBA'); return im
L=[img(o,pal.A,4,LICHT)]+[None]
row=[img(o,pal.A,4,LICHT)]
for im in (H,G):
    b=Image.new('RGBA',(64,64),LICHT+(255,)); b.alpha_composite(rgba(im)); row.append(b.resize((256,256),Image.NEAREST))
lv=Image.new('RGB',(3*256+4*16,256+40),(255,255,255)); d=ImageDraw.Draw(lv)
for i,(c,n) in enumerate(zip(row,['Dustly (A)','Hauntflare','Gengas'])):
    lv.paste(c.convert('RGB'),(16+i*272,32)); d.text((16+i*272,10),n,fill=(0,0,0))
lv.save('sprite_r1/lijn.png'); print('ok')
