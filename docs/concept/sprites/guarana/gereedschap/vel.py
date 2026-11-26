# vel.py SPRITE.png UIT.png [VORIGE.png]: sprite 8x | (vorige/kaal 8x) | model op schaal 8x / close-ups 12x (sprite | model) / 1x wit, licht, donker, zwart + model 1x
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
def rgb_from(im,bg=(255,255,255)):
    o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
sp=Image.open(sys.argv[1]); s=rgb_from(sp); m=model_op_schaal()
M=Image.open(MODEL).convert('RGB')
def mcrop(x0,y0,x1,y1,z):
    u0=(x0-X0)/S+U0; u1=(x1-X0)/S+U0; v0=(y0-Y0)/S+V0; v1=(y1-Y0)/S+V0
    f=lambda u,ph:ph+0.5+P*u
    return M.crop((int(f(u0,FX)),int(f(v0,FY)),int(f(u1,FX)),int(f(v1,FY)))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
panelen=[s.resize((512,512),Image.NEAREST)]
if len(sys.argv)>3: panelen.append(rgb_from(Image.open(sys.argv[3])).resize((512,512),Image.NEAREST))
panelen.append(m.resize((512,512),Image.NEAREST))
zones=[('vruchttros+ogen',8,13,33,38),('rank+blad',26,23,56,49),('ranken links',9,40,30,53),('ranken rechts',30,40,56,53)]
z=12; rows=[]
for n,x0,y0,x1,y1 in zones:
    a=s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); b=mcrop(x0,y0,x1,y1,z)
    r=Image.new('RGB',(a.width*2+8,a.height),'white'); r.paste(a,(0,0)); r.paste(b,(a.width+8,0))
    d=ImageDraw.Draw(r)
    for x in range(0,a.width,z): d.line([(x,0),(x,a.height)],fill=(225,225,225))
    for y in range(0,a.height,z): d.line([(0,y),(a.width,y)],fill=(225,225,225))
    rows.append(r)
W=max(sum(p.width+8 for p in panelen),max(r.width for r in rows))
H=520+sum(r.height+8 for r in rows)+80
v=Image.new('RGB',(W,H),'white'); x=0
for p in panelen: v.paste(p,(x,0)); x+=p.width+8
y=520
for r in rows: v.paste(r,(0,y)); y+=r.height+8
for i,bg in enumerate([(255,255,255),(248,248,232),(40,48,56),(24,24,24)]):
    v.paste(rgb_from(sp,bg),(i*72,y+8))
v.paste(m,(4*72,y+8))
v.save(sys.argv[2]); print(sys.argv[2],v.size)
