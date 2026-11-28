"""Ronde 3: frame 1 met de hand bijgewerkt (buikvenster + spiraal), frame 2 automatisch afgeleid:
elke pixel van het originele frame 2 krijgt de nieuwe kleur van dezelfde pixel in frame 1
(zelfde verschuiving als in het origineel; kop/lijf 1 px hoger, staart 1 px links)."""
from PIL import Image
O=Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/poliwag/icon.png')
o=[[O.getpixel((x,y)) for x in range(32)] for y in range(64)]
rows=[list(r) for r in open('r2_raster.txt').read().split('\n')[:64]]
def put(y,x,s):
    for i,c in enumerate(s): rows[y][x+i]=c
put(21,7,'f3336665eeeeef')
put(22,7,'f36888865eeeef')
put(23,8,'f68668655eeefff')
put(23,8,'f6866865eeeefff')
put(24,7,'f16868865eeff')
put(24,7,'f16868865eeff')
put(25,7,'fe144444eef')
f1=[r[:] for r in rows[:32]]
# frame 2
voorkeur=[(0,1),(1,1),(-1,1),(0,0),(1,0),(-1,0),(0,2),(1,2)]
for y in range(32):
    for x in range(32):
        v=o[32+y][x]
        if v==0: rows[32+y][x]='.'; continue
        for dx,dy in voorkeur:
            X,Y=x+dx,y+dy
            if 0<=X<32 and 0<=Y<32 and o[Y][X]==v:
                rows[32+y][x]=f1[Y][X]; break
        else: rows[32+y][x]='?'
# kristal ook in frame 2 (kop staat daar 1 px hoger)
put(43,16,'f'); put(44,15,'f3f'); put(45,15,'f8f')
open('r3_raster.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
for i in list(range(11,29))+list(range(43,61)): print('%2d '%i+''.join(rows[i]))
