# vel.png: r5 1x wit/donker | r5 8x met omcirkeld gebied | r4 (haren B) 8x | close-up gebied 8x r4 | r5
import numpy as np
from PIL import Image, ImageDraw
def rgb(fn,z,bg=(255,255,255)):
    im=Image.open(fn).convert('RGBA'); im=im.resize((im.width*z,im.height*z),Image.NEAREST)
    b=Image.new('RGB',im.size,bg); b.paste(im,(0,0),im); return b
r5,r4='kuiken_r5.png','../r4/kuiken_r4_haarB.png'
z=8; P=512; box=(26,32,54,64)   # omcirkeld gebied (rechterhelft: onderarm, staart, dij, poten)
cw=(box[2]-box[0])*z; ch=(box[3]-box[1])*z
vel=Image.new('RGB',(84+2*(P+10)+2*cw+20,P+30),(200,200,200)); d=ImageDraw.Draw(vel)
vel.paste(rgb(r5,1),(0,20)); vel.paste(rgb(r5,1,(40,40,40)),(0,94)); d.text((0,4),'r5 1x',fill=0)
x=84
for nm,fn in (('r5 8x',r5),('r4 (haren B) 8x',r4)):
    vel.paste(rgb(fn,z),(x,20)); d.text((x,4),nm,fill=0)
    if fn==r5: d.ellipse((x+box[0]*z-20,20+box[1]*z-30,x+box[2]*z+20,20+box[3]*z+10),outline=(220,0,0),width=3)
    x+=P+10
for nm,fn in (('gebied r4',r4),('gebied r5',r5)):
    vel.paste(rgb(fn,z).crop((box[0]*z,box[1]*z,box[2]*z,box[3]*z)),(x,20)); d.text((x,4),nm,fill=0); x+=cw+10
vel.save('vel.png')
