# r14 bouwen vanaf ../r13/hoatzin.png: kuif/verre vleugel/kruin -> buik, voeten, staart, nekbinnenlijn -> check -> diff -> vel
set -e
python3 kuif14.py
python3 rest14.py
python3 check.py
python3 -c "
import numpy as np; from PIL import Image
a=np.array(Image.open('hoatzin.png')); b=np.array(Image.open('../r13/hoatzin.png')); d=a!=b; P=np.load('part.npy')
Z=np.zeros_like(d); Z[0:21,4:31]=True; Z[36:47,16:36]=True; Z[54:64,12:41]=True; Z[44:64]|=(P[44:64]==1); Z[24:36,24:30]=True
print('anders', d.sum(), 'buiten de zones', (d&~Z).sum(), 'silhouet', ((a>0)!=(b>0)).sum())
for nm,(y0,y1,x0,x1) in {'kuif/verre vleugel/kruin':(0,21,4,31),'buik':(36,47,16,36),'voeten':(54,64,12,41),'nek-binnenlijn':(24,36,24,30)}.items(): print(' ',nm, d[y0:y1,x0:x1].sum())
print('  staart', (d&(P==1)&(np.arange(64)[:,None]>=44)).sum())
im=Image.open('hoatzin.png'); im.resize((512,512),Image.NEAREST).save('hoatzin_8x.png')
p=im.getpalette()[:48]
open('normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%tuple(p[i:i+3]) for i in range(0,48,3)))"
python3 vel.py
