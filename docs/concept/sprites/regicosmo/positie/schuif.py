# Verschuift ijsplaneet en Saturnus in Gemini r7 (alleen verplaatsen, niets tekenen).
import sys, numpy as np
from PIL import Image
from scipy import ndimage
im=np.array(Image.open('gemini/r7.png').convert('RGB'))
fg=im.min(axis=2)<230
lab,n=ndimage.label(fg)
L=lambda y,x: lab[y,x]
c2=lab==L(348,711)
ys,xs=np.nonzero(c2&(np.arange(im.shape[0])[:,None]>260))
cx=(xs.min()+xs.max())/2; cy=ys.max()-(xs.max()-xs.min())/2; r=(xs.max()-xs.min())/2
print('mars',cx,cy,r)
Y,X=np.mgrid[:im.shape[0],:im.shape[1]]
disk=(X-cx)**2+(Y-cy)**2<=(r+4)**2
box=lambda x0,x1,y0,y1:(X>=x0)&(X<x1)&(Y>=y0)&(Y<y1)
disk2=(X-cx)**2+(Y-cy)**2<=(r+10)**2
ijs=box(428,560,98,232)&~disk2
sat=box(860,1058,98,232)&~disk2
CEL=11.72
def make(dy_cells,dxi_cells,dxs_cells):
    out=im.copy()
    out[ijs]=255; out[sat]=255
    for m,dx,dy in ((ijs,dxi_cells,dy_cells),(sat,dxs_cells,dy_cells)):
        dx=round(dx*CEL); dy=round(dy*CEL)
        yy,xx=np.nonzero(m)
        out[yy+dy,xx+dx]=im[yy,xx]
    return out
vs=[(10,-5,5),(14,-6,6),(18,-6,6)]
tiles=[Image.fromarray(make(*v)) for v in vs]
for v,t in zip(vs,tiles): t.save('positie/r7_omlaag%d.png'%v[0])
sheet=Image.new('RGB',(1408,768*3//2*0+1152),(255,255,255))
W=704
sheet=Image.new('RGB',(W*2,384*2),(255,255,255))
sheet.paste(Image.open('gemini/r7.png').convert('RGB').resize((W,384)),(0,0))
for i,t in enumerate(tiles):
    sheet.paste(t.resize((W,384)),(((i+1)%2)*W,((i+1)//2)*384))
sheet.save('positie/vel.png')
