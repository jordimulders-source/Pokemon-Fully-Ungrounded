# vel.py SPRITE.png UIT.png [KAAL.png]: rij 1: sprite 8x | kaal 8x | model op schaal 8x | Gen 3 Starmie 8x
# rij 2: close-ups 12x (sprite | model): bovenarm+juweel, linkerarm, achterpunten links, achterpunten rechts/onder
# rij 3: 1x sprite op wit/creme/donker/zwart, model 1x, Gen 3 Starmie + Staryu 1x, maatstaf skinguin/dundragoon/viscacha/awki 1x
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
R='../../'
def rgb_from(im,bg=(255,255,255),frame=0):
    o=np.asarray(im)[frame*64:frame*64+64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
def pal_png(p,bg=(255,255,255)):
    im=Image.open(p)
    if im.mode=='P': return rgb_from(im,bg)
    im=im.convert('RGBA'); b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB').crop((0,0,64,64))
sp=Image.open(sys.argv[1]); s=rgb_from(sp); m=model_op_schaal()
G3=Image.open(R+'../../../graphics/pokemon/starmie/anim_front_gba.png'); g3=rgb_from(G3)
SY=Image.open(R+'../../../graphics/pokemon/staryu/anim_front_gba.png'); sy=rgb_from(SY)
M=Image.open(MODEL).convert('RGB')
def mcrop(x0,y0,x1,y1,z):
    f=lambda u:9.75+10.24*u
    u0=(x0-CX)/S+GEM[0]; u1=(x1-CX)/S+GEM[0]; v0=(y0-CY)/S+GEM[1]; v1=(y1-CY)/S+GEM[1]
    return M.crop((int(f(u0)),int(f(v0)),int(f(u1)),int(f(v1)))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
panelen=[s.resize((512,512),Image.NEAREST)]
if len(sys.argv)>3: panelen.append(rgb_from(Image.open(sys.argv[3])).resize((512,512),Image.NEAREST))
panelen+= [m.resize((512,512),Image.NEAREST), g3.resize((512,512),Image.NEAREST)]
zones=[('bovenarm+juweel',18,5,42,36),('linkerarm',3,20,27,46),('achter links (tl, ll)',4,10,24,47),('achter rechts/onder (tr, rl, b)',30,6,60,58)]
z=12; rows=[]
for n,x0,y0,x1,y1 in zones:
    a=s.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
    b=mcrop(x0,y0,x1,y1,z) if n.startswith(('boven','linker')) else g3.crop((x0,y0,x1,y1)).resize(a.size,Image.NEAREST)
    r=Image.new('RGB',(a.width*2+8,a.height+14),'white'); r.paste(a,(0,14)); r.paste(b,(a.width+8,14))
    d=ImageDraw.Draw(r); d.text((2,1),n+(' | model' if n.startswith(('boven','linker')) else ' | Gen 3 Starmie'),fill=(0,0,0))
    for x in range(0,a.width,z): d.line([(x,14),(x,14+a.height)],fill=(225,225,225))
    for y in range(14,14+a.height,z): d.line([(0,y),(a.width,y)],fill=(225,225,225))
    rows.append(r)
W=max(sum(p.width+8 for p in panelen),rows[0].width+rows[1].width+16)
paren=[rows[i:i+2] for i in range(0,len(rows),2)]
H=520+sum(max(r.height for r in p)+8 for p in paren)+240
v=Image.new('RGB',(W,H),'white'); x=0
for p in panelen: v.paste(p,(x,0)); x+=p.width+8
y=520
for p in paren:
    x=0
    for r in p: v.paste(r,(x,y)); x+=r.width+16
    y+=max(r.height for r in p)+8
y+=8
ones=[rgb_from(sp,bg) for bg in [(255,255,255),(248,248,232),(40,48,56),(24,24,24)]]+[m,g3,sy]
for f in ('skinguin/af/skinguin.png','dundragoon/af/dundragoon.png','viscacha/af/viscacha.png','awki/af/awki.png'): ones.append(pal_png(R+f))
for i,im in enumerate(ones): v.paste(im,(i*72,y))
ImageDraw.Draw(v).text((0,y+68),'1x: sprite wit/creme/donker/zwart | model | Gen 3 Starmie | Staryu | skinguin | dundragoon | zapacha | princadee',fill=(0,0,0))
# 2x rij
y+=82
for i,im in enumerate([rgb_from(sp),g3,sy]): v.paste(im.resize((128,128),Image.NEAREST),(i*136,y)) if y+128<=H else None
v.save(sys.argv[2]); print(sys.argv[2],v.size)
