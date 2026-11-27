# vel.py r11: python3 sprite_r11/vel.py (vanuit starmie/)
# rij 1 (8x): r11 | r10 (wijzigingen blauw omkaderd)
# rij 2 (16x): zone 1 r10 | r11 | r11_B | achterpunt linksboven ; zone 2 r10 | r11 | r11_B | linker voorarm gespiegeld ; rij 3: 2x/1x wit en donker
# rij 3: 2x en 1x op wit en donker: r10, r10_B, r9
import numpy as np; from PIL import Image, ImageDraw, ImageOps
def rgb(im,bg):
    o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3); img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
r10=Image.open('sprite_r11/starmie_r11.png'); r10b=Image.open('sprite_r11/starmie_r11_B.png'); r9=Image.open('sprite_r10/starmie_r10.png')
diff=np.asarray(r10)!=np.asarray(r9)
WIT=(255,255,255); DONK=(40,48,56)
Z1=(35,8,48,22); Z2=(43,19,58,29); V1=(11,7,26,21); V2=(2,19,17,29)
W=1100; H=2400
v=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(v)
for i,(im,n) in enumerate([(r10,'r11'),(r9,'r10')]):
    v.paste(rgb(im,WIT).resize((512,512),Image.NEAREST),(i*540,14)); d.text((i*540,0),n+' 8x (blauw = gewijzigd r10->r11)',fill=(0,0,0))
    for y,x in zip(*np.where(diff)): d.rectangle((i*540+x*8,14+y*8,i*540+x*8+7,14+y*8+7),outline=(0,90,255))
y0=14+512+30; x=0
def blok(im,box,n,flip=False):
    global x
    c=rgb(im,WIT).crop(box)
    if flip: c=ImageOps.mirror(c)
    c=c.resize(((box[2]-box[0])*16,(box[3]-box[1])*16),Image.NEAREST)
    v.paste(c,(x,y0+14)); d.text((x,y0),n,fill=(0,0,0)); x+=c.size[0]+8
for im,n in [(r9,'zone1 r10'),(r10,'zone1 r11'),(r10b,'zone1 r11_B')]: blok(im,Z1,n)
blok(r10,V1,'vgl: achterpunt LB')
y0b=y0+16*14+20
yy=y0+14+(Z1[3]-Z1[1])*16+20; x=0
def blok2(im,box,n,flip=False):
    global x
    c=rgb(im,WIT).crop(box)
    if flip: c=ImageOps.mirror(c)
    c=c.resize(((box[2]-box[0])*16,(box[3]-box[1])*16),Image.NEAREST)
    v.paste(c,(x,yy+14)); d.text((x,yy),n,fill=(0,0,0)); x+=c.size[0]+8
H2=yy+14+10*16+20
v=v.crop((0,0,W,H)) if False else v
for im,n in [(r9,'zone2 r10'),(r10,'zone2 r11'),(r10b,'zone2 r11_B')]: blok2(im,Z2,n)
blok2(r10,V2,'vgl: linker voorarm gespiegeld',flip=True)
y=yy+14+(Z2[3]-Z2[1])*16+20
for bg in (WIT,DONK):
    ims=[rgb(r10,bg),rgb(r10b,bg),rgb(r9,bg)]
    for i,im in enumerate(ims): v.paste(Image.new('RGB',(136,140),bg),(i*136,y)); v.paste(im.resize((128,128),Image.NEAREST),(i*136+4,y+6))
    y+=140
    for i,im in enumerate(ims): v.paste(Image.new('RGB',(136,70),bg),(i*136,y)); v.paste(im,(i*136+36,y+2))
    y+=70
d.text((0,y+4),'2x en 1x op wit / donker: r11 | r11_B | r10',fill=(0,0,0))
v=v.crop((0,0,W,y+20)); v.save('sprite_r11/vel.png'); print(v.size)
