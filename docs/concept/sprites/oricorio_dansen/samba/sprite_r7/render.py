# render.py: work.txt (rijen 'NN <64 tekens>') -> samba.png (palet r5) + samba_8x.png
import numpy as np, sys
from PIL import Image
from palet import PAL
H='.123456789abcdef'
def lees(p='work.txt'):
    a=np.zeros((64,64),np.uint8)
    for l in open(p):
        if len(l)<4 or not l[:2].strip().isdigit(): continue
        y=int(l[:2]); s=l[3:3+64]
        for x,c in enumerate(s): a[y,x]=H.index(c) if c!='.' else 0
    return a
def schrijf(a,p):
    im=Image.fromarray(a,'P'); pal=sum(PAL,()); im.putpalette(list(pal)+[0]*(768-len(pal))); im.save(p,transparency=0)
if __name__=='__main__':
    a=lees(sys.argv[1] if len(sys.argv)>1 else 'work.txt')
    schrijf(a,'samba.png')
    Image.open('samba.png').convert('RGB').resize((512,512),Image.NEAREST).save('samba_8x.png')
    np.save('samba_r5.npy',a)
