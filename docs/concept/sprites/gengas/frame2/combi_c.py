# Variant C (16 nov): tegenbeweging. Bol kantelt rechtsom (gezicht omhoog) en gaat 3 px omhoog;
# de manen draaien 30° de andere kant op rond de bol en zakken 4 px, zodat ze los van het hoofd bewegen.
import math,numpy as np
from PIL import Image
B='docs/concept/sprites/gengas/'
f1=Image.open(B+'af/gengas.png');a=np.array(f1);pal=f1.getpalette()
lijf=np.array(Image.open(B+'sprite_v15/lijf_zonder_manen_v15.png'))
lab=np.load(B+'frame2/manen_lab.npy')
MANEN={1:(-14,9),2:(-8,-7),5:(10,11),11:(8,-7)}   # 30° tegen de klok in + 4 omlaag, binnen het vak gehouden
L=Image.fromarray(lijf,'P');L.putpalette(pal)
R=np.array(L.rotate(-10,resample=Image.NEAREST,center=(32,34),fillcolor=0))
out=np.zeros_like(a);ys,xs=np.where(R!=0);out[ys-3,xs]=R[ys,xs]
for k,(mx,my) in MANEN.items():
    for y,x in zip(*np.where(lab==k)):
        assert 0<=x+mx<64 and 0<=y+my<64
        out[y+my,x+mx]=a[y,x]
o=Image.fromarray(np.vstack([a,out]),'P');o.putpalette(pal);o.save(B+'frame2/combi_c_anim_front.png')
def rgba(x):
    o=Image.fromarray(x,'P');o.putpalette(pal);d=np.array(o.convert('RGBA'));d[x==0,3]=0;return Image.fromarray(d)
F=[rgba(a),rgba(out)]
SIN=lambda i,amp:int(math.sin(2*math.pi*(i%256)/256)*amp)
def geen(t):return (0,0,0)
def vslide(t):return (0,-SIN(t*384//40,6) if t<=40 else 0,0)
def tip(t):
    if t>35:return (0,0,0)
    if t<10:return (0,0,t//2*512)
    if t<=29:return (-SIN(((t-10)*128)//20,5),0,2048)
    return (0,0,(35-t)//2*1024)
def render(anim,naam,start=6,eind=40,Z=5):
    imgs=[];dur=[]
    for t in range(0,70,2):
        dx,dy,rot=anim(t);f=1 if start<=t<eind else 0
        s=F[f].rotate(rot*360/65536,resample=Image.NEAREST,center=(32,32))
        c=Image.new('RGBA',(96,96),(255,255,255,255));c.alpha_composite(s,(16+dx,16+dy))
        imgs.append(c.convert('RGB').resize((96*Z,96*Z),Image.NEAREST));dur.append(33)
    dur[-1]=1000
    imgs[0].save(B+'frame2/'+naam,save_all=True,append_images=imgs[1:],duration=dur,loop=0)
render(geen,'combi_c_zonder_engine.gif');render(vslide,'combi_c_v_slide.gif');render(tip,'combi_c_tip_move_forward.gif')
b=lambda x:Image.alpha_composite(Image.new('RGBA',(64,64),(255,255,255,255)),rgba(x)).convert('RGB').resize((384,384),Image.NEAREST)
sh=Image.new('RGB',(776,384),'white');sh.paste(b(a),(0,0));sh.paste(b(out),(392,0));sh.save(B+'frame2/combi_c_vel.png')
