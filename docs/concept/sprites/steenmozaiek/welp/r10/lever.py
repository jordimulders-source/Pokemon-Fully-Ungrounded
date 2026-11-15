# Levert welp_r10.png (64x64 indexed, index 0 transparant), _8x, vel.png (r10 | r9 | model op 8x, kop 12x, 1x licht/donker naast Growlithe/Vulpix)
# en ver_oog.png (varianten ver oog op 12x naast het model).
import numpy as np, subprocess
from PIL import Image, ImageDraw
from toon6 import big
from zie import mod
F10=np.load('FIN10.npy'); F7=np.load('FIN7.npy'); a=np.load('welp_r10.npy'); r9=np.load('../r9/welp_r9.npy')
def png64(a,F,fn):
    h,w=a.shape; full=np.zeros((64,64),'uint8'); x0=(64-w)//2; full[63-h:63,x0:x0+w]=a
    p=Image.fromarray(full,'P'); pal=[255,0,255]+[int(v) for c in F[1:] for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(fn,transparency=0)
png64(a,F10,'welp_r10.png'); png64(r9,F7,'_r9.png')
big(a,8,F10,(255,255,255,255)).save('welp_r10_8x.png')
q=Image.open('welp_r10.png'); print(q.mode,q.size,'kleuren',len(set(np.array(q).ravel())))
row1=[(big(a,8,F10),'r10'),(big(r9,8,F7),'r9'),(mod((0,0,50,45),8),'model')]
row2=[(big(a[0:24,0:25],12,F10),'kop r10'),(big(r9[0:24,0:25],12,F7),'kop r9'),(mod((0,0,25,24),12),'kop model')]
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
refs=[Image.open(G+f'{kk}/anim_front_gba.png').convert('RGBA').crop((0,0,64,64)) for kk in ('growlithe','vulpix')]
w10=Image.open('welp_r10.png').convert('RGBA'); w9=Image.open('_r9.png').convert('RGBA')
V=Image.new('RGBA',(3*420,18+360+30+288+30+64*2+40),(255,255,255,255)); d=ImageDraw.Draw(V); x=0
for im,l in row1: V.alpha_composite(im,(x,18)); d.text((x,3),l,fill=(0,0,0)); x+=420
x=0; y=18+360+28
for im,l in row2: V.alpha_composite(im,(x,y)); d.text((x,y-14),l,fill=(0,0,0)); x+=420
y+=288+28; d.text((0,y-14),'1x: Growlithe | r10 | Vulpix | r9 (licht en donker), en 2x',fill=(0,0,0)); x=0
for bg in ((248,248,240,255),(40,44,52,255)):
    for im in (refs[0],w10,refs[1],w9):
        t=Image.new('RGBA',(64,64),bg); t.alpha_composite(im); V.alpha_composite(t,(x,y)); x+=70
    x+=16
for im in (refs[0],w10,refs[1]):
    t=Image.new('RGBA',(64,64),(248,248,240,255)); t.alpha_composite(im); V.alpha_composite(t.resize((128,128),Image.NEAREST),(x,y)); x+=134
V.save('vel.png'); print(V.size)
# ver oog: varianten
names=[('A','A: wit op de contour (model)'),('B','B: Growlithe/Vulpix (GEKOZEN)'),('C','C: Vulpix 1 breed')]
ims=[]
for v,l in names:
    subprocess.run(['python3','r10.py','band=B3','ver='+v,'oog=E9','tong=6','snuit=L','punt=1'],check=True,capture_output=True)
    ims.append((big(np.load('welp_r10_oogE9_ver%s_tand1_tong6_bandB3_snuitL_punt1.npy'%v)[4:16,0:12],12,F10,(255,255,255,255)),l))
ims.append((mod((0,4,12,16),12),'model'))
V=Image.new('RGBA',(4*154,14+144),(255,255,255,255)); d=ImageDraw.Draw(V)
for i,(im,l) in enumerate(ims): V.alpha_composite(im,(i*154,14)); d.text((i*154,1),l,fill=(0,0,0))
V.save('ver_oog.png')
