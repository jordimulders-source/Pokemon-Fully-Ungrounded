from lib import *
import sys
s=Sprite('cuyby_evo/ronde4')
# inkepingen tussen de lokpunten 1 rij dieper (onderkant identiek in beide frames)
for x in (12,28,36):
    s.both(x,49,0,0,exp=1)
    s.both(x-1,49,1,0); s.both(x+1,49,1,0)
d=s.save(sys.argv[1]); print(report(d))
