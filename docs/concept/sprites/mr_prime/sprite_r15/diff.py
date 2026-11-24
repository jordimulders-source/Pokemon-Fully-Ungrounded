# Diff tegen r14: binnen de zone x40-63 y0-20 tellen, erbuiten moet 0 zijn.
import numpy as np, sys; from PIL import Image
def L(p): return np.asarray(Image.open(p).convert('RGBA')).astype(int)
a=L('../sprite_r14/mr_prime.png')
for p in ['mr_prime.png','variant_A.png','variant_B1.png','variant_B2.png']:
    b=L(p); A=a[...,3]>0; B=b[...,3]>0
    d=(A!=B)|(A&B&np.any(a[...,:3]!=b[...,:3],axis=-1))
    z=np.zeros_like(d); z[0:21,40:64]=1
    print(p,'in zone:',int((d&z).sum()),'buiten zone:',int((d&~z).sum()))
