# stap 1: beide linker voorpoten als geheel 3 px naar rechts (kopiëren, niet tekenen)
import sys; sys.path.insert(0,'sprite_r14')
from lib import *
src=Image.open('sprite_r13/vlieg_r13.png'); a=src.load()
S=3
L=set()
for y in range(41,64):
    for x in range(0,27):
        if a[x,y]: L.add((x,y))
for x in range(16,22): L.add((x,40))
for x in range(20,24): L.add((x,39))
im=src.copy(); b=im.load()
for (x,y) in L: b[x,y]=0
for (x,y) in L: b[x+S,y]=a[x,y]
im.save('sprite_r14/_stap1.png',transparency=0)
