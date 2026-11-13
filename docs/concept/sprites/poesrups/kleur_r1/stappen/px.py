# px.py x,y x,y ... : modelhelderheid per spritepixel (gem / 15e pct / max) + spritewaarde
import sys,numpy as np
from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poesrups/'
c=np.asarray(Image.open(P+'referenties/model_gekozen.png').convert('RGB')).astype(float); L=c.mean(2)
x0,y0=69,240; s=16.648
R=[l.rstrip('\n') for l in open(P+'kleur_r1/raster.txt')]
for a in sys.argv[1:]:
    x,y=map(int,a.split(','))
    b=L[int(y0+(y-29)*s):int(y0+(y-28)*s), int(x0+(x-5)*s):int(x0+(x-4)*s)]
    print(f'({x},{y}) sprite {R[y][x]}  model gem {b.mean():.0f} p15 {np.percentile(b,15):.0f} max {b.max():.0f}')
