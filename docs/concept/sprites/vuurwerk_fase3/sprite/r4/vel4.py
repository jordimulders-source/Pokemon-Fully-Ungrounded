# vel.png r4: (1) kop 8x: r4 | r3 | model hoge resolutie; (2) hele sprite 8x: r4 | r3 | model BOX->64;
# (3) 1x op wit/creme/donker/groen (r4, r3, model); (4) modelomtrek (blauw) over de r4-kop op 12x.
import numpy as np; from PIL import Image, ImageDraw
def rgba(f):
    s=Image.open(f); s.save('/tmp/_v4.png',transparency=0); return Image.open('/tmp/_v4.png').convert('RGBA')
def op(im,c): b=Image.new('RGBA',im.size,c); b.alpha_composite(im); return b.convert('RGB')
r4=rgba('sprite.png'); r3=rgba('../r3/sprite.png')
M=Image.open('../../referenties/model_v14.png').convert('RGB'); MB=M.crop((106,120,874,888)); m64=MB.resize((64,64),Image.BOX).convert('RGBA')
fg=np.load('model_fg.npz')['fg']
KW,KH=26,31; Z=8
W=3*KW*Z+60; vel=Image.new('RGB',(max(W,3*512+60),40+KH*Z+40+512+40+90+40+KH*12+20),(232,232,232)); d=ImageDraw.Draw(vel)
y=10; d.text((20,y),'1. kop 8x: r4 | r3 | model (hoge resolutie)',fill=0); y+=16
for i,im in enumerate([op(r4,(255,255,255,255)).crop((0,0,KW,KH)).resize((KW*Z,KH*Z),Image.NEAREST),
                       op(r3,(255,255,255,255)).crop((0,0,KW,KH)).resize((KW*Z,KH*Z),Image.NEAREST),
                       M.crop((106,120,106+KW*12,120+KH*12)).resize((KW*Z,KH*Z),Image.LANCZOS)]):
    vel.paste(im,(20+i*(KW*Z+20),y))
y+=KH*Z+24; d.text((20,y),'2. hele sprite 8x: r4 | r3 | model BOX->64',fill=0); y+=16
for i,im in enumerate([r4,r3,m64]): vel.paste(op(im,(255,255,255,255)).resize((512,512),Image.NEAREST),(20+i*532,y))
y+=512+24; d.text((20,y),'3. 1x op wit / creme / donker / groen: r4, r3, model',fill=0); y+=16
for i,c in enumerate([(255,255,255,255),(248,240,220,255),(40,40,48,255),(90,140,90,255)]):
    for j,im in enumerate((r4,r3,m64)):
        b=op(im,c); vel.paste(b,(20+i*220+j*68,y))
y+=90; d.text((20,y),'4. modelomtrek (blauw, dekking van het model) over de r4-kop op 12x',fill=0); y+=16
ov=op(r4,(255,255,255,255)).crop((0,0,KW,KH)).resize((KW*12,KH*12),Image.NEAREST); px=ov.load()
f2=fg[120:120+KH*12,106:106+KW*12]; e=(f2^np.roll(f2,1,0))|(f2^np.roll(f2,1,1))
for yy,xx in zip(*np.where(e)): px[int(xx),int(yy)]=(0,90,255)
vel.paste(ov,(20,y))
vel.paste(M.crop((106,120,106+KW*12,120+KH*12)),(40+KW*12,y))
vel.save('vel.png'); print(vel.size)
