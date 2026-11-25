# Vergelijkingsvel keuring r4: model (op spriteraster) | kaal | r4 | Gen3-refs | maatstaf
import glob
from PIL import Image
import numpy as np
D='impala_lijn/impala/sprite/r4'
sp=Image.open(f'{D}/impala_r4.png'); sp.save('/dev/null','PNG') if False else None
sp=Image.open(f'{D}/impala_r4.png').convert('RGBA')
ka=Image.open(f'{D}/kaal.png').convert('RGBA')
a=np.array(ka)[:,:,3]; ys,xs=np.nonzero(a); print('kaal bbox',xs.min(),xs.max(),ys.min(),ys.max())
a2=np.array(sp)[:,:,3]; ys2,xs2=np.nonzero(a2); print('r4 bbox',xs2.min(),xs2.max(),ys2.min(),ys2.max())
m=Image.open('impala_lijn/impala/referenties/model_r5.png').convert('RGBA')
x0,y0,p,W,H=196,39,15.126984126984127,43,63
mc=m.crop((int(x0),int(y0),int(x0+p*W),int(y0+p*H))).resize((W,H),Image.LANCZOS)
mo=Image.new('RGBA',(64,64),(255,255,255,0)); mo.paste(mc,(xs.min(),ys.min()))
mo.save(f'{D}/keuring/model_64.png')
refs=['../../../graphics/pokemon/stantler/anim_front_gba.png','../../../graphics/pokemon/rapidash/anim_front_gba.png','../../../graphics/pokemon/girafarig/anim_front_gba.png','../../../graphics/pokemon/absol/anim_front_gba.png','skinguin/af/skinguin.png','dundragoon/af/dundragoon.png','viscacha/af/viscacha.png','awki/af/awki.png']
ims=[mo,ka,sp]
for r in refs:
    im=Image.open(r)
    if im.mode=='P': im.info['transparency']=0
    im=im.convert('RGBA').crop((0,0,64,64)); ims.append(im)
S=6
Wd=Image.new('RGBA',(6*64*S,2*(64*S+70)),'white')
for i,im in enumerate(ims):
    c,r=i%6,i//6
    big=im.resize((64*S,64*S),Image.NEAREST)
    Wd.paste(big,(c*64*S,r*(64*S+70)),big); Wd.paste(im,(c*64*S,r*(64*S+70)+64*S+3),im)
Wd.save(f'{D}/keuring/vel_vergelijk.png')
# groot naast elkaar: model 64 vs sprite op 10x
S=10; N=Image.new('RGBA',(2*64*S+20,64*S),'white')
for i,im in enumerate([mo,sp]):
    big=im.resize((64*S,64*S),Image.NEAREST); N.paste(big,(i*(64*S+20),0),big)
N.save(f'{D}/keuring/naast.png')
