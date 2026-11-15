# vel.png: v11 | v10a op 8x; 1x/2x op licht en donker; gezicht 12x: v11 | Gengar-gezicht 1,25x (nearest)
from PIL import Image
import os
D=os.path.dirname(os.path.abspath(__file__))+'/'
A=Image.open(D+'gengas_v11.png').convert('RGBA'); B=Image.open(D+'../sprite_v10/gengas_v10a.png').convert('RGBA')
G=Image.open(D+'../../../../../graphics/pokemon/gengar/anim_front.png').convert('RGBA').crop((0,0,64,64))
def op(im,k,s):
    b=Image.new('RGBA',im.size,k); b.alpha_composite(im); return b.resize((im.width*s,im.height*s),Image.NEAREST)
a=op(A,(255,255,255,255),1).crop((6,26,38,50)); a=a.resize((a.width*12,a.height*12),Image.NEAREST)
gz=op(G,(255,255,255,255),1).crop((15,23,40,42)); gz=gz.resize((round(gz.width*1.25),round(gz.height*1.25)),Image.NEAREST)
gz=gz.resize((gz.width*12,gz.height*12),Image.NEAREST)
H=8+512+16+128+16+max(a.height,gz.height)+8
V=Image.new('RGB',(max(16+2*528,16+a.width+16+gz.width+16),H),(235,235,235))
for i,im in enumerate((A,B)): V.paste(op(im,(255,255,255,255),8),(16+i*528,8))
x=16
for k in ((255,255,255,255),(40,40,48,255)):
    for s in (1,2):
        for im in (A,B): V.paste(op(im,k,s),(x,536)); x+=64*s+8
        x+=16
y=536+128+16
V.paste(a,(16,y)); V.paste(gz,(16+a.width+16,y))
V.save(D+'vel.png'); print('vel.png')
