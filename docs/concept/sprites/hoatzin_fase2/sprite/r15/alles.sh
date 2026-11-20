# r15 bouwen vanaf ../r14/hoatzin.png: verre vleugel/kuif/kruin -> buik, voeten, staart, nekrand -> check -> diff -> vel
set -e
python3 kuif15.py
python3 rest15.py
python3 check.py
python3 -c "
import numpy as np; from PIL import Image
a=np.array(Image.open('hoatzin.png')); b=np.array(Image.open('../r14/hoatzin.png')); d=a!=b; P=np.load('part.npy')
Z=np.zeros_like(d); Z[0:21,4:31]=True; Z[35:38,19:26]=True; Z[54:64,12:42]=True; Z[44:64]|=(P[44:64]==1); Z[34,16:21]=True
print('anders', d.sum(), 'buiten de zones', (d&~Z).sum(), 'silhouet', ((a>0)!=(b>0)).sum())
for nm,(y0,y1,x0,x1) in {'verre vleugel/kuif/kruin':(0,21,4,31),'buiktop':(35,38,19,26),'voeten':(54,64,12,42),'nekrand':(34,35,16,21)}.items(): print(' ',nm, d[y0:y1,x0:x1].sum())
V=np.zeros_like(d); V[54:64,12:42]=True; print('  staart (buiten voetzone)', (d&(P==1)&(np.arange(64)[:,None]>=44)&~V).sum())
im=Image.open('hoatzin.png'); im.resize((512,512),Image.NEAREST).save('hoatzin_8x.png')
p=im.getpalette()[:48]; print('kleuren', len(np.unique(a)), im.size)
open('normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%tuple(p[i:i+3]) for i in range(0,48,3)))"
python3 vel.py
