# vel.png: r8 1x wit/donker | r8 8x | r6 8x | r7 8x | close-up gebied r6 | r7 | r8 (12x)
from PIL import Image, ImageDraw
def rgb(fn,z,bg=(255,255,255)):
    im=Image.open(fn).convert('RGBA'); im=im.resize((im.width*z,im.height*z),Image.NEAREST)
    b=Image.new('RGB',im.size,bg); b.paste(im,(0,0),im); return b
r8,r7,r6='kuiken_r8.png','../r7/kuiken_r7.png','../r6/kuiken_r6.png'
z=8; P=512; box=(24,28,56,64); Z=12; cw=(box[2]-box[0])*Z; ch=(box[3]-box[1])*Z
vel=Image.new('RGB',(84+3*(P+10),P+30+ch+30),(200,200,200)); d=ImageDraw.Draw(vel)
vel.paste(rgb(r8,1),(0,20)); vel.paste(rgb(r8,1,(40,40,40)),(0,94)); d.text((0,4),'r8 1x',fill=0); x=84
for nm,fn in (('r8 8x',r8),('r6 8x',r6),('r7 8x',r7)): vel.paste(rgb(fn,z),(x,20)); d.text((x,4),nm,fill=0); x+=P+10
x=84; y=P+50
for nm,fn in (('gebied r6 12x',r6),('gebied r7 12x',r7),('gebied r8 12x',r8)):
    vel.paste(rgb(fn,Z).crop((box[0]*Z,box[1]*Z,box[2]*Z,box[3]*Z)),(x,y)); d.text((x,y-16),nm,fill=0); x+=cw+10
vel.save('vel.png')
