# gen3.py: Gen 3-Starmie (anim_front_gba frame 1) in punten verdelen op hoek vanaf de kern.
# Set A = punten op 96/28/-39/-118/176 graden (in Gen 3 de donkere ACHTERSTE ster),
# set B = 61/-2/-81/-151/140 graden (in Gen 3 de lichte VOORSTE ster).
# Model r3 heeft zijn voorste ster in de richtingen van set A en zijn achterste koekpunten in die van set B.
import numpy as np; from PIL import Image
G3='../../../../../graphics/pokemon/starmie/anim_front_gba.png'
def laad():
    im=Image.open(G3); o=np.asarray(im)[:64].astype(int)
    pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    return o,pal
C=(31.5,30.0)   # kern (midden van het juweel)
TIPS={'top':(28,7),'r':(56,17),'br':(54,47),'bl':(18,55),'l':(5,28),        # set A
      'tr':(44,7),'rl':(59,31),'b':(36,57),'ll':(7,44),'tl':(11,13)}         # set B
SETB=('tr','rl','b','ll','tl')
def hoek(x,y): return np.degrees(np.arctan2(C[1]-y,x-C[0]))
def punt_van(x,y):
    h=hoek(x,y); best=None
    for n,(tx,ty) in TIPS.items():
        d=abs((hoek(tx,ty)-h+180)%360-180)
        if best is None or d<best[0]: best=(d,n)
    return best[1]
