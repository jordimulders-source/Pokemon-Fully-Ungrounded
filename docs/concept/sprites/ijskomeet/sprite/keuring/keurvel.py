# keurvel r1: sprite 8x | model64 8x ; rij Gen 3 op 2x en 1x met de sprite ertussen
from PIL import Image, ImageDraw
G='../../../../../../graphics/pokemon/'
def g3(n):
    im=Image.open(G+n+'/anim_front_gba.png').convert('RGBA').crop((0,0,64,64))
    bg=im.getpixel((0,0)); d=[(0,0,0,0) if p[:3]==bg[:3] else p for p in im.getdata()]
    im.putdata(d); return im
spr=Image.open('../r1.png').convert('RGBA'); d=list(spr.getdata()); spr.putdata([(0,0,0,0) if p[:3]==(255,255,255) else p for p in d])
mod=Image.open('../model64.png').convert('RGBA')
W=1100; H=8*64+40+2*64+30+64+30
vel=Image.new('RGBA',(W,H),(255,255,255,255)); dr=ImageDraw.Draw(vel)
vel.paste(spr.resize((512,512),Image.NEAREST),(10,20),spr.resize((512,512),Image.NEAREST))
vel.paste(mod.resize((512,512),Image.NEAREST),(560,20))
dr.text((10,4),'r1 (8x)',fill='black'); dr.text((560,4),'model64 (8x, box-verkleind)',fill='black')
rij=['lunatone','solrock','glalie','r1','regice','metagross']
y=20+512+20; dr.text((10,y-14),'2x',fill='black')
for i,n in enumerate(rij):
    im=spr if n=='r1' else g3(n); b=im.resize((128,128),Image.NEAREST)
    vel.paste(b,(10+i*140,y),b); dr.text((10+i*140,y+128),n,fill='black')
y2=y+128+30; dr.text((10,y2-14),'1x',fill='black')
for i,n in enumerate(rij):
    im=spr if n=='r1' else g3(n); vel.paste(im,(10+i*70,y2),im)
vel.convert('RGB').save('keurvel_r1.png')
# close-up kop
k=Image.new('RGB',(2*12*36+20,12*36),'white')
k.paste(spr.crop((0,20,36,56)).resize((432,432),Image.NEAREST),(0,0),spr.crop((0,20,36,56)).resize((432,432),Image.NEAREST))
k.paste(mod.crop((0,20,36,56)).convert('RGB').resize((432,432),Image.NEAREST),(452,0))
k.save('kop_12x.png')
