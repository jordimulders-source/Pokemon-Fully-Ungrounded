import sys, numpy as np
from PIL import Image
FIN=np.load('FIN2.npy')
def rgba(a):
    im=np.zeros(a.shape+(4,),'uint8'); m=a>0; im[m,:3]=FIN[a[m]]; im[m,3]=255; return Image.fromarray(im)
if __name__=='__main__':
    out=sys.argv[1]; ims=[rgba(np.load(f)) for f in sys.argv[2:]]
    Z=10; Wt=sum(i.width*Z+20 for i in ims)
    o=Image.new('RGBA',(Wt,max(i.height for i in ims)*Z),(235,235,225,255)); x=0
    for i in ims: o.alpha_composite(i.resize((i.width*Z,i.height*Z),Image.NEAREST),(x,0)); x+=i.width*Z+20
    o.save(out)
