import sys; sys.path.insert(0,'keuring_r2'); from stats import stats
import numpy as np
for f in ['sprite_r2/pitahaya_r2.png','sprite_r2/pitahaya_r1.png']:
    a,pal,small,edge,dark=stats(f)
    face=lambda y,x: 18<=x<=36 and 22<=y<=34
    from collections import Counter
    c=Counter(); lst=[]
    for idx,comp in small:
        if idx in (3,4,5,6,9,10,11):
            inface=all(face(y,x) for y,x in comp)
            c[(idx,'face' if inface else 'rest')]+=1
            if not inface: lst.append((idx,[(x,y) for y,x in comp]))
    print(sorted(c.items()))
    if 'r2' in f:
        for i,l in lst: print(i,l)
