# Frame 2 viscacha: oren kantelen naar achteren (toppen 1 px naar rechts), staart zwiept (bovenste deel 1 px naar rechts).
# Alleen rijen verschuiven van onderdelen die aan lucht grenzen: geen verborgen stukken, geen nieuwe pixels.
import sys,numpy as np
from PIL import Image
src='docs/concept/sprites/viscacha/af/viscacha.png'
im=Image.open(src);a=np.array(im);pal=im.getpalette();b=a.copy()
def shift_rows(y0,y1,x0,x1,dx):
    for y in range(y0,y1+1):
        row=a[y,x0:x1+1].copy(); b[y,x0:x1+1]=0
        b[y,x0+dx:x1+1+dx]=row
shift_rows(15,19,8,16,1)    # top verre oor
shift_rows(15,18,17,27,1)   # top nabije oor (rij 19 blijft, anders breekt de omlijning)
shift_rows(14,22,48,62,1)   # staartpluim + bovenste staart
o=Image.fromarray(b,'P');o.putpalette(pal);o.save(sys.argv[1])
