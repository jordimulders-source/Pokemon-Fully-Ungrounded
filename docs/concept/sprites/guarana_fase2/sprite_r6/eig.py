# r6: welke vrucht (ellips uit vrucht.py, r3-r5) is eigenaar van elke spritepixel: de voorste ellips die de pixel bevat (zelfde regel als vrucht.teken)
import sys; sys.path.insert(0,'sprite_r6')
import numpy as np
from gemeen2 import *
import vrucht
def eigenaar():
    E=vrucht.ellipsen(); T2=vrucht.T2
    yy,xx=np.mgrid[0:64,0:64]; P=np.stack([xx+0.5,yy+0.5],-1)
    eig=np.full((64,64),-1); D=np.full((len(E),64,64),99.)
    for i,e in enumerate(E):
        d=P-e['mu']; D[i]=np.einsum('...i,ij,...j->...',d,e['Ci'],d); eig[D[i]<=T2]=i
    return E,eig,D
if __name__=='__main__':
    from PIL import Image
    E,eig,D=eigenaar(); np.save('sprite_r6/eig.npy',eig)
    o=np.array(Image.open('sprite_r5/guarana2_r5_A.png'))
    print(len(E),[round(e['back'],2) for e in E])
    rng=np.random.RandomState(3); col=rng.randint(40,255,(len(E)+1,3)); img=np.full((64,64,3),255,'uint8')
    R=np.isin(o,[2,3,4,5,12,14,10,11,1])&(o>0)
    for Y,X in zip(*np.where(R)):
        if eig[Y,X]>=0: img[Y,X]=col[eig[Y,X]]
    img[o==2]=img[o==2]//2
    Image.fromarray(img).resize((512,512),0).save('sprite_r6/eig_8x.png')
