# vel.py SPRITE.png UIT.png [VORIGE.png]: sprite 8x | (vorige 8x) | model op schaal 8x / close-ups 12x (sprite | model) / 1x licht+donker + model 1x
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap_r4'); from gemeen import *
def rgb_from(im,bg=(255,255,255)):
    o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
sp=Image.open(sys.argv[1]); s=rgb_from(sp); m=model_op_schaal()
M=Image.open(MODEL).convert('RGB')
# natief->1024: celmidden u -> 9.25+0.5+10.24*(u+0.5)
def mcrop(x0,y0,x1,y1,z):
    u0=(x0-X0)/S+U0; u1=(x1-X0)/S+U0; v0=(y0-Y0)/S+V0; v1=(y1-Y0)/S+V0
    f=lambda u,ph:ph+0.5+10.24*u
    return M.crop((int(f(u0,FX)),int(f(v0,FY)),int(f(u1,FX)),int(f(v1,FY)))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
panelen=[s.resize((512,512),Image.NEAREST)]
if len(sys.argv)>3: panelen.append(rgb_from(Image.open(sys.argv[3])).resize((512,512),Image.NEAREST))
panelen.append(m.resize((512,512),Image.NEAREST))
zones=[('bovenarm',20,10,38,28),('juweel',22,26,36,38),('linkerarm',8,22,28,40),('rechterarm',32,22,52,40),('benen',14,36,46,56)]
z=12; rows=[]
for n,x0,y0,x1,y1 in zones:
    a=s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); b=mcrop(x0,y0,x1,y1,z)
    r=Image.new('RGB',(a.width*2+8,a.height),'white'); r.paste(a,(0,0)); r.paste(b,(a.width+8,0))
    d=ImageDraw.Draw(r)
    for x in range(0,a.width,z): d.line([(x,0),(x,a.height)],fill=(225,225,225))
    for y in range(0,a.height,z): d.line([(0,y),(a.width,y)],fill=(225,225,225))
    rows.append(r)
W=max(sum(p.width+8 for p in panelen),rows[0].width+rows[1].width+16)
# close-ups twee per rij
paren=[rows[i:i+2] for i in range(0,len(rows),2)]
H=520+sum(max(r.height for r in p)+8 for p in paren)+80
v=Image.new('RGB',(W,H),'white'); x=0
for p in panelen: v.paste(p,(x,0)); x+=p.width+8
y=520
for p in paren:
    x=0
    for r in p: v.paste(r,(x,y)); x+=r.width+16
    y+=max(r.height for r in p)+8
for i,bg in enumerate([(255,255,255),(248,248,232),(40,48,56),(24,24,24)]):
    v.paste(rgb_from(sp,bg),(i*72,y+8))
v.paste(m,(4*72,y+8))
# Gen 3 Staryu en Starmie 1x (anim_front_gba + normal_gba.pal), voor de maat
for j,nm in enumerate(['staryu','starmie']):
    g=Image.open('../../../../../graphics/pokemon/%s/anim_front_gba.png'%nm); pl=[int(t) for t in open('../../../../../graphics/pokemon/%s/normal_gba.pal'%nm).read().split()[3:]]
    g.putpalette(pl+[0]*(768-len(pl))); g=g.convert('RGB').crop((0,0,64,64)); v.paste(g,(5*72+j*72,y+8))
v.save(sys.argv[2]); print(sys.argv[2],v.size)
