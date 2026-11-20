# vel.png: sprite 8x | model op dezelfde schaal 8x ; close-ups kop en poten 12x naast model ; 1x op licht en donker
import numpy as np; from PIL import Image, ImageDraw
from reduce_pal import PAL
S=1.6; X0,Y0=17,20
sp=Image.open('vlieg_r1.png'); sp.save('/tmp/_v.png',transparency=0); sp=Image.open('/tmp/_v.png').convert('RGBA')
o=np.loadtxt('vlieg_r1.txt',dtype=int); H,W=o.shape; ox=(64-W)//2; oy=63-H
nat=Image.open('natief.png').convert('RGB')
def modelcrop(i0,i1,j0,j1,Z):   # model-uitsnede die exact op spritecellen i0..i1, j0..j1 valt, Z px per cel
    F=10
    big=nat.resize((1000,1000),Image.NEAREST)
    box=(int((X0+i0*S)*F),int((Y0+j0*S)*F),int((X0+i1*S)*F),int((Y0+j1*S)*F))
    return big.crop(box).resize(((i1-i0)*Z,(j1-j0)*Z),Image.LANCZOS)
def spcrop(i0,i1,j0,j1,Z):
    a=np.array([(255,255,255)]+PAL[1:])[o[j0:j1,i0:i1]].astype('uint8')
    return Image.fromarray(a).resize(((i1-i0)*Z,(j1-j0)*Z),Image.NEAREST)
A=spcrop(0,W,0,H,8); B=modelcrop(0,W,0,H,8)
k1,k2=spcrop(0,17,1,21,12),modelcrop(0,17,1,21,12)
p1,p2=spcrop(0,W,19,H,12),modelcrop(0,W,19,H,12)
w=max(A.width*2+30, p1.width*2+30); h=A.height+20+k1.height+20+p1.height+20+200
v=Image.new('RGB',(w,h),'white'); d=ImageDraw.Draw(v); y=0
v.paste(A,(0,y)); v.paste(B,(A.width+30,y)); d.text((4,y+2),'vlieg r1 (8x)',fill=(255,0,0)); d.text((A.width+34,y+2),'model zelfde schaal',fill=(255,0,0)); y+=A.height+20
v.paste(k1,(0,y)); v.paste(k2,(k1.width+30,y)); d.text((4,y+2),'kop 12x',fill=(255,0,0)); y+=k1.height+20
v.paste(p1,(0,y)); v.paste(p2,(p1.width+30,y)); d.text((4,y+2),'poten 12x',fill=(255,0,0)); y+=p1.height+20
for k,bg in enumerate([(248,248,248),(232,224,200),(40,40,48),(16,16,16)]):
    t=Image.new('RGBA',(64,64),bg+(255,)); t.alpha_composite(sp); t2=t.resize((128,128),Image.NEAREST)
    v.paste(t.convert('RGB'),(k*150,y+10)); v.paste(t2.convert('RGB'),(k*150+10+0,y+70)) if False else None
for k,bg in enumerate([(248,248,248),(40,40,48)]):
    t=Image.new('RGBA',(64,64),bg+(255,)); t.alpha_composite(sp)
    v.paste(t.resize((128,128),Image.NEAREST).convert('RGB'),(600+k*150,y+10))
v.save('vel.png'); print(v.size)
