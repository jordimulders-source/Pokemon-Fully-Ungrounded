# vel.py: r10 | r9 | echte Altaria (8x); kop-close-up 20x naast de echte Altaria-kop; 1x op licht/donker. python3 sprite_r10/vel.py
from PIL import Image, ImageDraw
ALT='../../../../../graphics/pokemon/altaria/anim_front.png'
def plat(p,bg=(255,255,255)):
    im=Image.open(p).convert('RGBA').crop((0,0,64,64)); b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
def echte(bg=(255,255,255)):
    im=Image.open(ALT); im=im.crop((0,0,64,64)).convert('RGBA'); px=im.load()
    for y in range(64):
        for x in range(64):
            if px[x,y][:3]==(152,208,160): px[x,y]=(0,0,0,0)
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
R10,R9='sprite_r10/altaria_r10.png','sprite_r9/altaria_r9.png'
Z=20; kw,kh=17,12
vel=Image.new('RGB',(3*512+32,24+512+24+kh*Z+24+150),'white'); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate(((plat(R10),'r10'),(plat(R9),'r9'),(echte(),'echte Altaria (Gen 3)'))):
    vel.paste(im.resize((512,512),Image.NEAREST),(i*528,24)); d.text((i*528+4,6),t,fill=(0,0,0))
y=24+512+20
d.text((4,y-14),'kop 20x: r10 (X18-34, Y16-27) | echte Altaria (X19-37, Y11-24)',fill=(0,0,0))
a=plat(R10).crop((18,16,18+kw,16+kh)).resize((kw*Z,kh*Z),Image.NEAREST)
b=echte().crop((20,12,20+kw+1,12+kh+1)).resize(((kw+1)*Z,(kh+1)*Z),Image.NEAREST)
vel.paste(a,(0,y)); vel.paste(b,(a.width+24,y))
y+=b.height+16
for i,bg in enumerate(((255,255,255),(232,224,200),(80,96,120),(24,24,32))):
    vel.paste(plat(R10,bg),(8+i*80,y)); vel.paste(plat(R10,bg).resize((128,128),Image.NEAREST),(340+i*140,y))
vel.save('sprite_r10/vel.png')
