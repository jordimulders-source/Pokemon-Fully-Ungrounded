# Vel ronde 5: r5 | r4 | model A3 op 8x; 1x op licht en donker naast de impala
from PIL import Image, ImageDraw
import tempfile; S=tempfile.gettempdir()+'/'
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.save(S+'_v.png',transparency=0); im=Image.open(S+'_v.png')
    return im.convert('RGBA')
# vel: r4 | r3 | model, 8x; 1x op licht en donker naast de impala
Z=512; V=Image.new('RGBA',(3*(Z+10),Z+40+170),(255,255,255,255)); d=ImageDraw.Draw(V)
r5=rgba('r5/kudu_r5.png'); r4=rgba('r4/kudu_r4.png'); imp=rgba('../../impala/af/impala.png')
mm=Image.open('r3/model_A3.png').convert('RGBA').crop((91-6*16,0,91-6*16+1024,1024)).resize((Z,Z),Image.LANCZOS)
for i,(t,im) in enumerate([('r5 8x (oog B, wisselen: python3 r5.py A|B|C|D)',r5),('r4 8x',r4)]):
    b=im.resize((Z,Z),Image.NEAREST); V.paste(b,(i*(Z+10),20),b); d.text((i*(Z+10),4),t,fill=(0,0,0))
V.paste(mm,(2*(Z+10),20)); d.text((2*(Z+10),4),'model A3 verkleind',fill=(0,0,0))
y=Z+50
for j,bg in enumerate([(255,255,255,255),(40,44,52,255)]):
    x=j*320; V.paste(Image.new('RGBA',(300,150),bg),(x,y))
    for k,im in enumerate([r5,r4,imp]): V.paste(im,(x+10+k*95,y+40),im)
d.text((0,y-14),'1x op licht en donker: r5 | r4 | impala (af)',fill=(0,0,0))
V.save('r5/vel.png'); print('ok')
