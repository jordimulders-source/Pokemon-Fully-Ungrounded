# Vel r21: koeienvanger 12x r21 | r20 | model; hele sprite 8x r21 | r20 | model_64-projectie; 1x/2x.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r18')
from vel import *
P21=D+'sprite_r21/sprite.png'; P20=D+'sprite_r20/sprite.png'
box=(0,42,28,60)
kv=rij([label(z(P21,12,box),'r21'),label(z(P20,12,box),'r20'),label(model_sprite_box(box,-1,12),'model (natief, geprojecteerd)')])
heel=rij([label(z(P21,8),'r21 8x'),label(z(P20,8),'r20 8x'),label(model_sprite_box((0,0,64,64),-1,8),'model 8x (projectie)')])
M8=model_sprite_box((0,0,64,64),-1,8)
def klein(Z): return rij([z(P21,Z),z(P20,Z),M8.resize((64*Z,64*Z),Image.LANCZOS)],gap=8)
kl=rij([label(klein(1),'1x r21|r20|model'),label(klein(2),'2x r21|r20|model')],gap=30)
vorm=Image.open(D+'sprite_r21/vorm_16x.png').convert('RGBA')
kolom([kv,vorm,heel,kl]).convert('RGB').save(D+'sprite_r21/vel.png')
Image.open(P21).resize((512,512),Image.NEAREST).save(D+'sprite_r21/sprite_8x.png',transparency=0)
