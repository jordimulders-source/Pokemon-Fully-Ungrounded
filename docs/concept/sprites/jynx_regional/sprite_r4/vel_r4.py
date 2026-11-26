# vel_r4.py: r4 8x | r3 8x | model 8x / close-ups 12x van de rok (r4 | r3 | model, r4 | variant B | model, rokvouw r4 | r3 | B | model) /
# 1x op licht en donker naast Skinguin en Dundragoon + model 1x. Ook jynx_regional_r4_8x.png.
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
def rgb_from(path,bg=(255,255,255)):
    im=Image.open(path); o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
R3,R2,VAR='sprite_r4/jynx_regional_r4.png','sprite_r3/jynx_regional_r3.png','sprite_r4/jynx_regional_r4_B_zonder_lijn.png'
s3,s2,sv=rgb_from(R3),rgb_from(R2),rgb_from(VAR); m=model_op_schaal()
s3.resize((512,512),Image.NEAREST).save('sprite_r4/jynx_regional_r4_8x.png')
M=Image.open(MODEL).convert('RGB')
def mcrop(x0,y0,x1,y1,z):
    u0=(x0-X0)/S+U0; u1=(x1-X0)/S+U0; v0=(y0-Y0)/S+V0; v1=(y1-Y0)/S+V0
    f=lambda u,ph:ph+0.5+10.24*u
    return M.crop((int(f(u0,9.25)),int(f(v0,9.20)),int(f(u1,9.25)),int(f(v1,9.20)))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def raster(a,z):
    d=ImageDraw.Draw(a)
    for x in range(0,a.width,z): d.line([(x,0),(x,a.height)],fill=(225,225,225))
    for y in range(0,a.height,z): d.line([(0,y),(a.width,y)],fill=(225,225,225))
    return a
z=12
zones=[('rok',8,34,56,63,[s3,s2]),('rok: r4 | variant B zonder lijn',8,34,56,63,[s3,sv]),('rokvouw rechts',28,40,52,54,[s3,s2,sv])]
rows=[]
for n,x0,y0,x1,y1,srcs in zones:
    ps=[raster(q.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST),z) for q in srcs]+[mcrop(x0,y0,x1,y1,z)]
    r=Image.new('RGB',(sum(p.width+8 for p in ps),ps[0].height+18),'white'); d=ImageDraw.Draw(r)
    d.text((2,2),n+'  (r4 links, dan '+('r3' if srcs[1] is s2 else 'variant B')+(', dan variant B' if len(srcs)>2 else '')+', dan model)',fill=(0,0,0)); x=0
    for p in ps: r.paste(p,(x,18)); x+=p.width+8
    rows.append(r)
top=[s3.resize((512,512),Image.NEAREST),s2.resize((512,512),Image.NEAREST),m.resize((512,512),Image.NEAREST)]
W=max(1560,max(r.width for r in rows)); H=530+sum(r.height+8 for r in rows)+170
v=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(v)
for i,p in enumerate(top): v.paste(p,(i*520,0)); d.text((i*520+4,514),['r4','r3','model op schaal'][i],fill=(0,0,0))
y=530
for r in rows: v.paste(r,(0,y)); y+=r.height+8
def ref(path,bg):
    im=Image.open(path).convert('RGBA'); im=im.crop((0,0,64,64)); b=Image.new('RGB',(64,64),bg); b.paste(im,(0,0),im); return b
refs=['../skinguin/af/skinguin.png','../dundragoon/af/dundragoon.png']
x=0
for bg in [(255,255,255),(248,248,232),(40,48,56),(24,24,24)]:
    for q in [rgb_from(R3,bg)]+[ref(p,bg) for p in refs]: v.paste(q.resize((128,128),Image.NEAREST) if False else q,(x,y+8)); x+=68
    x+=12
v.paste(m,(x,y+8)); y2=y+80
x=0
for bg in [(255,255,255),(40,48,56)]:
    for q in [rgb_from(R3,bg)]+[ref(p,bg) for p in refs]: v.paste(q.resize((128,128),Image.NEAREST),(x,y2)); x+=136
v.save('sprite_r4/vel.png'); print(v.size)
