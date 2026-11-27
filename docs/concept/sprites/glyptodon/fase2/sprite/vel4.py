# vel_r4: model-oog natief (8x, zelfde fysieke maat als 12x sprite) | r4-oog 12x | Rhydon, Golem, Tauros oog 12x | r4 2x en 1x
import numpy as np
from PIL import Image,ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def ref(nm,box):
    im=Image.open(G+nm+'/anim_front_gba.png').convert('RGB').crop((0,0,64,64)); return im.crop(box)
nat=np.load('comp_nat.npy').astype('uint8')
m=Image.fromarray(nat[52:63,16:29]).resize((13*8+4,11*8+4),Image.NEAREST)   # natief x16-28 y52-62 ~ sprite x9-17 y38-45
sp=Image.open('r4.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(sp); S=bg.convert('RGB')
r4o=S.crop((9,38,18,46)).resize((9*12,8*12),Image.NEAREST)
refs=[('rhydon',(21,23,30,31)),('golem',(27,29,36,37)),('tauros',(21,28,30,36))]
H=380; o=Image.new('RGB',(1200,H),(235,235,235)); d=ImageDraw.Draw(o)
x=6
for lbl,im in [('model natief (x16-28,y52-62)',m),('r4 oog (x9-17,y38-45) 12x',r4o)]+[(n+' 12x',ref(n,b).resize(((b[2]-b[0])*12,(b[3]-b[1])*12),Image.NEAREST)) for n,b in refs]:
    d.text((x,4),lbl,fill=0); o.paste(im,(x,18)); x+=max(im.width+14,len(lbl)*6+8)
d.text((6,140),'r4 2x',fill=0); o.paste(S.resize((128,128),Image.NEAREST),(6,154))
d.text((150,140),'r4 1x',fill=0); o.paste(S,(150,154))
dk=Image.new('RGBA',(64,64),(40,44,52,255)); dk.alpha_composite(sp); o.paste(dk.convert('RGB'),(230,154))
o=o.crop((0,0,max(x,300),300)); o.save('vel_r4.png')
