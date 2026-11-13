# Bewaakt de afspraak "puur inkleuring": python3 bewaak.py NIEUW.png  (vanuit sprite3/kleur/)
# FAIL als het silhouet verandert (Jordi: "het silhouet staat"). Binnen het silhouet mag belijning, kleur, mond en zuignappen.
import sys; from PIL import Image; import numpy as np
a=np.array(Image.open('basis.png')); b=np.array(Image.open(sys.argv[1]))
ok=True
d=int(((a>0)!=(b>0)).sum()); print('silhouet-diff:',d); ok&=d==0
ya=(a>=10); yb=np.isin(b,[10,11,12]); print('geel-diff (plek):',int((ya!=yb).sum()),'(mag binnen mond/zuignappen, verantwoord in LOG.md)')
la=np.isin(a,[1,2]); lb=np.isin(b,[1,2])
print('lijnpixels weg:',int((la&~lb).sum()),'erbij:',int((lb&~la).sum()),'(binnenlijnen mogen scherper; elk blok verantwoord in LOG.md met het model als bron)')
print('omgekleurd 1<->2:',int((la&lb&(a!=b)).sum()),'| vulpixels gewijzigd:',int(((a>=3)&(a<=9)&(b>=3)&(b<=9)&(a!=b)).sum()),'| kleuren:',len(set(b.ravel()))-1)
print('OK' if ok else 'FAIL'); sys.exit(0 if ok else 1)
