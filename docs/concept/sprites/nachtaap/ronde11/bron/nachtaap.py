from lib import *
import sys
s=Sprite('nachtaap/ronde10')
H=1  # kop zakt 1 px in frame 2
# 1. mondje 1 px naar links
s.both(23,38,13,H,exp=7); s.both(25,38,7,H,exp=13)
# 2. verre (linker)oog 6 breed: iriskolom x19 eruit, rechterdeel 1 px naar links, x21 wordt masker (D)
for y in range(29,36):
    o20=int(s.old[y,20]); o21=int(s.old[y,21])
    s.both(19,y,o20,H); s.both(20,y,o21,H); s.both(21,y,6,H)
# 3. elleboog: knik naar buiten op y44-45, pols 1 px terug op y47 (arm gelijk in beide frames)
if 'noelbow' not in sys.argv:
    s.both(15,44,2,0,exp=0)                      # bovenkant knik: omlijning
    s.both(15,45,2,0,exp=0); s.both(16,45,4,0,exp=2)
    s.both(15,47,0,0,exp=2); s.both(16,47,2,0,exp=4)
d=s.save(sys.argv[1]); print(report(d))
