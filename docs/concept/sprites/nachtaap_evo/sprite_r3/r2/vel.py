# vel.png: r2 8x | r1 8x | oude sprite 8x ; lijf 12x r2 | r1 ; 1x en 2x op licht en donker
import sys; sys.path.insert(0,'r1'); from pal import *
from PIL import ImageDraw
g=np.array(Image.open('r2/anim_front.png'))[:64].astype(int); r=np.array(Image.open('r1/anim_front.png'))[:64].astype(int)
o=np.array(Image.open('referenties/oude_sprite.png')).astype(int); W=(255,255,255)
ims=[naar_img(x[6:64,0:63],8,W).convert('RGB') for x in (g,r,o)]
l=[naar_img(x[26:60,22:50],12,W).convert('RGB') for x in (g,r)]
V=Image.new('RGB',(ims[0].width*3+40,ims[0].height+l[0].height+60),(225,225,225)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate(zip(ims,('r2 (8x)','r1 (8x)','oude sprite (8x)'))): V.paste(im,(i*(im.width+20),20)); d.text((i*(im.width+20)+4,4),t,fill=(0,0,0))
yk=ims[0].height+44; d.text((4,yk-16),'lijf 12x: r2 | r1',fill=(0,0,0))
for i,im in enumerate(l): V.paste(im,(i*(im.width+16),yk))
x=2*(l[0].width+16)+30
for bg in ((248,248,248),(40,40,48)):
    for k,q in enumerate((g,o)):
        V.paste(naar_img(q,1,bg).convert('RGB'),(x+k*70,yk)); V.paste(naar_img(q,2,bg).convert('RGB'),(x,yk+80+k*140))
    x+=200
d.text((2*(l[0].width+16)+30,yk-16),'1x: r2, oud | 2x: r2 (boven), oud (onder); licht en donker',fill=(0,0,0))
V.save('r2/vel.png'); print(V.size)
