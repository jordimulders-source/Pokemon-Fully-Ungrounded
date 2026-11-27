# vel_oog.png: kop/oog 12x: r4 | r2 | r3 | model op schaal; daaronder 1x (echte grootte): r4 | r2 | r3 | model
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
from PIL import ImageDraw
def plat(p):
    im=Image.open(p).convert('RGBA'); out=Image.new('RGB',im.size,(255,255,255)); out.paste(im,(0,0),im); return out
ims=[plat(HIER+'/hoatzin_r4.png'),plat(HIER+'/../r2/hoatzin_r2.png'),plat(HIER+'/../r3/hoatzin_r3.png'),model_op_schaal()]
nm=['r4','r2','r3','model']
box=(12,8,28,22); f=12
groot=[i.crop(box).resize(((box[2]-box[0])*f,(box[3]-box[1])*f),0) for i in ims]
W=sum(g.width for g in groot)+8*3; H=groot[0].height+20+64+20
vel=Image.new('RGB',(W,H),(220,220,220)); d=ImageDraw.Draw(vel); x=0
for g,i,n in zip(groot,ims,nm):
    vel.paste(g,(x,16)); d.text((x+4,2),n+' 12x',fill=(0,0,0))
    vel.paste(i,(x,groot[0].height+36)); d.text((x+70,groot[0].height+60),n+' 1x',fill=(0,0,0))
    x+=g.width+8
vel.save(HIER+'/vel_oog.png'); print(vel.size)
