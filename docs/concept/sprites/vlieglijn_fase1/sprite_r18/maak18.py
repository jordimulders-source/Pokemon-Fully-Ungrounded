# r18 = r17 met de onderkant van het achterlijf (waar de buis zat) opnieuw uit de eigen strepen opgebouwd:
# strepen links van de onderpool buigen naar rechts (spiegel van rechts, waar ze al naar links buigen),
# schaduw (licht->4, donker->2) alleen in de onderste 2 rijen boven de echte onderrand (sikkel), geen band.
import sys; sys.path.insert(0,'sprite_r14')
from lib import *
im=Image.open('sprite_r17/vlieg_r17.png'); b=im.load()
P38={x:b[x,38] for x in range(35,47)}            # strepenpatroon van rij 38 (onaangetast)
# alleen achterlijfpixels (kabeldonker is sinds r16 ook index 3, dus expliciet opgesomd)
gebied=[(x,39) for x in range(35,46)]+[(x,40) for x in (35,36,37,38,42,43,44)]+[(36,41),(37,41)]\
      +[(37,42),(38,42),(37,43),(38,43),(39,43),(37,44),(38,44),(39,44),(38,45),(39,45)]
ONDER={35:40,36:41,37:44,38:45,39:45}            # onderrand van het achterlijf per kolom (achter de poten)
for (x,y) in gebied:
    s=(y-38)//2 if x<=41 else 0
    bron=P38.get(max(35,x-s))
    licht=bron in (5,6)
    schaduw=y>=ONDER.get(x,99)-1
    b[x,y]=(4 if schaduw else 5) if licht else (2 if schaduw else 3)
im.save('sprite_r18/vlieg_r18.png',transparency=0)
onbg(im).resize((512,512),Image.NEAREST).save('sprite_r18/vlieg_r18_8x.png')
