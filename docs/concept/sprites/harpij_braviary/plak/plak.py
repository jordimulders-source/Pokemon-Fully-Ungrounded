# Extra kuifveren op r6 plakken: kopie van een eigen pluk, verschoven/gedraaid, ACHTER de bestaande pixels (alleen op wit).
import sys
from PIL import Image
import numpy as np
src=np.array(Image.open('gemini/r6.png').convert('RGB')).astype(int)
H,W,_=src.shape
lum=src.mean(2)
feather=(lum<160)
yy,xx=np.mgrid[0:H,0:W]
crest=feather&(yy<232)
right=crest&(xx>=525); left=crest&(xx<525)&(xx>300)
white=(src.min(2)>235)
def place(out,mask,dx,dy,ang,pivot):
    img=Image.fromarray(np.where(mask[...,None],src,0).astype(np.uint8))
    m=Image.fromarray((mask*255).astype(np.uint8))
    if ang:
        img=img.rotate(ang,resample=Image.NEAREST,center=pivot)
        m=m.rotate(ang,resample=Image.NEAREST,center=pivot)
    a=np.array(img).astype(int); mm=np.array(m)>127
    a=np.roll(a,(dy,dx),(0,1)); mm=np.roll(mm,(dy,dx),(0,1))
    put=mm&white
    out[put]=a[put]
    return put
variants={
 'A':[(right,10,45,0,(540,225)),(left,-25,40,0,(420,215))],
 'B':[(right,0,10,-28,(540,225)),(left,0,5,28,(420,215))],
 'C':[(right,0,20,-40,(540,225)),(left,0,15,40,(420,215))],
}
for k,ops in variants.items():
    out=src.copy(); w=white.copy()
    for mask,dx,dy,ang,pv in ops:
        place(out,mask,dx,dy,ang,pv)
    Image.fromarray(out.astype(np.uint8)).save(f'plak/r6_plak_{k}.png')
print('ok')
