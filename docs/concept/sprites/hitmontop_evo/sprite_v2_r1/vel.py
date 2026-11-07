# Vel: 8x werk naast Hitmontop en Hitmonlee, 1x (licht/donker), close-ups 16x.
import sys
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'
sp=Image.open(sys.argv[1]).convert('RGB')
uit=sys.argv[2]
top=Image.open(R+'graphics/pokemon/hitmontop/anim_front.png').crop((0,0,64,64)).convert('RGB')
lee=Image.open(R+'graphics/pokemon/hitmonlee/anim_front.png').crop((0,0,64,64)).convert('RGB')
W=Image.new('RGB',(3*530+10,620+330),(235,235,240)); d=ImageDraw.Draw(W)
for i,(n,im) in enumerate([('WERK',sp),('hitmontop',top),('hitmonlee',lee)]):
    W.paste(im.resize((512,512),Image.NEAREST),(10+i*530,20)); d.text((10+i*530,5),n+' 8x',fill='black')
    W.paste(im,(10+i*530,540))
    dk=Image.new('RGB',(64,64),(40,40,48)); px=im.load()
    m=Image.new('L',(64,64),0); mp=m.load()
    for y in range(64):
        for x in range(64):
            if px[x,y]!=(152,208,160): mp[x,y]=255
    dk.paste(im,(0,0),m); W.paste(dk,(80+i*530,540))
    W.paste(im.resize((128,128),Image.NEAREST),(150+i*530,540))
for j,box in enumerate([(4,14,36,46),(24,0,64,32)]):
    c=sp.crop(box); W.paste(c.resize((c.width*10,c.height*10),Image.NEAREST),(10+j*560,620))
W.save(uit)
