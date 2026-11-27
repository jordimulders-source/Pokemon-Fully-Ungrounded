# Basis = variant B (schouders 14 modelpixels omlaag); voeten naar het midden (alleen verplaatsen).
import numpy as np
from PIL import Image
from scipy import ndimage
im=np.array(Image.open('positie/r7_omlaag14.png').convert('RGB'))
fg=im.min(axis=2)<230
lab,n=ndimage.label(fg)
Y,X=np.mgrid[:im.shape[0],:im.shape[1]]
box=lambda x0,x1,y0,y1:(X>=x0)&(X<x1)&(Y>=y0)&(Y<y1)
links=box(500,655,578,700); rechts=box(788,932,596,724)
CEL=11.72
def make(dl,dr):
    out=im.copy(); out[links]=255; out[rechts]=255
    for m,dx in ((links,dl),(rechts,dr)):
        dx=round(dx*CEL); yy,xx=np.nonzero(m); out[yy,xx+dx]=im[yy,xx]
    return Image.fromarray(out)
vs=[(1,-3),(2,-5),(3,-7)]
W,H=704,384
sheet=Image.new('RGB',(W*2,H*2),(255,255,255))
sheet.paste(Image.fromarray(im).resize((W,H)),(0,0))
for i,v in enumerate(vs):
    t=make(*v); t.save('positie/B_voeten%d.png'%(i+1))
    sheet.paste(t.resize((W,H)),(((i+1)%2)*W,((i+1)//2)*H))
sheet.save('positie/vel_voeten.png')
