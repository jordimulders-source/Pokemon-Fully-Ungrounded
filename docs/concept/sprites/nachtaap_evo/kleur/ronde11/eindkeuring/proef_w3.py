# Proef (niet de sprite): voorgestelde reparatie achterste wig, 4 px. Alleen een vergelijkingsplaatje.
import numpy as np
from PIL import Image
im=Image.open('../nachtaap.png'); a=np.array(im).copy()
for (x,y,v) in [(42,34,3),(44,34,6),(45,34,6),(43,35,6)]: a[y,x]=v
out=Image.fromarray(a,'P'); out.putpalette(im.getpalette()); out.info['transparency']=0
def show(i):
    r=i.convert('RGBA'); px=r.load(); s=np.array(i)
    for y in range(64):
        for x in range(64):
            if s[y,x]==0: px[x,y]=(0,0,0,0)
    return r
W=Image.new('RGBA',(2*(64*4+8)+2*72,64*4),(248,248,248,255))
for k,i in enumerate([im,out]):
    r=show(i); W.alpha_composite(r.crop((30,20,64,52)).resize((34*7,32*7),Image.NEAREST),(k*(64*4+8),0)); W.alpha_composite(r,(2*(64*4+8)+k*72,10))
W.save('proef_w3_voor_na.png'); print('diff px',(a!=np.array(im)).sum())
