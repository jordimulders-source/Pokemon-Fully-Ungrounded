# Natief r10 -> modeltonen (dichtstbijzijnde van een handvol modelkleuren gemeten in r10)
from PIL import Image; import numpy as np
M={'.':(255,255,255),'k':(19,17,25),'d':(129,114,94),'m':(166,150,123),'l':(191,175,151),'h':(216,200,173),
   'c':(242,235,210),'r':(107,20,36),'R':(150,40,55),'g':(100,90,75)}
def klas():
    a=np.array(Image.open('natief_r10.png')).astype(int)
    K=list(M); C=np.array([M[k] for k in K])
    d=((a[:,:,None,:]-C[None,None])**2).sum(-1); i=d.argmin(-1)
    return np.array(K)[i], d.min(-1)
if __name__=='__main__':
    T,e=klas()
    for y in range(8,99): print('%2d '%y+''.join(T[y,5:95]))
    print('max err',np.sqrt(e.max()))
