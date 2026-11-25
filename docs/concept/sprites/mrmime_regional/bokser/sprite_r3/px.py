# Modelhelderheid per spritecel (43x63-raster): gemiddelde/minimum. Gebruik: px.py y0 y1 x0 x1
import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open('natief.png').convert('L')).astype(float)[5:93,12:72]
s=88/63
y0,y1,x0,x1=map(int,sys.argv[1:5])
print('gem/min x10'); print('    '+''.join('%7d'%i for i in range(x0,x1)))
for j in range(y0,y1):
    r=[]
    for i in range(x0,x1):
        b=a[int(j*s):int(np.ceil((j+1)*s)),int(i*s):int(np.ceil((i+1)*s))]
        r.append('%3d/%3d'%(b.mean()//1,b.min()//1))
    print('%3d '%j+''.join(r))
