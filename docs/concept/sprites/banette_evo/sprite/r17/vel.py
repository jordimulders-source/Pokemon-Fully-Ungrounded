# voor_jordi.png: links r17 op 8x, rechts close-ups 19x van x0-17 y8-34: r16 (oud) | r17 (nieuw)
from PIL import Image, ImageDraw; import numpy as np
def rgb(p):
    im=Image.open(p); a=np.array(im); c=np.array(im.convert('RGB')); c[a==0]=(255,255,255); return Image.fromarray(c)
r16=rgb('../r16/banette_evo.png'); r17=rgb('banette_evo.png')
Z=19; cw,ch=18*Z,27*Z; T=24
W=Image.new('RGB',(512+20+2*(cw+20),max(512,ch)+T+10),(244,244,244)); d=ImageDraw.Draw(W)
W.paste(r17.resize((512,512),0),(0,T)); d.text((4,4),'r17 8x',fill=(0,0,0))
for i,(im,lab) in enumerate(((r16,'r16 (oud)  x0-17 y8-34, 19x'),(r17,'r17 (nieuw)  x0-17 y8-34, 19x'))):
    x0=532+i*(cw+20); W.paste(im.crop((0,8,18,35)).resize((cw,ch),0),(x0,T)); d.text((x0+4,4),lab,fill=(0,0,0))
    for k in range(19): d.line([(x0+k*Z,T),(x0+k*Z,T+ch)],fill=(210,210,210))
    for k in range(28): d.line([(x0,T+k*Z),(x0+cw,T+k*Z)],fill=(210,210,210))
    for k in range(0,18,2): d.text((x0+k*Z+2,T+2),str(k),fill=(200,0,0))
    for k in range(8,35,2): d.text((x0+2,T+(k-8)*Z+2),str(k),fill=(200,0,0))
W.save('voor_jordi.png')
