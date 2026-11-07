# px.py x,y x,y ... : modelhelderheid per spritepixel (gem / 15e pct / max) + spritewaarde
import sys,numpy as np
from PIL import Image
P='/home/user/pokemon-fully-ungrounded/docs/concept/sprites/poedelmot/'
c=np.asarray(Image.open(P+'referenties/samengesteld.png').convert('RGB')).astype(float); L=c.mean(2)
x0,y0=139,150; s=(854-139)/62
R=[l.rstrip('\n') for l in open(P+'kleur_r19/raster.txt')]
for a in sys.argv[1:]:
    x,y=map(int,a.split(','))
    b=L[int(y0+(y-17)*s):int(y0+(y-16)*s), int(x0+(x-1)*s):int(x0+x*s)]
    print(f'({x},{y}) sprite {R[y][x]}  model gem {b.mean():.0f} p15 {np.percentile(b,15):.0f} max {b.max():.0f}')
