import sys; import numpy as np; from PIL import Image
from gio import from_txt
from pal import PAL
o=from_txt(sys.argv[1]); s=int(sys.argv[3]) if len(sys.argv)>3 else 8
img=np.zeros((64,64,3),'uint8')+np.array([255,0,255],'uint8')
img[o<0]=(255,255,255)
for k,c in enumerate(PAL): img[o==k]=c
Image.fromarray(img).resize((64*s,64*s),Image.NEAREST).save(sys.argv[2])
