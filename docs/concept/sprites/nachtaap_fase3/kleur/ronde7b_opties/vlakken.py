# grootste egale blok (rechthoek, één tint) midden in de romp x26-42 r32-45 en grootste vlak gemeten als schijf
import sys
from PIL import Image
for f in sys.argv[1:]:
    a=Image.open(f).load(); best=(0,)
    for x0 in range(26,43):
        for y0 in range(32,46):
            v=a[x0,y0]
            if not 3<=v<=5: continue
            for w in range(1,18):
                for h in range(1,15):
                    if x0+w>43 or y0+h>46: break
                    if all(a[x,y]==v for x in range(x0,x0+w) for y in range(y0,y0+h)):
                        if w*h>best[0]: best=(w*h,v,x0,y0,w,h)
    print(f,'grootste egale rechthoek: %d px tint %d bij x%d r%d (%dx%d)'%best)
