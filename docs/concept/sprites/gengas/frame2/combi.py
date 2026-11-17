# Gengas frame 2 combinatie (16 nov): bol gekanteld (pixelrotatie, nearest, zoals de engine) + omhoog, manen los verplaatst (plan B).
import numpy as np,os
from PIL import Image
B='docs/concept/sprites/gengas/'
f1=Image.open(B+'af/gengas.png');a=np.array(f1);pal=f1.getpalette()
lijf=np.array(Image.open(B+'sprite_v15/lijf_zonder_manen_v15.png'))
lab=np.load(B+'frame2/manen_lab.npy')
MANEN={1:(-13,3),2:(-4,-14),5:(4,9),11:(7,-10)}
def maak(hoek,dy):
    L=Image.fromarray(lijf,'P');L.putpalette(pal)
    R=np.array(L.rotate(hoek,resample=Image.NEAREST,center=(32,34),fillcolor=0))
    out=np.zeros_like(a)
    ys,xs=np.where(R!=0); assert ys.min()+dy>=0
    out[ys+dy,xs]=R[ys,xs]
    for k,(mx,my) in MANEN.items():
        for y,x in zip(*np.where(lab==k)): out[y+my,x+mx]=a[y,x]
    return out
def rgb(x):
    o=Image.fromarray(x,'P');o.putpalette(pal);r=np.array(o.convert('RGB'));r[x==0]=255;return Image.fromarray(r).resize((384,384),Image.NEAREST)
f1r=rgb(a);vel=[f1r]
for naam,hoek in (('rechtsom',-10),('linksom',10)):
    out=maak(hoek,-3)
    o=Image.fromarray(np.vstack([a,out]),'P');o.putpalette(pal);o.save(B+f'frame2/combi_{naam}_anim_front.png')
    f2=rgb(out);vel.append(f2)
    f1r.save(B+f'frame2/combi_{naam}.gif',save_all=True,append_images=[f2],duration=[600,600],loop=0)
sh=Image.new('RGB',(3*392,384),'white')
for i,v in enumerate(vel): sh.paste(v,(392*i,0))
sh.save(B+'frame2/combi_vel.png')
