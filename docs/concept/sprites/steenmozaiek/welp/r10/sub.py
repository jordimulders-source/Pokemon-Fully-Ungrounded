# Model per halve spritepixel geclassificeerd (2x2 subcellen per spritepixel). python3 sub.py x0,y0,x1,y1
import sys,numpy as np
from PIL import Image
from punt import klas
m=np.asarray(Image.open('../../referenties/model_welp_gekozen.png').convert('RGB')).astype(int); k=16.896
def cel(X0,X1,Y0,Y1):
    cnt={}
    for c in m[int(Y0):int(Y1),int(X0):int(X1)].reshape(-1,3):
        kk='.' if c.mean()>246 else klas(tuple(c)); cnt[kk]=cnt.get(kk,0)+1
    return max(cnt,key=cnt.get)
b=tuple(map(int,sys.argv[1].split(',')))
print('    '+''.join(('%-2d'%x)[-2:] for x in range(b[0],b[2])))
for y in range(b[1],b[3]):
    for h in (0,0.5):
        row=''
        for x in range(b[0],b[2]):
            for v in (0,0.5):
                X0=99.3+(x+v)*k+2;Y0=191.5+(y+h)*k+2; row+=cel(X0,X0+k/2-4,Y0,Y0+k/2-4)
        print(('%2d  '%y if h==0 else '    ')+row)
