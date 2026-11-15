# Jordi 15 nov: "houd rekening met het feit dat de bol nu rechte lijnen heeft, dat moet echt een bol blijven".
# Bol in het silhouet = cirkel r 11 rond (31.5, 31.0) (past op de modelbreedte x 21-42); ijspunten bovenop (model, y <= 23) blijven.
import numpy as np; from PIL import Image
M=np.load('sprite/sil56.npy'); yy,xx=np.mgrid[0:64,0:64]
C=((xx-31.5)**2+(yy-31.0)**2)<=11*11
Z=(xx>=19)&(xx<=44)&(yy>=19)&(yy<=34)
N=M.copy(); N[Z]=(C|(M&(yy<=23)))[Z]
np.save('sprite/sil56_rond.npy',N)
print('erbij',int((N&~M).sum()),'eraf',int((M&~N).sum()))
for y in range(17,40): print('%2d '%y+''.join('#' if N[y,x] else '.' for x in range(16,48)))
a=np.zeros((64,64,4),'uint8'); a[N]=[0,0,0,255]; Image.fromarray(a).save('sprite/silhouet56_rond.png')
