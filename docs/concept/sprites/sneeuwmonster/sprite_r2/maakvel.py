# maakvel.py: vel.png voor r2 = r2 8x | r1 8x | model op dezelfde schaal 8x / close-up kop 12x (r1 | model) en lijf 12x /
# 1x op wit, crème, donker, zwart + model 1x / mondvarianten 8x naast elkaar (zonder | shroomish | chinchou), kop-uitsnede
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
U='sprite_r2/'
def rgb_from(path,bg=(255,255,255)):
    im=Image.open(path); o=np.asarray(im); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
M=Image.open(MODEL).convert('RGB'); f=lambda u,ph:ph+0.5+10.24*u
def mcrop(x0,y0,x1,y1,z):
    u0=(x0-X0)/S+U0; u1=(x1-X0)/S+U0; v0=(y0-Y0)/S+V0; v1=(y1-Y0)/S+V0
    return M.crop((int(f(u0,9.05)),int(f(v0,9.25)),int(f(u1,9.05)),int(f(v1,9.25)))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
def grid(a,z,c=(225,225,225)):
    d=ImageDraw.Draw(a)
    for x in range(0,a.width,z): d.line([(x,0),(x,a.height)],fill=c)
    for y in range(0,a.height,z): d.line([(0,y),(a.width,y)],fill=c)
    return a
B=(14,8,50,56)   # figuurvak voor 8x
z=8; w=(B[2]-B[0])*z; h=(B[3]-B[1])*z
r1=rgb_from(U+'sneeuwmonster_r2.png'); kaal=rgb_from('sprite_r1/sneeuwmonster_r1.png')
rij1=[r1.crop(B).resize((w,h),Image.NEAREST), kaal.crop(B).resize((w,h),Image.NEAREST), mcrop(*B,z)]
kop=(18,9,46,32); lijf=(16,30,48,54); Z=12
ck=[grid(r1.crop(kop).resize(((kop[2]-kop[0])*Z,(kop[3]-kop[1])*Z),Image.NEAREST),Z), mcrop(*kop,Z)]
cl=[grid(r1.crop(lijf).resize(((lijf[2]-lijf[0])*Z,(lijf[3]-lijf[1])*Z),Image.NEAREST),Z), mcrop(*lijf,Z)]
monden=[('zonder mond (r2)',U+'sneeuwmonster_r2.png'),('mond_shroomish',U+'mond_shroomish.png'),('mond_chinchou',U+'mond_chinchou.png')]
mk=(18,15,40,33)
mrij=[grid(rgb_from(p).crop(mk).resize(((mk[2]-mk[0])*8,(mk[3]-mk[1])*8),Image.NEAREST),8) for _,p in monden]
W=max(3*(w+10), 4*(16*12+8), 2*(ck[0].width+8)+8, 3*(mrij[0].width+10))
H=h+20+ck[0].height+10+cl[0].height+10+80+20+mrij[0].height+30+2*9*12+60
v=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(v); y=0
for i,(p,t) in enumerate(zip(rij1,['r2 8x','r1 8x','model (zelfde schaal)'])): v.paste(p,(i*(w+10),y+16)); d.text((i*(w+10)+4,y+2),t,fill=(200,0,0))
y+=h+20
for r in (ck,cl):
    x=0
    for p in r: v.paste(p,(x,y)); x+=p.width+8
    y+=r[0].height+10
x=0
for bg in [(255,255,255),(248,248,232),(40,48,56),(24,24,24)]: v.paste(rgb_from(U+'sneeuwmonster_r2.png',bg),(x,y)); x+=72
m1=Image.new('RGB',(64,64),'white'); m1.paste(mcrop(0,0,64,64,1),(0,0)); v.paste(m1,(x,y)); x+=72
for _,p in monden[1:]: v.paste(rgb_from(p),(x,y)); x+=72
y+=80
for i,((t,_),p) in enumerate(zip(monden,mrij)): d.text((i*(p.width+10)+4,y),t,fill=(200,0,0)); v.paste(p,(i*(p.width+10),y+14))
y+=mrij[0].height+20
ov=[('LB RB (r2)',U+'sneeuwmonster_r2.png'),('LA RA',U+'oog_LA_RA.png'),('LA RB',U+'oog_LA_RB.png'),('LB RA',U+'oog_LB_RA.png')]
ok=(20,20,36,29); oz=12
for i,(t,p) in enumerate(ov):
    a=grid(rgb_from(p).crop(ok).resize(((ok[2]-ok[0])*oz,(ok[3]-ok[1])*oz),Image.NEAREST),oz)
    d.text((i*(a.width+8)+4,y),'ogen '+t,fill=(200,0,0)); v.paste(a,(i*(a.width+8),y+14))
a2=mcrop(*ok,oz); d.text((4,y+14+a.height+4),'model',fill=(200,0,0)); v.paste(a2,(0,y+28+a.height+4))
v.save(U+'vel.png'); print(U+'vel.png',v.size)
