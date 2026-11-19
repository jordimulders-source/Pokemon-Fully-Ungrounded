# model verkleind naar spriteformaat (oppervlakgemiddelde van het natieve raster, 3x3) -> np rgb 
import numpy as np; from PIL import Image
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float)
OY=OX=1; h=(n.shape[0]-1)//3
m=n[OY:OY+3*h,OX:OX+3*h].reshape(h,3,h,3,3).mean((1,3)).astype('uint8')
Image.fromarray(m).save('model_1x.png')
