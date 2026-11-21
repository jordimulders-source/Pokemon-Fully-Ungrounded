# vel: sprite | model verkleind (zelfde schaal) op 8x; kop en poten 12x naast model; 1x licht/donker
import numpy as np, sys; from PIL import Image, ImageDraw
from reduce_pal import PAL
naam=sys.argv[1]; uit=sys.argv[2]
o=np.loadtxt(naam,dtype=int); H,W=o.shape
nat=Image.open('natief.png').convert('RGB')
S=67/W
MS=Image.open('model_zelfde_schaal.png').convert('RGB')
def mc(i0,i1,j0,j1,Z):
    return MS.crop((i0,j0,i1,j1)).resize(((i1-i0)*Z,(j1-j0)*Z),Image.NEAREST)
def sc(i0,i1,j0,j1,Z):
    a=np.array([(255,255,255)]+PAL[1:])[o[j0:j1,i0:i1]].astype('uint8')
    return Image.fromarray(a).resize(((i1-i0)*Z,(j1-j0)*Z),Image.NEAREST)
rij=[[sc(0,W,0,H,8),mc(0,W,0,H,8)],[sc(0,20,1,25,12),mc(0,20,1,25,12)],[sc(0,W,21,H,12),mc(0,W,21,H,12)]]
tit=[['r3 8x','model, zelfde schaal'],['kop 12x','model'],['poten 12x','model']]
w=max(sum(p.width+20 for p in r) for r in rij); h=sum(r[0].height+24 for r in rij)+400
v=Image.new('RGB',(w,h),'white'); d=ImageDraw.Draw(v); y=0
for r,t in zip(rij,tit):
    x=0
    for p,tt in zip(r,t): v.paste(p,(x,y+16)); d.text((x+2,y+2),tt,fill=(255,0,0)); x+=p.width+20
    y+=r[0].height+24
full=np.zeros((64,64),int); x0=(64-W)//2; full[62-H:62,x0:x0+W]=o
rgba=np.zeros((64,64,4),'uint8'); rgba[...,:3]=np.array(PAL)[full]; rgba[...,3]=(full>0)*255
sp=Image.fromarray(rgba)
for k,bg in enumerate([(248,248,248),(40,40,48)]):
    t=Image.new('RGBA',(64,64),bg+(255,)); t.alpha_composite(sp)
    v.paste(t.convert('RGB'),(k*80,y+10)); v.paste(t.resize((128,128),Image.NEAREST).convert('RGB'),(180+k*150,y+10))
vd=Image.open('verschil.png'); d.text((340,y-4),'verschil t.o.v. kale reductie: rood = reparatie, blauw = extra verre poten/vleugelruis',fill=(255,0,0))
v.paste(vd.resize((vd.width//2*1,vd.height//2*1)) if False else vd,(500,y+10)) if v.width>=500+vd.width else None
v.save(uit); print(v.size)
