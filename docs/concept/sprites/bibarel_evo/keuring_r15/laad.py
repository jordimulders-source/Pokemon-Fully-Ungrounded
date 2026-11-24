# hulpfuncties: referentiesprites laden (frame 1, normal.pal) als (idx, pal)
import numpy as np
from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/'
def jasc(p):
    L=open(p).read().split('\n'); n=int(L[2]); return np.array([[int(v) for v in L[3+i].split()] for i in range(n)],dtype='uint8')
def gen3(naam):
    im=Image.open(R+f'graphics/pokemon/{naam}/anim_front.png'); a=np.asarray(im)[:64,:64].astype(int)
    pal=jasc(R+f'graphics/pokemon/{naam}/normal.pal'); return a,pal
def ons(pad):
    im=Image.open(R+pad)
    if im.mode=='P':
        a=np.asarray(im).astype(int); pal=np.array(im.getpalette()[:48]+[0]*48,dtype='uint8')[:48].reshape(16,3)
        t=im.info.get('transparency',0)
        if isinstance(t,bytes): t=0
        if t!=0:  # herindexeer zodat 0 transparant is
            m=np.arange(16); m[t],m[0]=0,t; a=m[a]; pal=pal[m.argsort()] if False else pal[[t]+[i for i in range(16) if i!=t]]
            a=np.asarray(im).astype(int); order=[t]+[i for i in range(16) if i!=t]; inv=np.argsort(order); a=inv[a]
        return a,pal
    rgba=np.asarray(im.convert('RGBA')); cols={}
    a=np.zeros(rgba.shape[:2],int); pal=[(0,0,0)]
    for y in range(rgba.shape[0]):
        for x in range(rgba.shape[1]):
            r,g,b,al=rgba[y,x]
            if al<128: continue
            k=(r,g,b)
            if k not in cols: cols[k]=len(pal); pal.append(k)
            a[y,x]=cols[k]
    return a,np.array(pal,dtype='uint8')
def rgb(a,pal,bg=(152,208,160)):
    o=np.zeros(a.shape+(3,),'uint8'); o[:]=bg; m=a>0; o[m]=pal[a[m]]; return Image.fromarray(o)
