# vel.py: A | B | r10 | echte Altaria (8x); koppen 20x (A | B | echte Altaria); 1x op licht/donker. python3 sprite_r11/vel.py
from PIL import Image, ImageDraw
ALT='../../../../../graphics/pokemon/altaria/anim_front.png'
def plat(p,bg=(255,255,255),groen=False):
    im=Image.open(p).convert('RGBA').crop((0,0,64,64))
    if groen:
        px=im.load()
        for y in range(64):
            for x in range(64):
                if px[x,y][:3]==(152,208,160): px[x,y]=(0,0,0,0)
    b=Image.new('RGBA',(64,64),bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
A,B,R10='sprite_r11/altaria_r11A.png','sprite_r11/altaria_r11B.png','sprite_r10/altaria_r10.png'
Z=20; vel=Image.new('RGB',(4*400+48,24+400+24+16*Z+24+150),'white'); d=ImageDraw.Draw(vel)
for i,(im,t) in enumerate(((plat(A),'r11 A (100 %), 6,25x'),(plat(B),'r11 B (±117 %)'),(plat(R10),'r10'),(plat(ALT,groen=True),'echte Altaria'))):
    vel.paste(im.resize((400,400),Image.NEAREST),(i*416,24)); d.text((i*416+4,6),t,fill=(0,0,0))
y=24+400+20; x=0
d.text((4,y-14),'koppen 20x: A (X15-35, Y15-31) | B (zelfde uitsnede) | echte Altaria (X17-37, Y10-26)',fill=(0,0,0))
for im,box in ((plat(A),(15,15,36,31)),(plat(B),(15,15,36,31)),(plat(ALT,groen=True),(17,10,38,26))):
    c=im.crop(box).resize(((box[2]-box[0])*Z//2*2//2,(box[3]-box[1])*Z//2*2//2),Image.NEAREST)
    c=im.crop(box).resize(((box[2]-box[0])*16,(box[3]-box[1])*16),Image.NEAREST)
    vel.paste(c,(x,y)); x+=c.width+16
y+=16*16+24
for k,p in enumerate((A,B)):
    for i,bg in enumerate(((255,255,255),(232,224,200),(80,96,120),(24,24,32))):
        vel.paste(plat(p,bg),(8+k*360+i*80,y)); d.text((8+k*360,y+70),'A' if k==0 else 'B',fill=(0,0,0))
vel.save('sprite_r11/vel.png')
