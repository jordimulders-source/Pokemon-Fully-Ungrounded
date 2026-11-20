# vel.py SPRITE.png UIT.png [VORIGE.png]: sprite 8x | (vorige 8x) | model op schaal 8x / close-ups 12x (sprite | model) / 1x licht+donker
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
def laad(p):
    im=Image.open(p); im.save('/tmp/_v.png',transparency=0) if False else None
    o=np.asarray(im); return rgb_from(im)
def rgb_from(im,bg=(255,255,255)):
    o=np.asarray(im); pal=np.array(im.getpalette()[:48*3]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
sp=Image.open(sys.argv[1]); s=rgb_from(sp)
m=model_op_schaal()
# model in hoge resolutie op dezelfde uitsnede (voor close-ups)
M=Image.open(MODEL).convert('RGB'); k=10.24/S
ox=10.25+10.24*(U0-PHX)-X0*k; oy=10.25+10.24*(V0-PHY)-Y0*k
def mcrop(x0,y0,x1,y1,z):
    return M.crop((int(ox+x0*k),int(oy+y0*k),int(ox+x1*k),int(oy+y1*k))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
panelen=[s.resize((512,512),Image.NEAREST)]
if len(sys.argv)>3: panelen.append(rgb_from(Image.open(sys.argv[3])).resize((512,512),Image.NEAREST))
panelen.append(m.resize((512,512),Image.NEAREST))
W=sum(p.width+8 for p in panelen)
zones=[('kop',23,26,42,42),('kelp',21,13,55,32),('voeten',20,40,44,50)]
z=12; rows=[]
for n,x0,y0,x1,y1 in zones:
    a=s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); b=mcrop(x0,y0,x1,y1,z)
    r=Image.new('RGB',(a.width*2+8,a.height),'white'); r.paste(a,(0,0)); r.paste(b,(a.width+8,0))
    d=ImageDraw.Draw(r)
    for x in range(0,a.width,z): d.line([(x,0),(x,a.height)],fill=(225,225,225))
    for y in range(0,a.height,z): d.line([(0,y),(a.width,y)],fill=(225,225,225))
    rows.append(r)
W=max(W,max(r.width for r in rows),400)
H=512+8+sum(r.height+8 for r in rows)+80
v=Image.new('RGB',(W,H),'white'); x=0
for p in panelen: v.paste(p,(x,0)); x+=p.width+8
y=520
for r in rows: v.paste(r,(0,y)); y+=r.height+8
for i,bg in enumerate([(255,255,255),(248,248,232),(40,48,56),(24,24,24)]):
    v.paste(rgb_from(sp,bg),(i*72,y+8))
v.paste(m,(4*72,y+8))
v.save(sys.argv[2]); print(sys.argv[2],v.size)
