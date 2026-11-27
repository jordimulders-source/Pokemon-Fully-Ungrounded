import numpy as np
from PIL import Image,ImageDraw
nat=np.load('comp_nat.npy').astype('uint8')
m=Image.fromarray(nat[52:63,16:29]).resize((13*8+4,11*8+4),Image.NEAREST)
def S(f,bgc=(255,255,255,255)):
    sp=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',(64,64),bgc); bg.alpha_composite(sp); return bg.convert('RGB')
A=S('r5_A.png'); B=S('r5_B.png')
o=Image.new('RGB',(560,330),(235,235,235)); d=ImageDraw.Draw(o)
x=6
for lbl,im in [('model natief',m),('A: grijs 10 (46,46,48)',A.crop((9,38,18,46)).resize((108,96),Image.NEAREST)),('B: bruin 5 (90,71,62)',B.crop((9,38,18,46)).resize((108,96),Image.NEAREST))]:
    d.text((x,4),lbl,fill=0); o.paste(im,(x,18)); x+=150
d.text((6,130),'A 2x / 1x',fill=0); o.paste(A.resize((128,128),Image.NEAREST),(6,144)); o.paste(A,(140,144)); o.paste(S('r5_A.png',(40,44,52,255)),(140,214))
d.text((280,130),'B 2x / 1x',fill=0); o.paste(B.resize((128,128),Image.NEAREST),(280,144)); o.paste(B,(414,144)); o.paste(S('r5_B.png',(40,44,52,255)),(414,214))
o.save('vel_r5.png')
