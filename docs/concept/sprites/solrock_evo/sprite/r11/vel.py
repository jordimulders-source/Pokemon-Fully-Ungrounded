import numpy as np; from PIL import Image, ImageDraw
L=(232,236,224,255); D=(40,44,64,255)
def rgba(fn,bg,crop=None):
    im=Image.open(fn); 
    if crop: im=im.crop(crop)
    t=im.info.get('transparency',0); a=np.array(im); p=im.getpalette()
    out=Image.new('RGBA',im.size,bg); px=out.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            if a[y,x]!=t and not (fn.endswith('_gba.png') and a[y,x]==0): px[x,y]=tuple(p[3*a[y,x]:3*a[y,x]+3])+(255,)
    return out
G='../../../../../../graphics/pokemon/'
fs=[('../r9/sprite.png','r9'),('A.png','r11 A'),('B.png','r11 B (hue-shift)')]
pad=12; W=512
vel=Image.new('RGBA',(3*W+4*pad,14+W+pad+14+80+pad+14+256+2*pad),(255,255,255,255)); dr=ImageDraw.Draw(vel)
for k,(f,t) in enumerate(fs):
    dr.text((pad+k*(W+pad),pad-10),t+' 8x',fill=(0,0,0)); vel.paste(rgba(f,L).resize((W,W),Image.NEAREST),(pad+k*(W+pad),pad+4))
y=pad+4+W+pad
dr.text((pad,y),'1x licht / donker: r9, A, B',fill=(0,0,0))
for k,(f,t) in enumerate(fs):
    vel.paste(rgba(f,L),(pad+k*150,y+14)); vel.paste(rgba(f,D),(pad+k*150+70,y+14))
y+=14+80+pad
dr.text((pad,y),'4x: r11 A, r11 B, Golem, Metagross (Gen 3)',fill=(0,0,0))
items=[('A.png',None),('B.png',None),(G+'golem/anim_front_gba.png',(0,0,64,64)),(G+'metagross/anim_front_gba.png',(0,0,64,64))]
for k,(f,c) in enumerate(items): vel.paste(rgba(f,L,c).resize((256,256),Image.NEAREST),(pad+k*(256+pad),y+14))
vel.save('vel.png'); print(vel.size)
