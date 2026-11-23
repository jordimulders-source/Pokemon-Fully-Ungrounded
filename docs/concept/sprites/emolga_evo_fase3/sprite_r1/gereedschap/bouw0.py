# bouw0.py: kale reductie: silhouet = model.png (blok < 50% achtergrond), kleur = natieve r6-klassen (lijf via de gemeten rek), 16x16-blokken,
# groep eerst (zwart+donker samen), K wint vanaf 35% -> palet -> ../tussen/kaal.png
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/emolga_evo_fase3/sprite_r1/gereedschap')
from fv import *; import palet, os
c,reg=klassenkaart(); c=samen(c)
o,cov=reduceer4(c,dx=16,kprio=0.35)
p=np.array(palet.VAN2)[o]
os.makedirs(D+'sprite_r1/tussen',exist_ok=True)
palet.opslaan(p,D+'sprite_r1/tussen/kaal.png'); np.save(D+'sprite_r1/tussen/cov.npy',cov)
print('kaal: fig px',(p>0).sum())
