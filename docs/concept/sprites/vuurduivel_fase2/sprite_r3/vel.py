# vel.py: r3 8x | r2 8x | model; daaronder handvlam en staartvlam 12x (model | r2 | r3), staartproef apart; 1x (r3 links, r2 rechts)
import subprocess; from PIL import Image, ImageDraw
X0,Y0,NX,NY=4,5,62,6
S='/tmp/_vd2_'
def op(f,bgc=(255,255,255)):
    b=Image.new('RGBA',(64,64),bgc+(255,)); b.alpha_composite(Image.open(f).convert('RGBA')); return b.convert('RGB')
n=Image.open('natief.png')
mod=Image.new('RGB',(128,128),'white'); cx,cy=NX-X0*2,NY-Y0*2; mod.paste(n.crop((max(cx,0),max(cy,0),cx+128,cy+128)),(max(-cx,0),max(-cy,0)))
pan=[op('vuurduivel2_r3.png').resize((512,512),Image.NEAREST),op('../sprite_r2/vuurduivel2_r2.png').resize((512,512),Image.NEAREST),mod.resize((512,512),Image.NEAREST)]
def zoom(x0,y0,x1,y1,z=12):
    m=n.crop((NX+(x0-X0)*2,NY+(y0-Y0)*2,NX+(x1-X0)*2,NY+(y1-Y0)*2)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST)
    r1=op('../sprite_r2/vuurduivel2_r2.png').crop((x0,y0,x1,y1)).resize(m.size,Image.NEAREST)
    r2=op('vuurduivel2_r3.png').crop((x0,y0,x1,y1)).resize(m.size,Image.NEAREST)
    v=Image.new('RGB',(m.width*3+20,m.height),(235,235,235)); v.paste(m,(0,0)); v.paste(r1,(m.width+10,0)); v.paste(r2,(2*m.width+20,0)); return v
k1=zoom(3,15,15,30); k2=zoom(48,31,62,47)
import os
if os.path.exists('proef_staart.png'):
    pr=op('proef_staart.png').crop((48,31,62,47)).resize((14*12,16*12),Image.NEAREST); k2b=Image.new('RGB',(k2.width+pr.width+10,k2.height),(235,235,235)); k2b.paste(k2,(0,0)); k2b.paste(pr,(k2.width+10,0)); k2=k2b
W=max(3*522,k1.width+k2.width+30); H=512+10+max(k1.height,k2.height)+10+80
v=Image.new('RGB',(W,H),(235,235,235)); d=ImageDraw.Draw(v)
for i,p in enumerate(pan): v.paste(p,(i*522,0))
d.text((4,4),'r3',fill=(0,0,0)); d.text((526,4),'r2',fill=(0,0,0)); d.text((1048,4),'model',fill=(0,0,0))
v.paste(k1,(0,522)); v.paste(k2,(k1.width+20,522))
y=522+max(k1.height,k2.height)+10
for i,c in enumerate([(255,255,255),(200,220,200),(40,40,56),(16,16,16)]):
    v.paste(op('vuurduivel2_r3.png',c),(i*74,y)); v.paste(op('../sprite_r2/vuurduivel2_r2.png',c),(400+i*74,y))
v.save('vel.png')
