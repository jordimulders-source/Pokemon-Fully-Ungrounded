# Bewaakt de afspraak "puur inkleuring": python3 bewaak.py NIEUW.png  (vanuit sprite3/kleur/)
# FAIL als het silhouet verandert, als geel verandert, of als een omlijnings-/lijnpixel van plek verandert buiten de toegestane omkleuring 1<->2.
import sys; from PIL import Image; import numpy as np
a=np.array(Image.open('basis.png')); b=np.array(Image.open(sys.argv[1]))
ok=True
d=int(((a>0)!=(b>0)).sum()); print('silhouet-diff:',d); ok&=d==0
ya=(a>=10); yb=np.isin(b,[10,11,12]); d=int((ya!=yb).sum()); print('geel-diff (plek):',d); ok&=d==0
la=np.isin(a,[1,2]); lb=np.isin(b,[1,2])
weg=int((la&~lb).sum()); bij=int((lb&~la).sum()); print('lijnpixels weg:',weg,'erbij:',bij,'(toegestaan: weg <= 60 voor dubbele lijnen, erbij <= 15, elk verantwoord in LOG.md)'); ok&=(weg<=60 and bij<=15)
print('omgekleurd 1<->2:',int((la&lb&(a!=b)).sum()),'| vulpixels gewijzigd:',int(((a>=3)&(a<=9)&(b>=3)&(b<=9)&(a!=b)).sum()),'| kleuren:',len(set(b.ravel()))-1)
print('OK' if ok else 'FAIL'); sys.exit(0 if ok else 1)
