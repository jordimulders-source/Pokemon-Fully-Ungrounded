import sys
from PIL import Image
D='impala_lijn/impala/sprite/r2'
sp=Image.open(f'{D}/impala_r2.png').convert('RGBA')
ka=Image.open(f'{D}/kaal.png').convert('RGBA')
mo=Image.open('impala_lijn/impala/referenties/model_r5.png').convert('RGBA').resize((64,64),Image.LANCZOS)
refs=['../../../graphics/pokemon/stantler/anim_front_gba.png','../../../graphics/pokemon/rapidash/anim_front_gba.png','../../../graphics/pokemon/girafarig/anim_front_gba.png','../../../graphics/pokemon/absol/anim_front_gba.png','skinguin/af/','dundragoon/af/']
ims=[mo,ka,sp]
import glob,os
for r in refs:
    if r.endswith('/'):
        f=[x for x in sorted(glob.glob(r+'*.png')) if '8x' not in x]
        r=f[0]
    im=Image.open(r).convert('RGBA'); im=im.crop((0,0,64,64)); ims.append(im)
S=6
W=Image.new('RGBA',(len(ims)*64*S,64*S+64*2),'white')
for i,im in enumerate(ims):
    W.paste(im.resize((64*S,64*S),Image.NEAREST),(i*64*S,0),im.resize((64*S,64*S),Image.NEAREST))
    W.paste(im,(i*64*S,64*S),im)
W.save(f'{D}/keuring/vel_vergelijk.png')
