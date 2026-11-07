# Jordi 7 nov: 4 rood gestipte pixels (haarsliert linksboven) helemaal weg; "dan is die klaar".
import numpy as np; from PIL import Image
im=Image.open('../eind_r4/potoo.png'); a=np.array(im); pal=im.getpalette()
for x,y in ((24,0),(25,0),(23,1),(23,2)):
    assert a[y,x]==4,(x,y,a[y,x]); a[y,x]=0
o=Image.fromarray(a,'P'); o.putpalette(pal); o.save('potoo.png',transparency=0)
rgb=Image.new('RGBA',(64,64),(255,255,255,255)); rgb.alpha_composite(o.convert('RGBA')); rgb.resize((512,512),Image.NEAREST).convert('RGB').save('potoo_8x.png')
