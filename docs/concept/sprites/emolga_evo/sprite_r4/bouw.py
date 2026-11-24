# r4 (alleen A0): buikonderrand volgt het model (Jordi: "maak dat iets smoother" · "baseer je op het model" · "hele subtiele wijzigingen").
# Gemeten: laatste modelpixel per spriterij (rechterrand model.png, dekking >= 0,5 op rijmidden) t.o.v. r3:
#   rij 43:39 44:39 45:37 46:36 47:35 48:35 49:33 50:31 51:31 52:29   (model)
#   rij 43:39 44:38 45:37 46:36 47:35 48:34 49:32 50:32 51:30 52:29   (r3: gelijkmatige trap 1 rij / 1 kolom)
# Overgenomen: 44->39, 48->35, 49->33 (de verticale stukjes van het model). Rij 50/51 niet: dan breekt de omlijning (sprong van 2).
# Lijn blijft 1 px: zwarte pixels die door de nieuwe rand binnen komen te liggen krijgen de witte buiktint (9) van de buren.
import numpy as np; from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo/'
im=Image.open(D+'sprite_r3/A0.png'); o=np.asarray(im).astype(int); n=o.copy()
WIJZ={(39,44):1,(35,48):1,(33,49):1,(33,48):9,(32,49):9}
for (x,y),v in WIJZ.items(): n[y,x]=v
zone=np.zeros((64,64),bool); zone[42:53,28:42]=True
assert ((n!=o)&~zone).sum()==0
print('gewijzigd:',[(x,y,int(o[y,x]),int(n[y,x])) for y,x in zip(*np.where(n!=o))],'| buiten zone:',int(((n!=o)&~zone).sum()))
p=Image.fromarray(n.astype('uint8'),'P'); p.putpalette(im.getpalette()); p.save(D+'sprite_r4/A0.png',transparency=0)
# vel: r3 | r4 | model 8x, 1x licht/donker
import sys; sys.path.insert(0,D+'gereedschap'); sys.path.insert(0,D+'sprite_r1')
import bouw_a0; from raster import modelcrop
pal=np.array(im.getpalette()[:48]).reshape(-1,3)
def rgb(a,bg):
    r=np.zeros((64,64,3),'uint8'); r[:]=bg
    for k in range(1,16): r[a==k]=pal[k]
    return Image.fromarray(r)
v=Image.new('RGB',(512*3+32,512+90),'white')
v.paste(rgb(o,(255,255,255)).resize((512,512),Image.NEAREST),(0,0)); v.paste(rgb(n,(255,255,255)).resize((512,512),Image.NEAREST),(528,0))
v.paste(modelcrop(bouw_a0.S,bouw_a0.OX,bouw_a0.OY,0,0,64,64,8),(1056,0))
for i,(a,bg) in enumerate([(o,(232,232,216)),(n,(232,232,216)),(o,(40,48,56)),(n,(40,48,56))]): v.paste(rgb(a,bg),(i*72,520))
from PIL import ImageDraw; ImageDraw.Draw(v).text((300,540),'r3 | r4 | model 8x;  1x: r3, r4 licht; r3, r4 donker',fill=(0,0,0))
v.save(D+'sprite_r4/vel.png')
