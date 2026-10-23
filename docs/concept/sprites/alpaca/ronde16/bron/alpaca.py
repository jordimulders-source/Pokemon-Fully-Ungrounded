from lib import *
import sys
mode=sys.argv[2] if len(sys.argv)>2 else 'A'
s=Sprite('alpaca/ronde15')
# verre vuist (x25-30, y45-49) een tint donkerder; manchet en omlijning blijven. Lijf gelijk in beide frames.
m={7:8,8:9} if mode=='A' else {7:8,8:9,9:10}
for y in range(45,50):
    for x in range(25,31):
        o=int(s.old[y,x])
        if mode=='B' and y==49: continue
        if o in m: s.both(x,y,m[o],0)
if 'rug' in sys.argv:
    # rugrand: schoft 1 px omhoog bij x33-34
    # schoft: rugrand x32-34 1 px omhoog, sluit aan op de hals (geen deukje)
    for x in (32,33,34): s.both(x,27,6,0,exp=0); s.both(x,28,2,0,exp=6)
d=s.save(sys.argv[1]); print(report(d))
