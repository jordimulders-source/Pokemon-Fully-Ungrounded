# vel5.py SPRITE.png UIT.png [VORIGE.png]: als vel.py, close-ups 12x: krater, achterste anemoon L, voorste anemoon VL (sprite | model) + 1x
# close-ups 12x (sprite | model): krater, anemoon voor-links met tentakels, lijf+poten / 1x op licht en donker + model 1x
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
def rgb_from(im,bg=(255,255,255)):
    o=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
sp=Image.open(sys.argv[1]); s=rgb_from(sp)
panelen=[s.resize((512,512),Image.NEAREST)]
if len(sys.argv)>3: panelen.append(rgb_from(Image.open(sys.argv[3])).resize((512,512),Image.NEAREST))
panelen.append(model_op_schaal(8))
zones=[('krater',20,4,44,20),('anemoon L (achter)',2,3,27,27),('anemoon VL (voor)',12,13,38,32)]
z=12; rows=[]
for n,x0,y0,x1,y1 in zones:
    a=s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); b=model_crop(x0,y0,x1,y1,z)
    r=Image.new('RGB',(a.width*2+8,a.height+14),'white'); r.paste(a,(0,14)); r.paste(b,(a.width+8,14))
    d=ImageDraw.Draw(r); d.text((2,1),'%s x%d-%d y%d-%d (sprite | model)'%(n,x0,x1-1,y0,y1-1),fill=(0,0,0))
    for x in range(0,a.width+1,z): d.line([(x,14),(x,14+a.height)],fill=(225,225,225))
    for y in range(0,a.height+1,z): d.line([(0,14+y),(a.width,14+y)],fill=(225,225,225))
    rows.append(r)
W=max(sum(p.width+8 for p in panelen),rows[0].width+rows[1].width+16)
H=512+8+max(rows[0].height,rows[1].height)+8+rows[2].height+8
v=Image.new('RGB',(W,H),'white'); x=0
for p in panelen: v.paste(p,(x,0)); x+=p.width+8
y=520; v.paste(rows[0],(0,y)); v.paste(rows[1],(rows[0].width+16,y)); y+=max(rows[0].height,rows[1].height)+8
v.paste(rows[2],(0,y)); xx=rows[2].width+16
for i,bg in enumerate([(255,255,255),(248,248,232),(40,48,56),(24,24,24)]):
    v.paste(rgb_from(sp,bg),(xx+i*72,y+8))
v.paste(model_op_schaal(1),(xx+4*72,y+8))
v=v.crop((0,0,W,max(y+rows[2].height+8,y+80))); v.save(sys.argv[2]); print(sys.argv[2],v.size)
