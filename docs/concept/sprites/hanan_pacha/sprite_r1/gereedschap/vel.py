# vel.png: sprite 8x | r7 op dezelfde schaal | r5 (kleurbron) op vergelijkbare maat / 1x op licht en donker (ook 2x)
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *
sp=sys.argv[1]; out=sys.argv[2]
o=np.array(Image.open(sp)); F=8; W=64*F
s8=Image.fromarray(rgb(o,(248,248,248))).resize((W,W),Image.NEAREST)
def o_(n): return 0.1+6.4*n
m7=Image.open('../gemini/r7.png').convert('RGB')
x0=o_(NX0-OX/S); y0=o_(NY0-OY/S); x1=o_(NX0+(64-OX)/S); y1=o_(NY0+64/S)
m7=m7.crop((int(x0),int(y0),int(x1),int(y1))).resize((W,W),Image.LANCZOS)
m5=Image.open('../gemini/r5.png').convert('RGB'); m5=m5.crop((0,0,1408,768)); r=W/1408; m5=m5.resize((W,int(768*r)),Image.LANCZOS)
V=Image.new('RGB',(W*3+40,W+220),(255,255,255)); d=ImageDraw.Draw(V)
V.paste(s8,(0,20)); V.paste(m7,(W+20,20)); V.paste(m5,(2*W+40,20+(W-m5.height)//2))
d.text((4,4),'sprite r1 (8x)',fill=(0,0,0)); d.text((W+24,4),'model r7 (zelfde schaal)',fill=(0,0,0)); d.text((2*W+44,4),'r5 (kleurbron)',fill=(0,0,0))
x=0
for bg in ((248,248,248),(232,224,200),(40,40,56),(0,0,0)):
    for f in (1,2):
        im=Image.fromarray(rgb(o,bg)).resize((64*f,64*f),Image.NEAREST)
        V.paste(Image.new('RGB',(64*f+16,64*2+16),bg),(x,W+40)); V.paste(im,(x+8,W+48)); x+=64*f+24
V.save(out)
