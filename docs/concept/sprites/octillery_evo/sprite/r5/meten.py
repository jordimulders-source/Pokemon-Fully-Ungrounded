# meten.py [png...]: % bijna-zwart (luma<45) en gemiddelde luma van opake pixels
import sys
from PIL import Image
import numpy as np
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def m(p,crop=False):
    im=Image.open(p)
    if crop: im=im.crop((0,0,64,64))
    if im.mode=='P':
        t=im.info.get('transparency',0); a=np.asarray(im); rgb=np.asarray(im.convert('RGB')).astype(float); op=a!=t
    else:
        rgba=np.asarray(im.convert('RGBA')).astype(float); rgb=rgba[...,:3]; op=rgba[...,3]>0
    L=(rgb@[0.299,0.587,0.114])[op]; M=rgb.mean(2)[op]
    return (L<45).mean()*100,L.mean(),(M<45).mean()*100,M.mean()
for p in sys.argv[1:] or []:
    print('%-40s luma<45 %5.1f%%  luma %5.1f | mean<45 %5.1f%% mean %5.1f'%((p[-40:],)+m(p)))
if len(sys.argv)==1:
    for n in ['octillery','scizor','gyarados','seviper']:
        print('%-12s luma<45 %5.1f%%  luma %5.1f | mean<45 %5.1f%% mean %5.1f'%((n,)+m(G+n+'/anim_front_gba.png',True)))
