# toon.py uit.png idx.npy [...] : naast elkaar op 8x met modelpalet
import numpy as np,sys; from PIL import Image
C=np.load('model_pal.npy'); ims=[]
for f in sys.argv[2:]:
    o=np.load(f); r=np.full(o.shape+(3,),255,'uint8'); m=o>0; r[m]=C[o[m]-1].astype('uint8'); ims.append(Image.fromarray(r).resize((o.shape[1]*8,o.shape[0]*8),Image.NEAREST))
V=Image.new('RGB',(sum(i.width+16 for i in ims),max(i.height for i in ims)),(255,255,255)); x=0
for i in ims: V.paste(i,(x,0)); x+=i.width+16
V.save(sys.argv[1])
