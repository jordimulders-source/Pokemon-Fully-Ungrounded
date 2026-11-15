# Bewaakt c10: buiten de cirkelzone diff 0 met c9_2; binnen de zone alleen de halve cirkel t.o.v. c7 A; silhouet en gezicht diff 0.
import numpy as np
from PIL import Image
from basis import bevroren_kop
F=bevroren_kop(); ok=True
for v in '12':
  for t in ('','_grijs'):
    I=Image.open(f'welp_c10_{v}{t}.png'); a=np.array(I); c9=np.array(Image.open(f'../c9/welp_c9_2{t}.png')); c7=np.array(Image.open(f'../c7/welp_c7_a{t}.png'))
    Z=np.zeros(a.shape,bool); Z[23:34,23:30]=True
    r=dict(sil=int(((a>0)!=(c9>0)).sum()),buiten_c9=int(((a!=c9)&~Z).sum()),zone_vs_c7=int(((a!=c7)&Z).sum()),gezicht=int(((a!=c7)&F).sum()),palet=I.getpalette()[:48]==Image.open(f'../c9/welp_c9_2{t}.png').getpalette()[:48])
    print(v+t,r); ok&=r['sil']==0 and r['buiten_c9']==0 and r['gezicht']==0 and r['palet']
print('ALLES OK' if ok else 'FOUT')
