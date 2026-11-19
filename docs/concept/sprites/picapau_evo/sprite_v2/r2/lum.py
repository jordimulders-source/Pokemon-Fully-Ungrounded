# Per spritecel: zwartfractie (lum<60), witfractie en gemiddelde lum van de overige modelpixels. python3 lum.py x0 y0 x1 y1
import sys; import numpy as np; from PIL import Image
x0,y0,x1,y1=map(int,sys.argv[1:5])
a=np.asarray(Image.open('../../gemini/r9_prompt_v6.png').convert('RGB')).astype(int); L=a.mean(2); S=15.36; OY,OX=5.12,4*5.12
print('    '+''.join('%-9d'%x for x in range(x0,x1)))
for y in range(y0,y1):
    r=[]
    for x in range(x0,x1):
        b=L[int(OY+y*S):int(OY+(y+1)*S),int(OX+x*S):int(OX+(x+1)*S)].ravel()
        z=(b<60).mean(); w=(b>235).mean(); m=b[(b>=60)&(b<=235)]
        r.append('%2d/%2d/%3d'%(z*99,w*99,m.mean() if len(m) else 0))
    print('%2d  '%y+' '.join(r))
