# r6: vrucht-id per spritepixel direct uit het model (kaal.reductie FID) en de model-op-schaal-helderheid; opslaan als npy
import sys; sys.path.insert(0,'sprite_r6')
import numpy as np; from PIL import Image
from gemeen2 import *; import kaal
o,F,FID,LD=kaal.reductie()
np.save('sprite_r6/fid.npy',FID); np.save('sprite_r6/ld.npy',LD)
M=np.asarray(model_op_schaal()).astype(float); np.save('sprite_r6/model64.npy',M)
r5=np.array(Image.open('sprite_r5/guarana2_r5_A.png'))
rng=np.random.RandomState(5); ids=np.unique(FID); col={i:rng.randint(40,255,3) for i in ids}
img=np.full((64,64,3),255,'uint8')
for Y,X in zip(*np.where(r5>0)):
    if FID[Y,X]: img[Y,X]=col[FID[Y,X]]
    elif r5[Y,X] in (2,3,4,5,12,14): img[Y,X]=(0,0,0)
img[(r5==2)]=img[r5==2]//2
Image.fromarray(img).resize((512,512),0).save('sprite_r6/fid_8x.png')
Image.fromarray(M.astype('uint8')).resize((512,512),0).save('sprite_r6/model64_8x.png')
print(len(ids))
