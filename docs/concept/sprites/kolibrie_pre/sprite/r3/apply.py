# r3 = r2 + MOET-lijst uit r2/KEURING.md (per script, door Claude)
from PIL import Image
M=[(20,29,14),(21,29,14),(20,30,1),(21,30,1),(22,30,14),(23,30,14),(22,31,1),(24,31,14),(25,31,14),
   (33,25,1),(21,43,2),(24,48,1),
   (32,39,2),(32,42,2),(32,44,2),(31,36,3),
   (47,45,4),(48,45,4),(49,45,4),(50,45,4),(47,46,10),(48,46,10),(49,46,8),(50,46,8),(49,47,8)]
import sys
for src,dst in [('r2/hummlet.png','r3/hummlet.png'),('r2/hummlet_oogB.png','r3/hummlet_oogB.png')]:
    im=Image.open(src); px=im.load(); n=0
    for x,y,v in M:
        if px[x,y]!=v: px[x,y]=v; n+=1
    im.save(dst,transparency=0); print(dst,n,'px')
