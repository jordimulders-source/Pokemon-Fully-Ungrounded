# Levert welp_r6.png (64x64 indexed, index 0 transparant), _8x en vel.png
import numpy as np
from PIL import Image
from toon6 import big
F=np.load('FIN6.npy'); a=np.load('welp_r6.npy')
h,w=a.shape; full=np.zeros((64,64),'uint8'); x0=(64-w)//2; full[63-h:63,x0:x0+w]=a
p=Image.fromarray(full,'P'); pal=[255,0,255]+[int(v) for c in F[1:] for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save('welp_r6.png',transparency=0)
big(a,8,F,(255,255,255,255)).save('welp_r6_8x.png')
q=Image.open('welp_r6.png'); print(q.mode,q.size,'kleuren',len(set(np.array(q).ravel())))
