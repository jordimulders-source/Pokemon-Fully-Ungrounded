import sys, numpy as np; from PIL import Image
from klas import PAL
from schrap3 import schrap, kies, Y0,Y1,X0,X1, k
SP='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/81de79ab-6056-55f3-b3d2-5fcd03808eb6/scratchpad/'
def render(kk,s=8):
    P=np.array(PAL+[(0,0,0)]*2,'uint8'); im=P[kk]; im[kk==0]=(200,220,200); return Image.fromarray(im).resize((kk.shape[1]*s,kk.shape[0]*s),0)
if __name__=='__main__':
    rows=eval(sys.argv[1]); cols=eval(sys.argv[2])
    kk,*_=schrap(rows,cols); print(kk.shape); render(kk).save(SP+sys.argv[3])
