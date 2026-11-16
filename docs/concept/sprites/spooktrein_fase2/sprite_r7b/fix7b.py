# r7b: spookwiel weer leesbaar (Jordi: "De groene wielen moeten nog wat meer gedefinieerd").
# Ring = gesloten ovaal van 1 px in 5 op de plek van de donkere ringlijn uit r4; vlak binnen/buiten egaal 4; naaf 3 (r4 + model 170-175).
import numpy as np; from PIL import Image
src=Image.open('r7.png'); pal=src.getpalette(); o=np.asarray(src).astype(int).copy(); r=o.copy()
Z=np.zeros((64,64),bool); Z[45:57,20:32]=True
def fg(y,x): return 0<=y<64 and 0<=x<64 and o[y,x]>0
def edge(y,x): return any(not fg(y+dy,x+dx) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
log={}
def mark(pt,x,y,v):
    assert Z[y,x]
    if o[y,x]!=v: log.setdefault(pt,[]).append((x,y,int(o[y,x]),int(v))); o[y,x]=v
# vlak egaal 4: groen in rij 47-54, x21-31 (geen buitenrand)
for y in range(47,56):   # rij 56 (onderlijn) niet
    for x in range(21,32):
        if o[y,x] in (2,3,5) and not edge(y,x): mark('vlak 4',x,y,4)
# ovaal op de r4-ringlijn: links x23, boven y48, rechts x29, onder y56 (de onderlijn van r4/r7 op rij 56 blijft); midden (26,52), rx 3,5, ry 4
RING=[(23,50),(23,51),(23,52),(23,53),(23,54),(24,49),(24,55),(25,48),(26,48),(27,48),(28,49),(29,50),(29,51),(29,52),(29,53),(29,54),(28,55),(25,56),(26,56),(27,56)]
for x,y in RING: mark('ring 5',x,y,5)
for x,y in [(25,50),(26,50),(25,51),(26,51)]: mark('naaf 3',x,y,3)
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(pal); im.save('sprite.png',transparency=0)
d=o!=r
with open('telling.txt','w') as f:
    for k in log: s='%s: %d %s'%(k,len(log[k]),log[k]); print(s); f.write(s+'\n')
print('diff totaal',int(d.sum()),'buiten wielzone',int((d&~Z).sum()))
