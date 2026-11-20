# r16 bouwen vanaf ../r15/hoatzin.png (kuif terug van r14): bouw16.py -> check -> diff -> vel
set -e
python3 bouw16.py
python3 check.py
python3 -c "
import numpy as np; from PIL import Image
a=np.array(Image.open('hoatzin.png')); b=np.array(Image.open('../r15/hoatzin.png')); d=a!=b
zones={'kuif/verre vleugel/kruin (r14-kuif)':(0,22,4,31),'nek':(22,36,22,31),'linker poot':(50,61,12,30)}
Z=np.zeros_like(d)
for y0,y1,x0,x1 in zones.values(): Z[y0:y1,x0:x1]=True
print('anders t.o.v. r15', d.sum(), 'buiten de zones', (d&~Z).sum(), 'silhouet', ((a>0)!=(b>0)).sum())
for nm,(y0,y1,x0,x1) in zones.items(): print(' ',nm, d[y0:y1,x0:x1].sum())
r14=np.array(Image.open('../r14/hoatzin.png')); k=(a!=r14)[8:22,4:31]; print('  kuif y8-21 anders dan r14:', k.sum())
im=Image.open('hoatzin.png'); im.resize((512,512),Image.NEAREST).save('hoatzin_8x.png')
p=im.getpalette()[:48]; print('kleuren', len(np.unique(a)), im.size)
open('normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%tuple(p[i:i+3]) for i in range(0,48,3)))"
python3 vel.py
