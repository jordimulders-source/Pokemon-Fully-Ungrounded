# Gengas frame 2 (16 nov): alleen verplaatsen, niets tekenen.
# Lijf = sprite_v15/lijf_zonder_manen_v15.png (bol rond, door maker-agents); manen = pixels uit af/gengas.png volgens manen_lab.npy.
import sys,numpy as np
from PIL import Image
B='docs/concept/sprites/gengas/'
f1=Image.open(B+'af/gengas.png');a=np.array(f1);pal=f1.getpalette()
lijf=np.array(Image.open(B+'sprite_v15/lijf_zonder_manen_v15.png'))
lab=np.load(B+'frame2/manen_lab.npy')
LIJF=(0,-3)                      # bol 3 px omhoog (knik)
MANEN={1:(-6,0),2:(0,-5),5:(0,-6),11:(-6,-2)}   # boven, rechterhand, linkerhand, voet: (dx,dy)
out=np.zeros_like(a)
def paste(src,mask,dx,dy):
    for y,x in zip(*np.where(mask)):
        Y,X=y+dy,x+dx
        assert 0<=X<64 and 0<=Y<64, (y,x,dx,dy)
        out[Y,X]=src[y,x]
paste(lijf,lijf!=0,*LIJF)
for k,(dx,dy) in MANEN.items(): paste(a,lab==k,dx,dy)
assert set(np.unique(out))<=set(np.unique(a))
o=Image.fromarray(out,'P');o.putpalette(pal);o.save(B+'frame2/gengas_frame2.png')
v=np.vstack([a,out]);s=Image.fromarray(v,'P');s.putpalette(pal);s.save(B+'frame2/gengas_anim_front.png')
def big(x):
    r=np.array(Image.fromarray(x,'P').convert('RGB') if False else (lambda i:(i.putpalette(pal),i)[1])(Image.fromarray(x,'P')).convert('RGB'));r[x==0]=255
    return Image.fromarray(r).resize((384,384),Image.NEAREST)
b1,b2=big(a),big(out)
b1.save(B+'frame2/gengas_frame2.gif',save_all=True,append_images=[b2,b1,b2,b1],duration=[700,250,250,250,1200],loop=0)
sh=Image.new('RGB',(776,384),'white');sh.paste(b1,(0,0));sh.paste(b2,(392,0));sh.save(B+'frame2/gengas_frame2_vel.png')
