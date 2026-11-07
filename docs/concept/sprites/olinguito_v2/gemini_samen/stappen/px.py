# px.py raster x,y ... : modelhelderheid per spritepixel (gem/p15/max) + spritewaarde  (naar poedelmot/kleur_r19/stappen/px.py)
import sys,numpy as np
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/olinguito_v2/'
c=np.asarray(Image.open(D+'gemini/ronde2_v4_pose.png').convert('RGB')).astype(float); L=c.mean(2)
S=15.5; X0=184-S*11; Y0=977-S*62
R=[l.rstrip('\n') for l in open(sys.argv[1])]
for a in sys.argv[2:]:
    x,y=map(int,a.split(','))
    b=L[int(Y0+y*S):int(Y0+(y+1)*S), int(X0+x*S):int(X0+(x+1)*S)]
    print(f'({x},{y}) sprite {R[y][x]}  model gem {b.mean():.0f} p15 {np.percentile(b,15):.0f} max {b.max():.0f}')
