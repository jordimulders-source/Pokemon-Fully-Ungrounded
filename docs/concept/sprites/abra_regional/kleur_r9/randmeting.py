# randmeting.py: aandeel zwart (donkerste paletkleur) op de buitenrand = figuurpixels die (4-buren) aan transparant of de beeldrand grenzen
import sys; import numpy as np; from PIL import Image
def rand(a):
    t=np.pad(a==0,1,constant_values=True)
    nb=t[:-2,1:-1]|t[2:,1:-1]|t[1:-1,:-2]|t[1:-1,2:]
    return (a>0)&nb
def meet(p,frame=True,zwart=None):
    im=Image.open(p); a=np.array(im).astype(int)
    if frame and a.shape[0]==128: a=a[:64]
    pal=np.array(im.getpalette()[:48]).reshape(16,3)
    if zwart is None:
        used=[i for i in np.unique(a) if i>0]; zwart=min(used,key=lambda i:pal[i].sum())
    r=rand(a); return (a[r]==zwart).mean(), r.sum(), zwart
if __name__=='__main__':
    for p in sys.argv[1:]:
        f,n,z=meet(p); print(f'{p}: rand {n} px, zwart (idx {z}) {100*f:.1f} %')
