# mediaan.py: model zonder textuurvlekjes (mediaanfilter houdt vlakgrenzen scherp), lijnen eerst vervangen door omgeving
import numpy as np, sys, time
from PIL import Image, ImageFilter
M='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp'
k=int(sys.argv[1]) if len(sys.argv)>1 else 15
im=Image.open(M).convert('L'); L=np.asarray(im).astype(float)
lines=np.asarray(Image.open('lijnen_model.png'))>0
# lijnpixels vullen met max van omgeving (lijnen zijn donker), zodat ze de mediaan niet verdonkeren
F=np.asarray(im.filter(ImageFilter.MaxFilter(9))).astype(float)
L2=np.where(lines|(L<45),F,L)
L2[L>=235]=255
t=time.time(); med=np.asarray(Image.fromarray(L2.astype('uint8')).filter(ImageFilter.MedianFilter(k))).astype(int); print(time.time()-t)
np.save('medL.npy',med)
Image.fromarray(med.astype('uint8')).save('mediaan.png')
