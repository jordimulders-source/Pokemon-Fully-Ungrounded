import numpy as np
from PIL import Image
s=Image.open('sprite_r1/sprite.png'); pal=s.getpalette(); si=np.array(s)
srgb=s.convert('RGBA'); a=np.array(srgb); a[si==0,3]=0; srgb=Image.fromarray(a)
m=Image.open('model/model_gekozen_natief.png').convert('RGB'); ma=np.array(m)
bg=ma[0,0]; print('bg',bg)
mask=(np.abs(ma.astype(int)-bg).sum(2)>30); ys,xs=np.where(mask); print('model bbox',xs.min(),xs.max(),ys.min(),ys.max())
ys,xs=np.where(si!=0); print('sprite bbox',xs.min(),xs.max(),ys.min(),ys.max())
mr=m.resize((round(99*0.787),)*2,Image.BOX)
W=8
def up(im,f): return im.resize((im.width*f,im.height*f),Image.NEAREST)
canvas=Image.new('RGBA',(64*8*2+78*8+60,78*8+200),(200,220,200,255))
x=10
canvas.paste(up(srgb,1),(x,10),up(srgb,1)); canvas.paste(up(srgb,2),(x+80,10),up(srgb,2)); canvas.paste(mr,(x+220,10))
canvas.paste(up(srgb,8),(10,150),up(srgb,8))
canvas.paste(up(mr.convert('RGBA'),8),(10+64*8+20,150))
canvas.save('keuring_r1/vel.png')
