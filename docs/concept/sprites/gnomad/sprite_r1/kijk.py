# kijk.py a.png [b.png ...] -> kijk.png: sprites op 8x naast het model op schaal (8x)
import sys, numpy as np; from PIL import Image
from gemeen import *
def model_op_schaal():
    a=Image.open('natief.png').convert('RGB'); n=int(round(100*S))
    m=a.resize((n,n),Image.LANCZOS)
    W=Image.new('RGB',(64,64),'white')
    # natief (0,0) -> sprite (CXS-CXN*S, BOTS-BOTN*S)
    W.paste(m,(int(round(CXS-CXN*S)),int(round(BOTS-BOTN*S)))); return W
def sprite(p,bg=(255,255,255)):
    im=Image.open(p); o=np.asarray(im).astype(int); pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
if __name__=='__main__':
    ps=[sprite(p) for p in sys.argv[1:]]+[model_op_schaal()]
    W=Image.new('RGB',(len(ps)*520,512),'white')
    for i,p in enumerate(ps): W.paste(p.resize((512,512),Image.NEAREST),(i*520,0))
    W.save('kijk.png')
