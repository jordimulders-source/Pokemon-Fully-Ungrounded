# grid.py X0 Y0 X1 Y1 : per spritepixel model p15 (//10) en sprite-index
import sys,numpy as np
from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poedellarve/'
c=np.asarray(Image.open(P+'referenties/model_gekozen.png').convert('RGB')).astype(float); L=c.mean(2)
x0,y0=236,346; s=13.55
R=[l.rstrip('\n') for l in open(P+'kleur_r2/raster.txt')]
X0,Y0,X1,Y1=map(int,sys.argv[1:5]); q=int(sys.argv[5]) if len(sys.argv)>5 else 15
print('     '+''.join(f'{x:>4}' for x in range(X0,X1)))
for y in range(Y0,Y1):
    r=''
    for x in range(X0,X1):
        b=L[int(y0+(y-33)*s):int(y0+(y-32)*s), int(x0+(x-12)*s):int(x0+(x-11)*s)]
        r+=f'{int(np.percentile(b,q))//10:>3}{R[y][x]}'
    print(f'{y:>3}  '+r)
