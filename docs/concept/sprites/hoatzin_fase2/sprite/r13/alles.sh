# r13 bouwen: alleen de kop op ../r12/hoatzin.png (kop13.py), check, export, vel
set -e
python3 kop13.py A
python3 check.py
python3 -c "
import numpy as np; from PIL import Image
a=np.array(Image.open('hoatzin.png')); b=np.array(Image.open('../r12/hoatzin.png')); d=a!=b
z=np.zeros_like(d); z[16:29,4:20]=True
print('anders', d.sum(), 'buiten kopzone', (d&~z).sum(), 'silhouet', ((a>0)!=(b>0)).sum())
im=Image.open('hoatzin.png'); im.resize((512,512),Image.NEAREST).save('hoatzin_8x.png')
p=im.getpalette()[:48]
open('normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%tuple(p[i:i+3]) for i in range(0,48,3)))"
python3 vel.py
