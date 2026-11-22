# vel_ogen.py: koppen 12x (r1 | A | B | C) en hele sprites 4x, plus 1x op licht/donker
import sys; sys.path.insert(0,'gereedschap'); from gemeen import *; from PIL import Image, ImageDraw
P=[('r1','sprite_r1/kricketune_evo_r1.png')]+[(n,'sprite_r2/oog_%s.png'%n) for n in 'ABC']
x0,y0,x1,y1=18,4,46,24; z=12; bw=(x1-x0)*z
W=Image.new('RGB',(len(P)*(bw+12),16+(y1-y0)*z+16+256+16+70),'white'); d=ImageDraw.Draw(W)
for i,(n,p) in enumerate(P):
    o=laden(p); X=i*(bw+12)
    W.paste(rgb(o,(255,255,255)).crop((x0,y0,x1,y1)).resize((bw,(y1-y0)*z),Image.NEAREST),(X,16)); d.text((X+2,2),n+' kop 12x',fill=(0,0,0))
    W.paste(rgb(o,(255,255,255)).resize((256,256),Image.NEAREST),(X,32+(y1-y0)*z))
    for j,bg in enumerate([(232,232,216),(40,48,56)]): W.paste(rgb(o,bg),(X+j*70,48+(y1-y0)*z+256))
W.save('sprite_r2/vel.png'); print(W.size)
