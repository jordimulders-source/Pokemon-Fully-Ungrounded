# rgb.py X0 Y0 X1 Y1 : gemiddelde modelkleur (alleen voorgrond) per spritepixel als hex RGB//16 + lum
import sys,numpy as np
from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poedellarve/'
c=np.asarray(Image.open(P+'referenties/model_gekozen.png').convert('RGB')).astype(float)
g=(c[...,1]>c[...,0]+40)&(c[...,0]<120)
x0,y0=236,346; s=13.55
X0,Y0,X1,Y1=map(int,sys.argv[1:5])
print('    '+''.join(f'{x:>5}' for x in range(X0,X1)))
for y in range(Y0,Y1):
    r=f'{y:>3} '
    for x in range(X0,X1):
        sl=(slice(int(y0+(y-33)*s),int(y0+(y-32)*s)),slice(int(x0+(x-12)*s),int(x0+(x-11)*s)))
        b=c[sl]; f=~g[sl]
        r+='    .' if f.mean()<.3 else f'{int(b[f].mean(1).mean()) if False else int(b[f].mean()):>5}'
    print(r)
