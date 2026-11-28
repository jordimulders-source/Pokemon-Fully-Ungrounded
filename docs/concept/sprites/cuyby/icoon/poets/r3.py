"""Cuyby-icoon ronde 3: frame 1 opnieuw uitgelijnd op de rekenregels (r1/r2 hadden de rechterhelft 1 px verschoven),
silhouet ronder. Kop 0,6 rond de hals (31,37): icoon_x = 16,1 + (x-31)*0,6, icoon_y = 23,9 + (y-37)*0,6;
franje 0,55 breed / 0,5 hoog. pal0. python3 r3.py -> poets/r3.png"""
import numpy as np
from PIL import Image
D='docs/concept/sprites/cuyby/icoon/'
# O=15 omlijning/oogzwart, D=14 zwarte vacht en onderste omlijning, G=1 glans/oogonderglans, W=3 creme(wit),
# S=2 schaduw creme, R=7 oranje, Q=6 donker oranje, P=10 roze, L=11 lichtroze
K={'.':0,'O':15,'D':14,'G':1,'W':3,'S':2,'R':7,'Q':6,'P':10,'L':11}
F1=[ #0         1         2         3
     #01234567890123456789012345678901
 (10,"..........OOO..................."),
 (11,".........OGDDO.......OO........."),
 (12,".........ODLDOOOOOOOORLO........"),
 (13,".........ODPDODDWRRRRRRO........"),
 (14,".........OGDDDDDWRRRRRQO........"),
 (15,"........OGDDDDDWWWRRRRQQO......."),
 (16,"........ODGDDDDWWWRRRRQQO......."),
 (17,".......ODGDDDDWWWWSRRRQQQO......"),
 (18,".......OGDOODDWWOOWSRRRQQO......"),
 (19,".......ODOWOOWWOWOOSRRRQQO......"),
 (20,".......ODOOGOWWOOGOSRRRQQO......"),
 (21,".......ODWOOWWWWOOWSRRRQQO......"),
 (22,"........DWWWWLPWWWWSSRRQQD......"),
 (23,"........DWWWWGWWWWWSSRQQD......."),
 (24,"........DSWWWWWWWWWSSRQQD......."),
 (25,"........DSWWWSWWWWSWSRQQD......."),
 (26,"........DSWWWSWWWSWSRQRQD......."),
 (27,"........DDSWWDPDWWSDPDSQDD......"),
 (28,".........DDDDDDDWWDDDD.DD......."),
 (29,"...............DD..............."),
]
def raster(rows):
    a=np.zeros((32,32),np.uint8)
    for y,s in rows:
        assert len(s)==32,(y,len(s))
        for x,c in enumerate(s):
            if c!='.': a[y,x]=K[c]
    return a
def frame2(f1):
    """Stap 7: alles t/m y26 1 px omlaag, rij 27 vervalt, voeten (y28-29) blijven staan."""
    f2=np.zeros_like(f1); f2[11:28]=f1[10:27]; f2[28:]=f1[28:]
    return f2
def bewaar(f1,f2,pad):
    out=np.zeros((64,32),np.uint8); out[:32]=f1; out[32:]=f2
    IP=[int(v) for l in open('graphics/pokemon/icon_palettes/pal0.pal').read().split('\n')[3:19] for v in l.split()[:3]]
    im=Image.fromarray(out,'P'); im.putpalette(IP); im.save(pad)
if __name__=='__main__':
    f1=raster(F1); bewaar(f1,frame2(f1),D+'poets/r3.png')
