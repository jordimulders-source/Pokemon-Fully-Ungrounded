import numpy as np
from PIL import Image
a=np.array(Image.open('sprite.png'))
KL={0:'t',1:'d',2:'d',3:'d',4:'l',5:'l',6:'p',7:'p',8:'p',9:'o',10:'o',11:'w',12:'w',13:'w',14:'w',15:'w'}
los=[]
for y in range(1,63):
    for x in range(1,63):
        c=a[y,x]
        if c==0: continue
        nb=[a[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if dy or dx]
        if not any(KL[n]==KL[c] for n in nb): los.append((x,y-13,int(c)))
print('losse pixels (x, rasterrij, kleur):',los)
# zwart (1) volledig binnen de vorm (geen transparante 4-buur)
binnen=[(x,y-13) for y in range(1,63) for x in range(1,63) if a[y,x]==1 and all(a[y+dy,x+dx]!=0 for dy,dx in((1,0),(-1,0),(0,1),(0,-1)))]
print('zwarte pixels zonder transparante buur:',len(binnen),binnen)
for nm,(x0,y0,x1,y1) in {'voor':(13,34,16,38),'links':(18,17,19,18),'rechts':(51,25,52,26)}.items():
    blk=a[y0+13:y1+14,x0:x1+1]; print('oog',nm,'binnen ring:',sorted(set(blk.ravel().tolist())))
