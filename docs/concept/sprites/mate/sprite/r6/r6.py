# Ronde 6: alleen schaduw kop (keurder r5), gemeten op de modelmediaan per spritepixel. Basis r5.
import sys; sys.path.insert(0,'r4')
import numpy as np; from PIL import Image
im=Image.open('r5/mate.png'); PAL=im.getpalette(); r5=np.asarray(im).astype(int); a=r5.copy()
# 1. sikkel rechtsboven (model ±48-62 = b): binnenrand gebogen langs de omtrek, loopt over in de strook x46-49
BINNEN={31:38,32:38,33:38,34:38,35:39,36:39,37:40,38:40,39:41,40:42,41:44}
for y,x0 in BINNEN.items():
    for x in range(x0,47):
        if a[y,x]==4: a[y,x]=3
# 2. licht alleen linksboven (model d tot x25 bovenaan, smaller naar het oog toe), tussen de ogen middentint
RECHTS={31:25,32:25,33:24,34:24,35:24,36:23,37:21,38:21,39:21}
for y in range(31,41):
    for x in range(22,32):
        if a[y,x]==5 and (y==40 and x>24 or y<40 and x>RECHTS[y]): a[y,x]=4
# kruin tussen hoornlijnen (42-43,31) blijft c: sluit aan op c erboven (anders vlakje van 2 px)
a[31,42]=a[31,43]=4
# 3. rechtervoet bovenste rij b (model ±57-61); (35,60) model b
for x in range(35,41): a[59,x]=3
a[60,35]=3
p=Image.fromarray(a.astype('uint8'),'P'); p.putpalette(PAL); p.save('r6/mate.png',transparency=0); np.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/f952c4af-e06e-5b56-87d5-86ed60c9233c/scratchpad/r6.npy',a)
d=a!=r5; print('diff t.o.v. r5',int(d.sum()))
zones=[(38,31,46,41),(22,31,31,40),(35,59,40,60)]
print('buiten de zones',[(x,y) for y,x in zip(*np.where(d)) if not any(x0<=x<=x1 and y0<=y<=y1 for x0,y0,x1,y1 in zones)])
for z in zones: x0,y0,x1,y1=z; print(z,int(d[y0:y1+1,x0:x1+1].sum()))
