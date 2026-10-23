from lib import *
s=Sprite('cuyby/ronde3')
# frame2 = frame1 one row up (dy2=-1)
# 1. verre (linker)oog 1 px smaller: kolom x24 y29-32 -> vacht
s.both(24,29,10,-1,exp=14)   # naast (25,29)=a
for y in (30,31,32): s.both(24,y,3,-1,exp=14)
# 2. zwart oor 1 px hoger
for x in (21,22,23): s.both(x,15,1,-1,exp=0)
s.both(20,16,1,-1,exp=0); s.both(21,16,10,-1,exp=1); s.both(22,16,11,-1,exp=1); s.both(23,16,11,-1,exp=1); s.both(24,16,1,-1,exp=0)
import sys
if 'pad' in sys.argv:
    # C6 linker voetkussen 1 px hoger
    s.both(26,44,12,-1,exp=1); s.both(27,44,13,-1,exp=1)
    s.both(26,45,1,-1,exp=12); s.both(27,45,1,-1,exp=13)
    s.both(26,46,0,-1,exp=1); s.both(27,46,0,-1,exp=1)
d=s.save(sys.argv[1]); print(report(d))
