# vel.png: r7 1x wit/donker | r7 8x | r6 8x | close-up gebied r6 | r7
from PIL import Image, ImageDraw
def rgb(fn,z,bg=(255,255,255)):
    im=Image.open(fn).convert('RGBA'); im=im.resize((im.width*z,im.height*z),Image.NEAREST)
    b=Image.new('RGB',im.size,bg); b.paste(im,(0,0),im); return b
r7,r6='kuiken_r7.png','../r6/kuiken_r6.png'
z=8; P=512; box=(24,28,56,64); Z=12; cw=(box[2]-box[0])*Z; ch=(box[3]-box[1])*Z
vel=Image.new('RGB',(84+2*(P+10)+2*(cw+10),max(P,ch)+30),(200,200,200)); d=ImageDraw.Draw(vel)
vel.paste(rgb(r7,1),(0,20)); vel.paste(rgb(r7,1,(40,40,40)),(0,94)); d.text((0,4),'r7 1x',fill=0); x=84
for nm,fn in (('r7 8x',r7),('r6 8x',r6)): vel.paste(rgb(fn,z),(x,20)); d.text((x,4),nm,fill=0); x+=P+10
for nm,fn in (('gebied r6 12x',r6),('gebied r7 12x',r7)):
    vel.paste(rgb(fn,Z).crop((box[0]*Z,box[1]*Z,box[2]*Z,box[3]*Z)),(x,20)); d.text((x,4),nm,fill=0); x+=cw+10
vel.save('vel.png')
