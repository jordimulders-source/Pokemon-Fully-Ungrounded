# Levert welp_r9.png (64x64 indexed, index 0 transparant), _8x en vel.png (r7 | r6 | model op 8x, kop 12x, 1x naast Growlithe/Vulpix)
import numpy as np
from PIL import Image, ImageDraw
from toon6 import big
F7=np.load('FIN7.npy'); F6=np.load('FIN7.npy'); a=np.load('welp_r9.npy'); r6=np.load('welp_r8.npy')
def png64(a,F,fn):
    h,w=a.shape; full=np.zeros((64,64),'uint8'); x0=(64-w)//2; full[63-h:63,x0:x0+w]=a
    p=Image.fromarray(full,'P'); pal=[255,0,255]+[int(v) for c in F[1:] for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(fn,transparency=0)
png64(a,F7,'welp_r9.png'); png64(r6,F6,'/tmp/claude-0/_r8.png')
big(a,8,F7,(255,255,255,255)).save('welp_r9_8x.png')
q=Image.open('welp_r9.png'); print(q.mode,q.size,'kleuren',len(set(np.array(q).ravel())))
SRC='../../referenties/model_welp_gekozen.png'; k=16.896; m=Image.open(SRC).convert('RGBA')
mod=lambda b,z: m.crop((int(99.3+b[0]*k),int(191.5+b[1]*k),int(99.3+b[2]*k),int(191.5+b[3]*k))).resize(((b[2]-b[0])*z,(b[3]-b[1])*z),Image.LANCZOS)
row1=[(big(a,8,F7),'r9'),(big(r6,8,F6),'r8'),(mod((0,0,50,45),8),'model')]
row2=[(big(a[0:24,0:25],12,F7),'kop r9'),(big(r6[0:24,0:25],12,F6),'kop r8'),(mod((0,0,25,24),12),'kop model')]
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
refs=[Image.open(G+f'{kk}/anim_front_gba.png').convert('RGBA').crop((0,0,64,64)) for kk in ('growlithe','vulpix')]
w7=Image.open('welp_r9.png').convert('RGBA'); w6=Image.open('/tmp/claude-0/_r8.png').convert('RGBA')
V=Image.new('RGBA',(3*420,18+360+30+288+30+64*2+40),(255,255,255,255)); d=ImageDraw.Draw(V); x=0
for im,l in row1: V.alpha_composite(im,(x,18)); d.text((x,3),l,fill=(0,0,0)); x+=420
x=0; y=18+360+28
for im,l in row2: V.alpha_composite(im,(x,y)); d.text((x,y-14),l,fill=(0,0,0)); x+=420
y+=288+28; d.text((0,y-14),'1x: Growlithe | r9 | Vulpix | r8 (licht en donker), en 2x',fill=(0,0,0)); x=0
for bg in ((248,248,240,255),(40,44,52,255)):
    for im in (refs[0],w7,refs[1],w6):
        t=Image.new('RGBA',(64,64),bg); t.alpha_composite(im); V.alpha_composite(t,(x,y)); x+=70
    x+=16
for im in (refs[0],w7,refs[1]):
    t=Image.new('RGBA',(64,64),(248,248,240,255)); t.alpha_composite(im); V.alpha_composite(t.resize((128,128),Image.NEAREST),(x,y)); x+=134
V.save('vel.png'); print(V.size)
