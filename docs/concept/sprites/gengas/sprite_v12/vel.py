# vel.png: v12 | v11 op 8x; 1x/2x op licht en donker
from PIL import Image
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
ims=[Image.open(D+p).convert('RGBA') for p in ('gengas_v12.png','../sprite_v11/gengas_v11.png')]
def op(im,k,s):
    b=Image.new('RGBA',im.size,k); b.alpha_composite(im); return b.resize((64*s,64*s),Image.NEAREST)
V=Image.new('RGB',(16+2*528,540+150),(235,235,235))
for i,im in enumerate(ims): V.paste(op(im,(255,255,255,255),8),(16+i*528,8))
x=16
for k in ((255,255,255,255),(40,40,48,255)):
    for s in (1,2):
        for im in ims: V.paste(op(im,k,s),(x,540)); x+=64*s+8
        x+=16
V.save(D+'vel.png'); print('vel.png')
