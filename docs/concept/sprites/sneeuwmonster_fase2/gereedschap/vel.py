# vel.py SPRITE.png UIT.png [VORIGE.png]: sprite 8x | (vorige 8x) | model op dezelfde schaal 8x
#   / close-ups 12x (sprite | model): gezicht, stenen, emmer / 1x op licht en donker + model 1x
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
def rgb_from(im,bg=(255,255,255)):
    o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
sp=Image.open(sys.argv[1]); s=rgb_from(sp); M=Image.open(MODEL).convert('RGB')
def mcrop(x0,y0,x1,y1,size):
    a0,b0=s2m(x0,y0); a1,b1=s2m(x1,y1)
    c=Image.new('RGB',(int(a1-a0),int(b1-b0)),'white'); c.paste(M,(-int(a0),-int(b0)))
    return c.resize(size,Image.LANCZOS)
panelen=[s.resize((512,512),Image.NEAREST)]
if len(sys.argv)>3: panelen.append(rgb_from(Image.open(sys.argv[3])).resize((512,512),Image.NEAREST))
panelen.append(mcrop(0,0,64,64,(512,512)))
zones=[('gezicht',14,15,40,29),('stenen',14,32,30,51),('emmer',20,1,46,19)]
z=12; rows=[]
for n,x0,y0,x1,y1 in zones:
    a=s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); b=mcrop(x0,y0,x1,y1,a.size)
    r=Image.new('RGB',(a.width*2+8,a.height),'white'); r.paste(a,(0,0)); r.paste(b,(a.width+8,0))
    d=ImageDraw.Draw(r)
    for x in range(0,a.width,z): d.line([(x,0),(x,a.height)],fill=(225,225,225))
    for y in range(0,a.height,z): d.line([(0,y),(a.width,y)],fill=(225,225,225))
    rows.append(r)
W=max(sum(p.width+8 for p in panelen),sum(r.width+16 for r in rows[:2]),rows[2].width)
H=520+max(rows[0].height,rows[1].height)+8+rows[2].height+8+80
v=Image.new('RGB',(W,H),'white'); x=0
for p in panelen: v.paste(p,(x,0)); x+=p.width+8
y=520; v.paste(rows[0],(0,y)); v.paste(rows[1],(rows[0].width+16,y)); y+=max(rows[0].height,rows[1].height)+8
v.paste(rows[2],(0,y)); y+=rows[2].height+8
for i,bg in enumerate([(255,255,255),(248,248,232),(40,48,56),(24,24,24)]): v.paste(rgb_from(sp,bg),(i*72,y+8))
v.paste(mcrop(0,0,64,64,(64,64)),(4*72,y+8))
v.save(sys.argv[2]); print(sys.argv[2],v.size)
