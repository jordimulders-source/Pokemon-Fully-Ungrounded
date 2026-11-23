# kuiven_vel.png: koppen op 8x: r3 | kantel 0 | 0.25 | 0.5 | Gen 3 Mr. Mime
from PIL import Image, ImageDraw
def kop(p,box,pal=None):
    im=Image.open(p).convert('RGBA').crop(box); bg=Image.new('RGB',im.size,(232,240,232)); bg.paste(im,(0,0),im)
    return bg.resize((im.size[0]*8,im.size[1]*8),Image.NEAREST)
mm=Image.open('../../../../../../graphics/pokemon/mr_mime/anim_front_gba.png').crop((0,0,64,64))
pal=[tuple(map(int,l.split())) for l in open('../../../../../../graphics/pokemon/mr_mime/normal_gba.pal').read().split('\n')[3:19]]
m=Image.new('RGBA',(64,64))
for y in range(64):
    for x in range(64):
        i=mm.getpixel((x,y)); m.putpixel((x,y),(0,0,0,0) if i==0 else pal[i]+(255,))
m.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/ace1b272-8fcb-563d-9151-2a564511bb7f/scratchpad/mm_rgba.png')
items=[('r3','../sprite_r3/bokser.png',(18,0,62,22)),('kantel 0','var/kantel_0.png',(18,0,62,22)),('kantel 0.25','var/kantel_0.25.png',(18,0,62,22)),
       ('kantel 0.5','var/kantel_0.5.png',(18,0,62,22)),('Mr. Mime','/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/ace1b272-8fcb-563d-9151-2a564511bb7f/scratchpad/mm_rgba.png',(10,6,54,28))]
ims=[(t,kop(p,b)) for t,p,b in items]
o=Image.new('RGB',(sum(i.size[0]+12 for _,i in ims),ims[0][1].size[1]+20),(255,255,255)); d=ImageDraw.Draw(o); x=0
for t,i in ims: o.paste(i,(x,18)); d.text((x,3),t,fill=(0,0,0)); x+=i.size[0]+12
o.save('kuiven_vel.png')
