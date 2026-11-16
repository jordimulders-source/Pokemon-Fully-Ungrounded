# zone-vergelijking: paars-donker (spikes), nevel, ijs, oog per pixel model vs sprite
from PIL import Image; import numpy as np
spr=np.array(Image.open('../r1.png').convert('RGBA')).astype(int)
mod=np.array(Image.open('../model64.png').convert('RGB')).astype(int)
def klas(c,a=True):
    r,g,b=c[...,0],c[...,1],c[...,2]; L=0.299*r+0.587*g+0.114*b
    k=np.full(L.shape,'.',dtype='<U1')
    k[(L<235)]='n'                       # licht/nevel/ijs
    k[(L<235)&(b-r>25)&(L<175)]='p'      # paars/blauw donker (spikes)
    k[(L<80)]='D'
    k[(g>200)&(r<190)&(b>200)]='o'       # cyaan oog
    return k
ks=klas(spr[...,:3]); ks[spr[...,3]==0]='.'
km=klas(mod)
for y in range(64):
    print(''.join(km[y])+'  '+''.join(ks[y]))
