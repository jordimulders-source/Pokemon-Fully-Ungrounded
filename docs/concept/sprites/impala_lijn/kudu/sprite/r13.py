# r13 = r10 B6a (linkerstuk manen) + r12 (rechterstuk manen: schouderrand, x>=30). Jordi 27 nov.
from PIL import Image; import numpy as np
a=Image.open('r10/kudu_r10_B6a.png'); b=Image.open('r12/kudu_r12.png')
A=np.array(a.convert('RGBA')); B=np.array(b.convert('RGBA'))
out=A.copy(); out[:,30:]=B[:,30:]
assert ((A!=B).any(2)[:, :30] & False).sum()==0
im=Image.fromarray(out); im.save('r13/kudu_r13.png')
im.resize((512,512),Image.NEAREST).save('r13/kudu_r13_8x.png')
d=np.argwhere((out!=A).any(2)); print('px anders dan B6a:',len(d),'alle x>=30:',all(x>=30 for _,x in d))
