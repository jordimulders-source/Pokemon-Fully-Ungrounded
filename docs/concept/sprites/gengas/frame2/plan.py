# Plan Gengas frame 2 (16 nov): bol staat stil (v15, rond), alleen de manen verplaatst; knik = engine-animatie (gesimuleerd).
import math,numpy as np
from PIL import Image
B='docs/concept/sprites/gengas/'
f1=Image.open(B+'af/gengas.png');a=np.array(f1);pal=f1.getpalette()
lijf=np.array(Image.open(B+'sprite_v15/lijf_zonder_manen_v15.png'))
lab=np.load(B+'frame2/manen_lab.npy')
import os
MANEN=eval(os.environ.get("MANEN","{1:(-6,0),2:(0,-5),5:(0,-6),11:(-6,-2)}"))   # boven, rechterhand, linkerhand, voet (dx,dy)
SUF=os.environ.get("SUF","")
out=lijf.copy()
for k,(dx,dy) in MANEN.items():
    for y,x in zip(*np.where(lab==k)): out[y+dy,x+dx]=a[y,x]
assert set(np.unique(out))<=set(np.unique(a))
for n,x in (('gengas_frame2_plan'+SUF+'.png',out),):
    o=Image.fromarray(x,'P');o.putpalette(pal);o.save(B+'frame2/'+n)
s=Image.fromarray(np.vstack([a,out]),'P');s.putpalette(pal);s.save(B+'frame2/gengas_anim_front_plan'+SUF+'.png')
def rgba(x):
    o=Image.fromarray(x,'P');o.putpalette(pal);r=o.convert('RGBA');d=np.array(r);d[x==0,3]=0;return Image.fromarray(d)
F=[rgba(a),rgba(out)]
SIN=lambda i,amp: int(math.sin(2*math.pi*(i%256)/256)*amp)
def vslide(t):   # Anim_VerticalSlide, data0=40
    return (0,-SIN(t*384//40,6) if t<=40 else 0,0)
def tip(t):      # Anim_TipMoveForward (rotatie in 1/65536 cirkel)
    if t>35: return (0,0,0)
    if t<10: return (0,0,t//2*512)
    if t<=29: return (-SIN(((t-10)*128)//20,5),0,9*256*0+2048)
    return (0,0,(35-t)//2*1024)
def frame_at(t): return 0 if t<6 or t>=30 else 1   # FRAME(0,6),(1,24),(0,..)
def render(anim,naam,Z=5):
    imgs=[];dur=[]
    for t in range(0,60,2):
        dx,dy,rot=anim(t)
        spr=F[frame_at(t)].rotate(rot*360/65536,resample=Image.NEAREST,center=(32,32))
        c=Image.new('RGBA',(96,96),(255,255,255,255));c.alpha_composite(spr,(16+dx,16+dy))
        imgs.append(c.convert('RGB').resize((96*Z,96*Z),Image.NEAREST));dur.append(33)
    dur[-1]=1200
    imgs[0].save(B+'frame2/'+naam,save_all=True,append_images=imgs[1:],duration=dur,loop=0)
render(vslide,'plan_v_slide'+SUF+'.gif');render(tip,'plan_tip_move_forward'+SUF+'.gif')
b=lambda x:rgba(x).resize((384,384),Image.NEAREST)
sh=Image.new('RGBA',(776,384),(255,255,255,255));sh.alpha_composite(b(a),(0,0));sh.alpha_composite(b(out),(392,0));sh.convert('RGB').save(B+'frame2/plan_vel'+SUF+'.png')
