"""Cuyby-icoon ronde 2 (oogonderglans G i.p.v. Q): frame 1 met de hand gepoetst op de onderlaag onderdelen/a1.png (pal0),
pixel voor pixel volgens de rekenregels (kop 0,6 rond de hals (31,37), onderlijf 0,5; zie NOTITIES.md).
python3 r1.py -> poets/r2.png (32x64; frame 2 nog leeg)"""
import numpy as np, sys
from PIL import Image
D='docs/concept/sprites/cuyby/icoon/'
# O=15 omlijning/oogzwart, D=14 zwarte vacht (en onderste omlijning), G=1 glans zwarte vacht, W=3 wit/creme,
# S=2 schaduw creme, R=7 oranje, Q=6 donker oranje, P=10 roze, L=11 lichtroze
K={'.':0,'O':15,'D':14,'G':1,'W':3,'S':2,'R':7,'Q':6,'P':10,'L':11}
X0=7
F1=[ # x 7..25
 (10,"...OOO..............."),
 (11,"..OGDDO.......OO....."),
 (12,"..ODLDOOOOOOOOLRO...."),
 (13,"..ODPDODDWRRRRRRO...."),
 (14,"..OGDDDDDWRRRRRRO...."),
 (15,"..OGDDDDWWWRRRRQO...."),
 (16,".OGDDDDDWWWRRRRQQO..."),
 (17,".OGDDDDDWWWSRRRQQO..."),
 (18,"OGDDOODDWWOOWSRRQQQO."),
 (19,"ODDOWOOWWOWOOSRRRQQO."),
 (20,"ODDOOGOWWOOGOSRRRQQO."),
 (21,"ODDWOOWWWWOOWSRRQQQO."),
 (22,"ODWWWWWLPWWWWSSRQQQO."),
 (23,".DWWWWWGWWWWWSSRQQD.."),
 (24,"..DWWWWWWWWWSSRQQD..."),
 (25,".DSWWWWWWWWWSSRQQQD.."),
 (26,".DSWWWSWWWSWSSRQQQD.."),
 (27,".DSDWWDWWWDWSDQQDQD.."),
 (28,"..DDSDPDWWDPDDQD.D..."),
 (29,"........DD..........."),
]
def raster(rows):
    a=np.zeros((32,32),np.uint8)
    for y,s in rows:
        for i,c in enumerate(s):
            if c!='.': a[y,X0+i]=K[c]
    return a
def frame2(f1):
    """Stap 7: alles t/m y26 1 px omlaag, rij 27 vervalt, voeten (y28-29) blijven staan."""
    f2=np.zeros_like(f1); f2[11:28]=f1[10:27]; f2[28:]=f1[28:]
    return f2

if __name__=='__main__':
    f1=raster(F1); out=np.zeros((64,32),np.uint8); out[:32]=f1; out[32:]=frame2(f1)
    IP=[int(v) for l in open('graphics/pokemon/icon_palettes/pal0.pal').read().split('\n')[3:19] for v in l.split()[:3]]
    im=Image.fromarray(out,'P'); im.putpalette(IP); im.save(D+'poets/r2.png')
