# vel.png: r4 A 1x (wit/donker) + B 1x | r4 A 8x | r4 B 8x | r3 A 8x | model verkleind
import numpy as np, os
from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__))
def rg(fn,z,bg=(255,255,255)):
    im=Image.open(fn).convert('RGBA'); im=im.resize((64*z,64*z),Image.NEAREST)
    b=Image.new('RGB',im.size,bg); b.paste(im,(0,0),im); return b
mo=Image.open(H+'/../../model/fase1_model.png').convert('RGB'); a=np.array(mo).sum(2)<700; ys,xs=np.nonzero(a)
mc=mo.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); w=round(mc.width*44/mc.height)
mv=Image.new('RGB',(64,64),'white'); mv.paste(mc.resize((w,44),Image.LANCZOS),((64-w)//2,20))
z=8; P=64*z; vel=Image.new('RGB',(80+4*(P+10),P+30),(200,200,200)); d=ImageDraw.Draw(vel)
A=H+'/kuiken_r4.png'; B=H+'/kuiken_r4_haarB.png'
vel.paste(rg(A,1),(4,20)); vel.paste(rg(A,1,(40,40,40)),(4,90)); vel.paste(rg(B,1),(4,170)); vel.paste(rg(B,1,(40,40,40)),(4,240))
d.text((4,6),'r4 A 1x',fill=0); d.text((4,158),'r4 B 1x',fill=0); x=80
for nm,im in (('r4 haren A',rg(A,z)),('r4 haren B',rg(B,z)),('r3 haren A',rg(H+'/../r3/kuiken_r3.png',z)),('model verkleind',mv.resize((P,P),Image.NEAREST))):
    vel.paste(im,(x,20)); d.text((x,6),nm,fill=0); x+=P+10
vel.save(H+'/vel.png')
