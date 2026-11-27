# vel r13: rij 1 = r13 | r12 | r9 | model (8x); rij 2 = 1x en 2x op wit en donker naast Murkrow
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
P=[H+'/hoatzin_r13.png',H+'/../r12/hoatzin_r12.png',H+'/../r9/hoatzin_r9.png']
r1=[rgb(p,W).resize((512,512),0) for p in P]+[md.resize((512,512),0)]
wit=[rgb(p,W) for p in P]+[murkrow(W)]; dk=[rgb(p,DK) for p in P]+[murkrow(DK)]
pad=10
v=Image.new('RGB',(4*512+3*pad,30+512+30+136+10),(225,225,225)); d=ImageDraw.Draw(v)
d.text((4,4),'8x: r13 | r12 | r9 | model',fill=(0,0,0))
for i,m in enumerate(r1): v.paste(m,(i*(512+pad),30))
y=30+512; d.text((4,y+8),'1x en 2x: r13, r12, r9, Murkrow (wit en donker)',fill=(0,0,0)); y+=30
x=0
for m in wit: v.paste(m,(x,y)); x+=72
for m in dk: v.paste(m,(x,y)); x+=72
x=600
for m in wit: v.paste(m.resize((128,128),0),(x,y)); x+=136
for m in dk: v.paste(m.resize((128,128),0),(x,y)); x+=136
v.save(H+'/vel.png'); print(v.size)
