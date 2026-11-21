# vel.png: r2 | r1 | model (8x, zelfde schaal) ; kop en poten 12x: r2 | model ; 1x en 2x op licht en donker
import numpy as np; from PIL import Image, ImageDraw
from reduce_pal import PAL
S=1.6; X0,Y0=17,20
o2=np.loadtxt('vlieg_r2.txt',dtype=int); o1=np.loadtxt('vlieg_r1.txt',dtype=int); H,W=o2.shape
nat=Image.open('natief.png').convert('RGB').resize((1000,1000),Image.NEAREST)
def mc(i0,i1,j0,j1,Z):
    b=(int((X0+i0*S)*10),int((Y0+j0*S)*10),int((X0+i1*S)*10),int((Y0+j1*S)*10))
    return nat.crop(b).resize(((i1-i0)*Z,(j1-j0)*Z),Image.LANCZOS)
def sc(o,i0,i1,j0,j1,Z):
    a=np.array([(255,255,255)]+PAL[1:])[o[j0:j1,i0:i1]].astype('uint8')
    return Image.fromarray(a).resize(((i1-i0)*Z,(j1-j0)*Z),Image.NEAREST)
rij=[[sc(o2,0,W,0,H,8),sc(o1,0,W,0,H,8),mc(0,W,0,H,8)],
     [sc(o2,0,18,1,22,12),mc(0,18,1,22,12)],
     [sc(o2,0,W,18,H,12),mc(0,W,18,H,12)]]
tit=[['r2','r1','model'],['r2 kop 12x','model'],['r2 poten 12x','model']]
w=max(sum(p.width+20 for p in r) for r in rij); h=sum(r[0].height+24 for r in rij)+150
v=Image.new('RGB',(w,h),'white'); d=ImageDraw.Draw(v); y=0
for r,t in zip(rij,tit):
    x=0
    for p,tt in zip(r,t): v.paste(p,(x,y+16)); d.text((x+2,y+2),tt,fill=(255,0,0)); x+=p.width+20
    y+=r[0].height+24
im=Image.open('vlieg_r2.png'); im.save('/tmp/_v2.png',transparency=0); sp=Image.open('/tmp/_v2.png').convert('RGBA')
for k,bg in enumerate([(248,248,248),(40,40,48)]):
    t=Image.new('RGBA',(64,64),bg+(255,)); t.alpha_composite(sp)
    v.paste(t.convert('RGB'),(k*80,y+10)); v.paste(t.resize((128,128),Image.NEAREST).convert('RGB'),(200+k*150,y+10))
v.save('vel.png'); print(v.size)
