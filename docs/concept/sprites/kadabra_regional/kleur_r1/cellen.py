# model -> 100x100 celraster (mediaan per cel), opgeslagen als cellen.npy / cellen.png
import sys,numpy as np
sys.path.insert(0,'../model'); from grid10 import load,cell,cls
from PIL import Image
a=load('../model/model_B_hand3.png')
C=np.array([[cell(a,i,j) for i in range(100)] for j in range(100)])
np.save('cellen.npy',C); Image.fromarray(C.astype('uint8')).save('cellen.png')
if __name__=='__main__':
    for j in range(100): print('%2d '%j+''.join(cls(C[j,i]) for i in range(100)))
