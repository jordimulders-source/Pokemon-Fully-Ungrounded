import sys, numpy as np
from PIL import Image
FIN=np.load('FIN2.npy')
def rgba(a):
    im=np.zeros(a.shape+(4,),'uint8'); m=a>0; im[m,:3]=FIN[a[m]]; im[m,3]=255; return Image.fromarray(im)
def big(a,z,bg=(235,235,225,255)):
    im=rgba(a); o=Image.new('RGBA',(im.width*z,im.height*z),bg); o.alpha_composite(im.resize(o.size,Image.NEAREST)); return o
if __name__=='__main__':
    out=sys.argv[1]; ims=[np.load(f) for f in sys.argv[2:]]
    bigs=[big(a,8) for a in ims]; ones=[big(a,1) for a in ims]
    Wt=sum(b.width+20 for b in bigs)+sum(o.width+10 for o in ones)
    o=Image.new('RGBA',(Wt,max(b.height for b in bigs)),(255,255,255,255)); x=0
    for b in bigs: o.alpha_composite(b,(x,0)); x+=b.width+20
    for b in ones: o.alpha_composite(b,(x,0)); x+=b.width+10
    o.save(out)
