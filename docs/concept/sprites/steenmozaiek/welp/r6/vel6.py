# vel: r6 | r5 | r3 | model op 8x; kop op 12x; 1x tussen Growlithe en Vulpix (licht en donker).
import sys,numpy as np
from PIL import Image, ImageDraw
from toon6 import big, rgba
F6=np.load('FIN6.npy'); F2=np.load('FIN2.npy')
nm=sys.argv[1] if len(sys.argv)>1 else 'welp_r6.npy'; out=sys.argv[2] if len(sys.argv)>2 else 'vel.png'
r6=np.load(nm); r5=np.load('welp_r5.npy'); r3=np.load('welp_r3_A_oog1.npy')
SRC='../../referenties/model_welp_gekozen.png'; k=16.896
m=Image.open(SRC).convert('RGBA')
def mod(box,z):
    return m.crop((int(99.3+box[0]*k),int(191.5+box[1]*k),int(99.3+box[2]*k),int(191.5+box[3]*k))).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.LANCZOS)
row1=[(big(r6,8,F6),'r6'),(big(r5,8,F2),'r5'),(big(r3,8,F2),'r3'),(mod((0,0,50,45),8),'model')]
box=(0,0,25,24)
row2=[(big(r6[0:24,0:25],12,F6),'kop r6'),(big(r5[0:24,0:25],12,F2),'kop r5'),(big(r3[0:24,0:25],12,F2),'kop r3'),(mod(box,12),'kop model')]
def png64(a,FIN):
    h,w=a.shape; full=np.zeros((64,64),'uint8'); x0=(64-w)//2; full[63-h:63,x0:x0+w]=a
    p=Image.fromarray(full,'P'); pal=[255,0,255]+[int(v) for c in FIN[1:] for v in c]; p.putpalette(pal+[0]*(768-len(pal))); return p
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
refs=[Image.open(G+f'{kk}/anim_front_gba.png').convert('RGBA').crop((0,0,64,64)) for kk in ('growlithe','vulpix')]
p6=png64(r6,F6); p6.save('/tmp/claude-0/_p6.png',transparency=0); w6=Image.open('/tmp/claude-0/_p6.png').convert('RGBA')
p5=png64(r5,F2); p5.save('/tmp/claude-0/_p5.png',transparency=0); w5=Image.open('/tmp/claude-0/_p5.png').convert('RGBA')
Wd=sum(i.width+20 for i,_ in row1)
V=Image.new('RGBA',(Wd,18+360+30+288+30+64*2+40),(255,255,255,255)); d=ImageDraw.Draw(V); x=0
for im,l in row1: V.alpha_composite(im,(x,18)); d.text((x,3),l,fill=(0,0,0)); x+=im.width+20
x=0; y=18+360+28
for im,l in row2: V.alpha_composite(im,(x,y)); d.text((x,y-14),l,fill=(0,0,0)); x+=im.width+20
y+=288+28; d.text((0,y-14),'1x: Growlithe | r6 | Vulpix | r5   (licht en donker), en 2x',fill=(0,0,0)); x=0
for bg in ((248,248,240,255),(40,44,52,255)):
    for im in (refs[0],w6,refs[1],w5):
        t=Image.new('RGBA',(64,64),bg); t.alpha_composite(im); V.alpha_composite(t,(x,y)); x+=70
    x+=16
for im in (refs[0],w6,refs[1]):
    t=Image.new('RGBA',(64,64),(248,248,240,255)); t.alpha_composite(im); V.alpha_composite(t.resize((128,128),Image.NEAREST),(x,y)); x+=134
V.save(out); print(V.size)
