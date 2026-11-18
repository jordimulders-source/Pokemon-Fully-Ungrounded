from PIL import Image; import numpy as np
from scipy import ndimage as nd
K=np.load('klassen.npy'); nb=K>0
body=nd.binary_opening(nb,structure=np.ones((11,11)))
body=nd.binary_dilation(body,structure=np.ones((5,5)))
dr=nb&~body
lab,n=nd.label(dr,structure=np.ones((3,3)))
sz=nd.sum(dr,lab,range(1,n+1))
keep=np.isin(lab,1+np.where(sz>=60)[0])
np.save('draden_mask.npy',keep); np.save('body_mask.npy',body)
im=np.full(K.shape+(3,),255,'uint8'); im[body]=(200,200,200); im[keep]=(255,0,0)
Image.fromarray(im).save('draden.png')
for k in range(1,n+1):
    if sz[k-1]>=60:
        ys,xs=np.where(lab==k); print(k,int(sz[k-1]),'x',xs.min(),xs.max(),'y',ys.min(),ys.max())
