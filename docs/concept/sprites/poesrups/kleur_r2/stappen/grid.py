# grid.py X0 Y0 X1 Y1 : per spritepixel model p15 (//10) en sprite-index
import sys,numpy as np
from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poesrups/'
c=np.asarray(Image.open(P+'referenties/model_gekozen.png').convert('RGB')).astype(float); L=c.mean(2)
x0,y0=69,240; s=16.648
R=[l.rstrip('\n') for l in open(P+'kleur_r2/raster.txt')]
X0,Y0,X1,Y1=map(int,sys.argv[1:5]); q=int(sys.argv[5]) if len(sys.argv)>5 else 15
print('     '+''.join(f'{x:>4}' for x in range(X0,X1)))
for y in range(Y0,Y1):
    r=''
    for x in range(X0,X1):
        b=L[int(y0+(y-29)*s):int(y0+(y-28)*s), int(x0+(x-5)*s):int(x0+(x-4)*s)]
        r+=f'{int(np.percentile(b,q))//10:>3}{R[y][x]}'
    print(f'{y:>3}  '+r)
