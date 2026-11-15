# gengas_v9_8x.png (alleen de sprite, 8x op wit) en vel.png: v9 | v8b op 8x en 1x/2x (licht en donker)
from PIL import Image
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
def rgba(p): return Image.open(p).convert('RGBA')
A=rgba(D+'gengas_v9.png'); B=rgba(D+'../sprite_v8/gengas_v8b.png')
def op(im,k,s):
    b=Image.new('RGBA',im.size,k); b.alpha_composite(im); return b.resize((64*s,64*s),Image.NEAREST)
op(A,(255,255,255,255),8).convert('RGB').save(D+'gengas_v9_8x.png')
V=Image.new('RGB',(16+2*528,540+150),(235,235,235))
for i,im in enumerate((A,B)): V.paste(op(im,(255,255,255,255),8),(16+i*528,8))
x=16
for k in ((255,255,255,255),(40,40,48,255)):
    for s in (1,2):
        for im in (A,B): V.paste(op(im,k,s),(x,540)); x+=64*s+8
        x+=16
V.save(D+'vel.png'); print('vel.png')
