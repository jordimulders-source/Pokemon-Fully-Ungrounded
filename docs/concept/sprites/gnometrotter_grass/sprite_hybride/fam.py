# fam.py (Grass): familie per modelpixel (volle resolutie). 0 achtergrond, 1 zwart/lijn, 2 bruin (schors), 3 roze, 4 blauw, 5 groen (blad)
import numpy as np; from PIL import Image
MODEL='../hybride/model_hybride.png'
def familie(path=MODEL):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    r,g,b=a[...,0],a[...,1],a[...,2]
    f=np.full(r.shape,2)
    f[(r-g>38)&(r-b>15)]=3
    f[(b-r>18)]=4
    f[(g-r>6)&(g-b>10)]=5
    f[a.max(2)<62]=1
    f[a.min(2)>=235]=0
    return a,f
if __name__=='__main__':
    a,f=familie()
    np.savez_compressed('model_fam.npz',f=f.astype('uint8'))
    C=np.array([(255,255,255),(0,0,0),(140,90,50),(230,140,160),(100,160,210),(80,170,70)],'uint8')
    Image.fromarray(C[f]).crop((260,30,760,530)).save('model_fam.png')
    print([(k,(f==k).sum()) for k in range(6)])
