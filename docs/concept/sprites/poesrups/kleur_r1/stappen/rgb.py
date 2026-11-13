# rgb.py X0 Y0 X1 Y1 : gemiddelde modelkleur (alleen voorgrond) per spritepixel als hex RGB//16 + lum
import sys,numpy as np
from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poesrups/'
c=np.asarray(Image.open(P+'referenties/model_gekozen.png').convert('RGB')).astype(float)
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from bg import masker; g=masker()
x0,y0=69,240; s=16.648
X0,Y0,X1,Y1=map(int,sys.argv[1:5])
print('    '+''.join(f'{x:>5}' for x in range(X0,X1)))
for y in range(Y0,Y1):
    r=f'{y:>3} '
    for x in range(X0,X1):
        sl=(slice(int(y0+(y-29)*s),int(y0+(y-28)*s)),slice(int(x0+(x-5)*s),int(x0+(x-4)*s)))
        b=c[sl]; f=~g[sl]
        r+='    .' if f.mean()<.3 else f'{int(b[f].mean(1).mean()) if False else int(b[f].mean()):>5}'
    print(r)
