# view.py IN.png OUT.png : sprite 8x | model (natief, zelfde schaal, BOX naar 64) 8x
import sys,numpy as np
from PIL import Image
f=59/75; X0,Y0,OX,OY=17,16,2,6
src=Image.open('../model/model_gekozen_natief.png').convert('RGB')
# modelcoördinaat van spritepixel 0: X0-OX/f
x0=X0-OX/f; y0=Y0-OY/f; k=1/f
big=src.resize((990,990),Image.NEAREST)
m=big.crop((int(x0*10),int(y0*10),int((x0+64*k)*10),int((y0+64*k)*10))).resize((64,64),Image.BOX)
def rgba(path):
    p=Image.open(path); p.save('/tmp/claude-0/sat/_v.png',transparency=0); return Image.open('/tmp/claude-0/sat/_v.png').convert('RGBA')
s=rgba(sys.argv[1]); bg=Image.new('RGBA',(64,64),(152,208,160,255)); bg.alpha_composite(s)
Z=8; o=Image.new('RGB',(64*Z*2+8,64*Z),'white')
o.paste(bg.convert('RGB').resize((512,512),Image.NEAREST),(0,0)); o.paste(m.resize((512,512),Image.NEAREST),(520,0))
o.save(sys.argv[2])
