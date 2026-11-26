import numpy as np, sys
from PIL import Image
import kaal
def rgb(A,bgc=(235,240,235)):
    P=np.array(kaal.PAL,np.uint8); r=P[A]; r[A==0]=bgc; return Image.fromarray(r)
