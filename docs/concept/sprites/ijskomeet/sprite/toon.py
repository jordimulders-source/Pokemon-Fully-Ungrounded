import sys; from PIL import Image; import numpy as np
from klas_pal import COL
o=np.load(sys.argv[1]); img=np.zeros((64,64,3),'uint8')+np.array([255,0,255],'uint8')
for k,c in COL.items(): img[o==k]=c
Image.fromarray(img).resize((512,512),Image.NEAREST).save(sys.argv[2])
