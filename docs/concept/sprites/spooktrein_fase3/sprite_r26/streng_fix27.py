# r27 = r26 + alleen paletwaarden (0 px): grijs terug naar (licht warm) neutraal grijs, roestdonker 9 van paars-rood naar donker roestbruin.
# Helderheid per index ~gelijk aan r26, zodat de contrastwinst van r26 blijft. Asserts: indexen gelijk aan r26, groen en zwart ongewijzigd.
import numpy as np
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/'
im=Image.open(D+'sprite_r26/sprite.png'); pal=list(im.getpalette()); oud=pal[:]
NIEUW={9:(90,46,38),10:(176,169,160),11:(124,120,114),12:(82,78,75)}
for i,c in NIEUW.items(): pal[3*i:3*i+3]=list(c)
for i in (0,1,2,3,4,5,6,13): assert pal[3*i:3*i+3]==oud[3*i:3*i+3]
o=im.copy(); o.putpalette(pal)
assert (np.array(o)==np.array(im)).all()
o.save(D+'sprite_r27/sprite.png',transparency=0)
o.resize((512,512),Image.NEAREST).save(D+'sprite_r27/sprite_8x.png',transparency=0)
L=lambda c:.3*c[0]+.59*c[1]+.11*c[2]
for i,c in NIEUW.items(): print(i,tuple(oud[3*i:3*i+3]),round(L(oud[3*i:3*i+3])),'->',c,round(L(c)))
