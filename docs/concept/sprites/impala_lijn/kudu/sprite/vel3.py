# Vel ronde 3 + oogvarianten
from PIL import Image, ImageDraw
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.save('/tmp/_v.png',transparency=0); im=Image.open('/tmp/_v.png')
    return im.convert('RGBA')
# oogvarianten: alleen het hoofd (spritex 6..32, y 14..32) op 8x
V=Image.new('RGBA',(3*(26*8+20)+20,18*8+40),(255,255,255,255)); d=ImageDraw.Draw(V)
for i,(f,t) in enumerate([('r3/kudu_r3.png','a: oog impala (af, B3) 1-op-1, omgekleurd'),('r3/kudu_r3_oogb.png','b: oog Stantler (_gba) 1-op-1, omgekleurd'),('r3/kudu_r3_oogc.png','c: modeloog met lid (half dicht)')]):
    s=rgba(f).crop((6,14,32,32)).resize((26*8,18*8),Image.NEAREST); x=10+i*(26*8+20)
    V.paste(s,(x,30),s); d.text((x,8),t,fill=(0,0,0,255))
V.save('r3/oog_varianten.png')
S=512; V=Image.new('RGBA',(3*(S+10)+200,S+40+170),(255,255,255,255)); d=ImageDraw.Draw(V)
r3=rgba('r3/kudu_r3.png'); r2=rgba('r2/kudu_r2.png'); imp=rgba('../../impala/af/impala.png')
m=Image.open('r3/model_A3.png').convert('RGBA').crop((91-6*16,0,91-6*16+1024,1024)).resize((S,S),Image.LANCZOS)
for i,(t,im) in enumerate([('r3 8x',r3),('r2 8x',r2)]):
    b=im.resize((S,S),Image.NEAREST); V.paste(b,(i*(S+10),20),b); d.text((i*(S+10),4),t,fill=(0,0,0,255))
V.paste(m,(2*(S+10),20)); d.text((2*(S+10),4),'model A3 (manen hersteld) verkleind',fill=(0,0,0,255))
y=S+50
for j,bg in enumerate([(255,255,255,255),(40,44,52,255)]):
    x=j*320; V.paste(Image.new('RGBA',(300,150),bg),(x,y))
    for k,im in enumerate([r3,r2,imp]): V.paste(im,(x+10+k*95,y+40),im)
d.text((0,y-14),'1x op licht en donker: r3 | r2 | impala (af)',fill=(0,0,0,255))
b=imp.resize((192,192),Image.NEAREST); V.paste(b,(3*(S+10),20),b); d.text((3*(S+10),4),'impala af 3x',fill=(0,0,0,255))
V.save('r3/vel.png'); print('ok')
