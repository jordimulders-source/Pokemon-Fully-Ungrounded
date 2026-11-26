import sys
from PIL import Image
import numpy as np
def show(src,dst,k=8):
    im=Image.open(src); p=im.getpalette(); a=np.array(im)
    rgb=np.array(p[:48]).reshape(16,3)[a].astype(np.uint8)
    rgb[a==0]=(255,255,255)
    # raster
    big=np.kron(rgb,np.ones((k,k,1),np.uint8))
    Image.fromarray(big).save(dst)
if __name__=='__main__': show(sys.argv[1],sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 8)
