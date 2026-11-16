# r7 = r6b met een iets fellere lichtrand (alleen palet index 7 en 8); indexkaart identiek.
import sys; sys.path.insert(0,'sprite_r1'); import numpy as np, colorsys; from PIL import Image, ImageDraw; from render import img
r6b=Image.open('sprite_r6/dustly_r6b.png'); o=np.asarray(r6b).astype('uint8'); P6=r6b.getpalette()[:33]; P6=[tuple(P6[i:i+3]) for i in range(0,33,3)]
P7=list(P6); P7[7]=(232,96,122); P7[8]=(255,196,148)
hs=lambda c: tuple(round(v,2) for v in colorsys.rgb_to_hsv(*[q/255 for q in c]))
for i in (7,8): print(i,P6[i],'->',P7[i],'hsv',hs(P6[i]),'->',hs(P7[i]))
p=Image.fromarray(o,'P'); fl=[v for c in P7 for v in c]; p.putpalette(fl+[0]*(768-len(fl))); p.save('sprite_r7/dustly_r7.png',transparency=0)
q=np.asarray(Image.open('sprite_r7/dustly_r7.png')); print('index-diff t.o.v. r6b',int((q!=o).sum()))
img(o,P7,8).save('sprite_r7/dustly_r7_8x.png')
L,D=(248,248,240),(40,40,48)
out=Image.new('RGB',(2*512+48,24+512+24+140),(255,255,255)); d=ImageDraw.Draw(out)
for i,(P,n) in enumerate(((P6,'r6b'),(P7,'r7'))): out.paste(img(o,P,8,L).convert('RGB'),(16+i*528,24)); d.text((16+i*528,6),n,fill=(0,0,0))
x=16; y=560
for P in (P6,P7):
    for bg in (L,D):
        for s in (1,2): c=img(o,P,s,bg).convert('RGB'); out.paste(c,(x,y)); x+=c.width+8
    x+=24
out.save('sprite_r7/vel.png')
