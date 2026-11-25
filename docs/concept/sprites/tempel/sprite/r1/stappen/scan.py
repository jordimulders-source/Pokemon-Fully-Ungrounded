# scan.py rij|kol van tot xa xb : donkere modellijnen (L<75, >=2 px) per spriterij (x-posities) of per spritekolom (y-posities)
import sys, numpy as np
from PIL import Image
L=np.asarray(Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp').convert('L')).astype(int)
s=(983-46)/62; X0,Y0=46,57
mode=sys.argv[1]; a,b,c,d=map(int,sys.argv[2:6])
for k in range(a,b):
    if mode=='rij':
        Y=int(Y0+(k+0.5-3)*s); line=L[Y,int(X0+(c-1)*s):int(X0+(d-1)*s)]; off=X0+(c-1)*s; conv=lambda p:(p-X0)/s+1
    else:
        X=int(X0+(k+0.5-1)*s); line=L[int(Y0+(c-3)*s):int(Y0+(d-3)*s),X]; off=Y0+(c-3)*s; conv=lambda p:(p-Y0)/s+3
    runs=[];st=None
    for i,v in enumerate(list(line)+[255]):
        if v<75 and st is None: st=i
        if v>=75 and st is not None:
            if i-st>=2: runs.append(round(conv(off+(st+i)/2),1))
            st=None
    print(k,runs)
