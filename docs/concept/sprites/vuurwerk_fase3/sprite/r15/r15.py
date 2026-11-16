# Jordi (16 nov): "ik heb hier puntjes op 3 potentiele pixels gezet die mogen veranderen, de rest blijft hetzelfde"
# Puntjes (referenties/jordi_linkeroog_puntjes.png, gemeten): (4,22), (4,23), (5,24). Basis r12 p2 (spikkels B).
from PIL import Image, ImageDraw
import numpy as np
src=Image.open('../r12/sprite_B_p2.png'); a0=np.array(src); pal=src.getpalette()
B,G,Z,T,C4,C5=2,13,1,3,4,5   # bruin, geel, pupil, tan, creme-midden, creme-licht
V={ # (4,22),(4,23),(5,24)
 '1':(B,B,B),'2':(B,B,C5),'3':(C4,B,B),'4':(G,B,B),'5':(B,C4,B),'6':(T,B,B),'7':(G,Z,B),'8':(B,Z,B)}
outs=[]
for k,(p1,p2,p3) in V.items():
    a=a0.copy(); a[22,4]=p1; a[23,4]=p2; a[24,5]=p3
    d=np.argwhere(a!=a0); assert all(tuple(x) in [(22,4),(23,4),(24,5)] for x in d)
    im=Image.fromarray(a,'P'); im.putpalette(pal); im.info.update(src.info); im.save(f'sprite_{k}.png', transparency=src.info.get('transparency',0)); outs.append((k,im))
outs.append(('r12 p2',src))
S=12; cw,ch=26*S,30*S
W=Image.new('RGB',(16+len(outs)*(cw+12),ch+64+150),(235,235,235)); d=ImageDraw.Draw(W)
for i,(k,im) in enumerate(outs):
    rgba=(Image.open(f'sprite_{k}.png') if k!='r12 p2' else im).convert('RGBA'); bg=Image.new('RGBA',rgba.size,(255,255,255,255)); bg.alpha_composite(rgba)
    crop=bg.crop((0,4,26,34)).resize((cw,ch),Image.NEAREST); x=16+i*(cw+12)
    W.paste(crop.convert('RGB'),(x,24)); d.text((x,6),k,fill=(0,0,0))
    W.paste(bg.convert('RGB').resize((128,128),Image.NEAREST),(x,ch+40))
W.save('vel.png')
