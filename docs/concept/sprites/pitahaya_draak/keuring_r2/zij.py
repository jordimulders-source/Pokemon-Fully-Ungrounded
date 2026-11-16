from PIL import Image
r2=Image.open('sprite_r2/pitahaya_r2.png').convert('RGBA')
r1=Image.open('sprite_r2/pitahaya_r1.png').convert('RGBA')
nat=Image.open('sprite_r2/natief.png').convert('RGBA')
def bg(im,c=(255,255,255,255)):
    b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b
# crop sprite 14..48 x, 5..57 y
box=(14,5,48,57)
s=8
a=bg(r2.crop(box)).resize(((box[2]-box[0])*s,(box[3]-box[1])*s),Image.NEAREST)
b=bg(r1.crop(box)).resize(a.size,Image.NEAREST)
# natief: find bbox of non-white
import numpy as np
n=np.array(nat)[:,:,:3].astype(int)
m=(n.sum(2)<720)
ys,xs=np.where(m); print(xs.min(),xs.max(),ys.min(),ys.max())
nc=nat.crop((xs.min()-6,ys.min()-6,xs.max()+7,ys.max()+7))
nc=nc.resize((int(nc.width*a.height/nc.height),a.height),Image.LANCZOS)
W=a.width+b.width+nc.width+40
out=Image.new('RGBA',(W,a.height),(200,200,200,255))
out.paste(a,(0,0)); out.paste(b,(a.width+20,0)); out.paste(nc,(a.width+b.width+40,0))
out.save('keuring_r2/zij8x.png')
# 1x and 2x on light & dark
o=Image.new('RGBA',(64*6+50,64*2+20),(255,255,255,255))
for i,(im,sc) in enumerate([(r2,1),(r1,1),(r2,2),(r1,2)]):
    pass
row=[]
x=0
canvas=Image.new('RGBA',(400,300),(255,255,255,255))
dark=Image.new('RGBA',(400,150),(40,40,48,255))
canvas.paste(dark,(0,150))
xx=5
for im,sc in [(r2,1),(r1,1),(r2,2),(r1,2)]:
    t=im.resize((64*sc,64*sc),Image.NEAREST)
    canvas.alpha_composite(t,(xx,5)); canvas.alpha_composite(t,(xx,155)); xx+=64*sc+10
canvas.save('keuring_r2/1x2x.png')
