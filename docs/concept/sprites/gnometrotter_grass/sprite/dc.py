# dc.py: Dragonfly Cave-omlijningsronde (gids r. 80-170, 340-470; maatstaf Gnomad r10-r11) op red.png -> gnometrotter_grass.png
# 1. buitenlijn: geen zwart en outline base om en om (losse enkele pixel op een rand neemt de kleur van zijn twee randburen over)
# 2. outline highlight: op de meest belichte buitenrand (normaal recht naar linksboven) van muts, rugkam en de ronde roze delen
#    komt de schaduwtint van het vlak in de lijn (gids: "outline highlights" binnen de lijn), max 3 px per onderdeel
# 3. binnenlijnen nooit zwart behalve de vaste zwarte boog rond de ronde delen (al in maak.py)
import numpy as np
from gemeen import *
o=lees('red.png'); zone=np.load('zone_af.npy'); fg=o>0
OUT=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg)):
    if any(not(0<=Y+dy<64 and 0<=X+dx<64) or not fg[Y+dy,X+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): OUT[Y,X]=True
gew=[]
for _ in range(2):
    for Y,X in zip(*np.where(OUT)):
        k=o[Y,X]; b=BASIS[zone[Y,X]]
        if k not in (1,b): continue
        nb=[o[Y+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=Y+dy<64 and 0<=X+dx<64 and OUT[Y+dy,X+dx] and zone[Y+dy,X+dx]==zone[Y,X]]
        ander=1 if k==b else b
        if len(nb)>=2 and nb.count(k)==0 and nb.count(ander)>=2:
            o[Y,X]=ander; gew.append((X,Y,'om en om'))
LICHT=np.array([-0.6,-0.8])
def normaal(Y,X):
    v=np.zeros(2)
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if (dy or dx) and (not(0<=Y+dy<64 and 0<=X+dx<64) or not fg[Y+dy,X+dx]): v+=(dx,dy)
    n=np.linalg.norm(v); return v/n if n else v
HL={1:13,5:7,9:7,19:7}
for zz,t in HL.items():
    kand=sorted(((normaal(Y,X)@LICHT,Y,X) for Y,X in zip(*np.where(OUT&(zone==zz))) if o[Y,X]==BASIS[zz]),reverse=True)
    for s,Y,X in kand[:3]:
        if s>0.9: o[Y,X]=t; gew.append((X,Y,'outline highlight'))
opslaan(o,'gnometrotter_grass.png')
print(len(gew),'pixels:',gew)
