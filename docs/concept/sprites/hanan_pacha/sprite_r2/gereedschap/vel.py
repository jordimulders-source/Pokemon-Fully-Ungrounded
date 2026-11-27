# vel.png: rij 1 k120 | k135 | k150 (8x); rij 2 r1 (8x) | r7 | r5; rij 3: varianten 1x en 2x op licht en donker
import sys,numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); from gemeen import *; from reduceer import s2o
F=8; W=64*F; G=16
def sp(f,bg=(248,248,248),s=F):
    o=np.array(Image.open(f)); return Image.fromarray(rgb(o,bg)).resize((64*s,64*s),Image.NEAREST)
m7=Image.open('../gemini/r7.png').convert('RGB'); x0,y0=s2o(0,0); x1,y1=s2o(64,64)
m7=m7.crop((int(x0),int(y0),int(x1),int(y1))).resize((W,W),Image.LANCZOS)
m5=Image.open('../gemini/r5.png').convert('RGB'); m5=m5.resize((W,int(768*W/1408)),Image.LANCZOS)
V=Image.new('RGB',(3*W+2*G,2*W+3*G+300),'white'); d=ImageDraw.Draw(V)
for i,(f,t) in enumerate((('sprite_k120.png','r2 kop x1,20 (oog Spearow)'),('sprite_k135.png','r2 kop x1,35 (oog Pidgeot)'),('sprite_k150.png','r2 kop x1,50 (oog Pidgeot)'))):
    V.paste(sp(f),(i*(W+G),G)); d.text((i*(W+G)+4,2),t,fill=(0,0,0))
y=W+2*G
V.paste(sp('r1.png'),(0,y)); d.text((4,y-14),'r1',fill=(0,0,0))
V.paste(m7,(W+G,y)); d.text((W+G+4,y-14),'model r7 (zelfde schaal als r1)',fill=(0,0,0))
V.paste(m5,(2*(W+G),y+(W-m5.height)//2)); d.text((2*(W+G)+4,y-14),'r5 (staart, kleurbron)',fill=(0,0,0))
y=2*W+3*G; x=0
for f in ('sprite_k120.png','sprite_k135.png','sprite_k150.png'):
    for bg in ((248,248,248),(40,40,56)):
        for s in (1,2):
            V.paste(Image.new('RGB',(64*s+12,140),bg),(x,y)); V.paste(sp(f,bg,s),(x+6,y+6)); x+=64*s+16
    x+=12
V=V.crop((0,0,max(3*W+2*G,x),y+150)); V.save('vel.png')
