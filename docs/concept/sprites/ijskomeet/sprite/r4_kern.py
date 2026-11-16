# r4 stap 3: kleine opruiming lijf + grotere kern (v -> n -> j, gloed naar beneden) + spiraalboog
from gio import from_txt, to_txt, CH
import numpy as np, math
o=from_txt('r4_lijf.txt'); C={c:i for i,c in enumerate(CH)}
for (x,y,c) in [(9,43,'M'),(8,45,'L'),(6,45,'L'),(23,45,'M')]: o[y,x]=C[c]
cx,cy=25.4,35.0
for (x,y) in [(26,32),(27,32),(28,33),(29,34),(29,35),(28,36)]: o[y,x]=C['n']
for y in range(28,39):
    for x in range(20,33):
        if CH[o[y,x]] not in 'ijnv' if o[y,x]>=0 else True: continue
        dx=(x+0.5-cx)/3.3; dy=(y+0.5-cy)/(3.0 if y+0.5<cy else 3.5)
        d=math.hypot(dx,dy)
        if d<=1.0: o[y,x]=C['v']
        elif d<=(1.45 if y+0.5<cy else 1.7): o[y,x]=C['n']
        elif d<=2.0 and CH[o[y,x]]=='i': o[y,x]=C['j']
# spiraalboog (1 px v, met n ertussen) rechtsboven om de vlek
for y in range(28,39):
    for x in range(20,33):
        if o[y,x]<0 or CH[o[y,x]] not in 'nj': continue
        dx=(x+0.5-cx)/3.3; dy=(y+0.5-cy)/3.0
        d=math.hypot(dx,dy); a=math.degrees(math.atan2(dy,dx))
        if 1.38<=d<=1.7 and -75<=a<=35: o[y,x]=C['v']
to_txt(o,'r4_kern.txt')
for y in range(27,40): print('%2d '%y+''.join('.' if v<0 else CH[v] for v in o[y,16:40]))
print('v-pixels kern', int(sum(1 for y in range(28,39) for x in range(20,33) if o[y,x]==C['v'])))
