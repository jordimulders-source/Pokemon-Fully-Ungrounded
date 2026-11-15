import numpy as np
from PIL import Image
def rgba(a,FIN):
    im=np.zeros(a.shape+(4,),'uint8'); m=a>0; im[m,:3]=FIN[a[m]]; im[m,3]=255; return Image.fromarray(im)
def big(a,z,FIN,bg=(235,235,225,255)):
    im=rgba(a,FIN); o=Image.new('RGBA',(im.width*z,im.height*z),bg); o.alpha_composite(im.resize(o.size,Image.NEAREST)); return o
