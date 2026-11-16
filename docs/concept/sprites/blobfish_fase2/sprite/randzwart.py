# Aandeel zwart (lum<50) in de buitenlijn (dekkende pixels met een transparante 4-buur) van echte Gen 3-sprites of van een eigen sprite
import sys; import numpy as np; from PIL import Image
def meet(f):
    im=Image.open(f); a=np.array(im)[:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    op=a!=0; p=np.pad(op,1); rand=op&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
    lum=pal[a]@[.299,.587,.114]; return (rand&(lum<50)).sum()/rand.sum(), rand.sum()
for f in sys.argv[1:]: z,n=meet(f); print(f'{f}: {z:.0%} zwart van {n} randpixels')
