# Bewaakt c8 t.o.v. c7 A: alleen pixels in de cirkelzone (x23-29, y23-33) gewijzigd, silhouet en gezicht diff 0, palet gelijk.
import numpy as np
from PIL import Image
from basis import bevroren_kop
F=bevroren_kop(); ok=True
for t in ('','_grijs'):
    A=np.array(Image.open(f'../c7/welp_c7_a{t}.png')); pa=Image.open(f'../c7/welp_c7_a{t}.png').getpalette()[:48]
    for v in '123':
        I=Image.open(f'welp_c8_{v}{t}.png'); a=np.array(I)
        Z=np.zeros(a.shape,bool); Z[23:34,23:30]=True; d=a!=A
        r=dict(sil=int(((a>0)!=(A>0)).sum()),buiten=int((d&~Z).sum()),gezicht=int((d&F).sum()),palet=I.getpalette()[:48]==pa,px=int(d.sum()))
        print(v+t,r); ok&=r['sil']==0 and r['buiten']==0 and r['gezicht']==0 and r['palet']
print('ALLES OK' if ok else 'FOUT')
