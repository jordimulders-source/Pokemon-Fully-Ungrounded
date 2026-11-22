# vel.py SPRITE.png UIT.png [VORIGE/KAAL.png] [kopregel]: sprite 8x | kaal 8x | model op dezelfde schaal 8x (natief raster, zelfde rijen/kolommen geschrapt)
# / close-ups 12x (sprite | model op schaal): kop+bek+oog, opgeheven poot, manen, poten / 1x op wit, licht, donker naast Mightyena 1x
import sys; sys.path.insert(0,'gereedschap')
from PIL import Image, ImageDraw; import numpy as np; from gemeen import *; from schrap import schrap
def rgbp(im,bg=(255,255,255)):
    o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
def model_op_schaal():
    a,c,L=klassen(); s,r,k,_,_=schrap(c)
    A=np.delete(np.delete(a,r,0),k,1); img=np.full((64,64,3),255,'uint8'); H,W=s.shape
    blk=A.astype('uint8'); blk[s==0]=255; img[Y0:Y0+H,X0:X0+W]=blk
    return Image.fromarray(img)
sp=Image.open(sys.argv[1]); s=rgbp(sp); m=model_op_schaal()
pan=[s]+([rgbp(Image.open(sys.argv[3]))] if len(sys.argv)>3 else [])+[m]
zones=[('kop, bek, oog',0,2,24,31),('opgeheven poot',3,26,22,48),('manen',18,6,56,32),('poten',20,40,62,64)]
z=12; rows=[]
for n,x0,y0,x1,y1 in zones:
    A=s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); B=m.crop((x0,y0,x1,y1)).resize(A.size,Image.NEAREST)
    r=Image.new('RGB',(A.width*2+8,A.height+16),'white'); r.paste(A,(0,16)); r.paste(B,(A.width+8,16))
    d=ImageDraw.Draw(r); d.text((2,2),n+' (sprite | model op schaal)',fill=(0,0,0))
    for off in (0,A.width+8):
        for x in range(0,A.width+1,z): d.line([(off+x,16),(off+x,16+A.height)],fill=(225,225,225))
        for y in range(0,A.height+1,z): d.line([(off,16+y),(off+A.width,16+y)],fill=(225,225,225))
    rows.append(r)
my=Image.open('../../../../graphics/pokemon/mightyena/anim_front_gba.png')
W=max(len(pan)*520,rows[0].width+rows[1].width+16,rows[2].width+rows[3].width+16)
H=530+max(rows[0].height,rows[1].height)+8+max(rows[2].height,rows[3].height)+8+90
v=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(v)
for i,p in enumerate(pan): v.paste(p.resize((512,512),Image.NEAREST),(i*520,14))
lbl=sys.argv[4] if len(sys.argv)>4 else 'sprite 8x | kaal 8x | model op dezelfde schaal 8x'
d.text((2,0),lbl,fill=(0,0,0))
y=532
for pr in (rows[0:2],rows[2:4]):
    x=0
    for r in pr: v.paste(r,(x,y)); x+=r.width+16
    y+=max(r.height for r in pr)+8
for i,bg in enumerate([(255,255,255),(232,232,216),(40,48,56)]):
    v.paste(rgbp(sp,bg),(i*140,y+8)); v.paste(rgbp(my,bg),(i*140+68,y+8))
v.paste(m,(3*140,y+8)); d.text((2,y+76),'1x: sprite | Mightyena op wit, licht, donker; model op schaal',fill=(0,0,0))
v.save(sys.argv[2]); print(sys.argv[2],v.size)
