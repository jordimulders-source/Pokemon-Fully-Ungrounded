"""Ronde 1: bestaand Poliwag-icoon (pal0) pixel voor pixel omkleuren naar pal3 volgens onze front.
Uitvoer: r1_raster.txt (hex per pixel, hand te bewerken)."""
from PIL import Image
import os
D=os.path.dirname(os.path.abspath(__file__))
im=Image.open('graphics/pokemon/poliwag/icon.png')
def kleur(v,x,y,fr):
    yy=y   # frame 2 staat al op frame 1-coordinaten (ly)
    if v==0: return 0
    staart = x>=21 or (x==20 and v in (14,2,1,3,12))
    if staart and v!=15 and yy<=23:
        return {14:14,3:6,1:6,2:5,12:8,8:8,9:14}[v]
    if 13<=x<=16 and 16<=yy<=19 and v in (3,1,15):   # oog
        return {3:3,1:6,15:15}[v]
    if v in (11,10):                                   # mond
        return 7 if yy==18 and v==11 else (15 if v==10 else 8)
    if 8<=x<=15 and 20<=yy<=25 and v in (3,1,2,14):    # buikvenster
        if yy==25 and v==14: return 4
        return {3:6,1:3,2:5,14:8}[v]
    if (yy>=24 and x<=10) or yy>=26:                   # voeten
        return {8:1,9:14,15:15,14:14,2:1,3:1,12:1}.get(v,v)
    if (yy<=19 and x<=13) or (yy<=16 and x<=16):       # gele kopband
        return {12:11,8:10,9:9,15:15,3:11}.get(v,v)
    return {8:14,9:15,12:1,15:15,14:14,2:1,3:1}.get(v,v)
out=[]
for y in range(64):
    fr=1 if y<32 else 2; ly=y if fr==1 else y-31
    out.append(''.join('.' if im.getpixel((x,y))==0 else '%x'%kleur(im.getpixel((x,y)),x,ly,fr) for x in range(32)))
open(os.path.join(D,'r1_raster.txt'),'w').write('\n'.join(out)+'\n')
print('\n'.join('%2d '%i+r for i,r in enumerate(out) if r.strip('.')))
