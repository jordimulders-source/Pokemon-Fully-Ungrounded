# vel r10: rij 1 = A | B | r9 | model (8x); rij 2 = kop+snavel 12x (A | B | r9 | model);
# rij 3 = 1x op wit en donker: A, B, r9, model, Murkrow gba
import os,sys,numpy as np
from PIL import Image,ImageDraw
H=os.path.dirname(os.path.abspath(__file__)); R=H+'/../../../../../..'
sys.path.insert(0,H+'/../r8'); from gemeen import model_op_schaal
def rgb(path,bg):
    im=Image.open(path); a=np.array(im); w=np.array(im.convert('RGB')); w[a==0]=bg; return Image.fromarray(w)
def murkrow(bg):
    a=np.array(Image.open(R+'/graphics/pokemon/murkrow/anim_front_gba.png'))[:64]
    t=[l for l in open(R+'/graphics/pokemon/murkrow/normal_gba.pal').read().split('\n')[3:] if l.strip()]
    pal=np.array([[int(v) for v in l.split()] for l in t],'uint8'); w=pal[a]; w[a==0]=bg; return Image.fromarray(w)
md=model_op_schaal().convert('RGB')
W=(255,255,255); DK=(40,40,48)
P=[H+'/hoatzin_r10_A.png',H+'/hoatzin_r10_B.png',H+'/../r9/hoatzin_r9.png']
r1=[rgb(p,W).resize((512,512),0) for p in P]+[md.resize((512,512),0)]
box=(6,0,30,26)
r2=[rgb(p,W).crop(box).resize((24*12,26*12),0) for p in P]+[md.crop(box).resize((24*12,26*12),0)]
r3=[rgb(p,W) for p in P]+[md,murkrow(W)]+[rgb(p,DK) for p in P]+[murkrow(DK)]
pad=10
v=Image.new('RGB',(4*512+3*pad,30+512+30+312+30+64*2+20),(225,225,225)); d=ImageDraw.Draw(v)
y=0; d.text((4,y+4),'8x: r10 A (r9-donkerte) | r10 B (Murkrow-bereik) | r9 | model',fill=(0,0,0)); y+=30
for i,m in enumerate(r1): v.paste(m,(i*(512+pad),y))
y+=512; d.text((4,y+8),'kop + snavel 12x: A | B | r9 | model',fill=(0,0,0)); y+=30
for i,m in enumerate(r2): v.paste(m,(i*(512+pad),y))
y+=312; d.text((4,y+8),'1x: A, B, r9, model, Murkrow (wit) | A, B, r9, Murkrow (donker); en 2x',fill=(0,0,0)); y+=30
x=0
for m in r3: v.paste(m,(x,y)); x+=72
x+=20
for m in r3[:3]+r3[4:5]: v.paste(m.resize((128,128),0),(x,y)); x+=136
for m in r3[5:]: v.paste(m.resize((128,128),0),(x,y)); x+=136
v.save(H+'/vel.png'); print(v.size)
