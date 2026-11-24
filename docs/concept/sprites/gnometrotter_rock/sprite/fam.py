# fam.py: familie per modelpixel (volle resolutie). 0 achtergrond, 1 zwart/lijn, 2 grijs (steen), 3 roze, 4 blauw
import numpy as np; from PIL import Image
def familie(path):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    r,g,b=a[...,0],a[...,1],a[...,2]
    f=np.full(r.shape,2)
    f[(r-b>18)&(r-g>18)]=3
    f[(b-r>18)]=4
    f[a.max(2)<62]=1
    f[a.min(2)>=235]=0
    return a,f
if __name__=='__main__':
    a,f=familie('../r8/gemini_r8.png')
    np.savez_compressed('model_fam.npz',f=f.astype('uint8'))
    C=np.array([(255,255,255),(0,0,0),(150,150,150),(230,140,160),(100,160,210)],'uint8')
    Image.fromarray(C[f]).crop((260,30,760,530)).save('model_fam.png')
    print([(k,(f==k).sum()) for k in range(5)])
