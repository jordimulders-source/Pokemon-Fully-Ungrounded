# Keurder r4: eilandjes van 1 pixel per kleurindex (4-buren), buiten de ogen.
from PIL import Image; import numpy as np
a=np.array(Image.open('docs/concept/sprites/satelliet_fase3/sprite/r4/sprite.png'))
k=np.array(Image.open('docs/concept/sprites/satelliet_fase3/sprite/r4/kaal.png'))
for c in range(1,16):
    for y in range(64):
        for x in range(64):
            if a[y,x]==c and all(not(0<=x+dx<64 and 0<=y+dy<64) or a[y+dy,x+dx]!=c for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
                print('idx',c,'1px op',(x,y),'kaal',k[y,x])
