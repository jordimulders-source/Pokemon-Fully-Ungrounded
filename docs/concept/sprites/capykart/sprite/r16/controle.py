import numpy as np, json
from PIL import Image
exec(open('r16.py').read().split("# ---- zones uit r15b")[0].split("G=src.copy()")[0])
a=np.array(Image.open('capykart.png')).astype(int); b=np.array(Image.open('../r15b/capykart_creme.png')).astype(int)
FACE=set([(x,y) for x in range(28,32) for y in range(16,22)]+[(x,y) for x in range(17,24) for y in range(30,34)]
         +[(21,15),(22,15),(23,15),(21,16),(22,16),(23,16),(15,22),(16,22),(18,28),(19,28)]+[(x,30) for x in range(25,29)])
def toren(x,y): return x>=44 and y<=32 and not (x<=46 and y>=29)
hout=np.load('hout_mask.npy'); kop=np.load('kop_mask.npy')
bm=b.copy(); bm[(bm==3)]=13   # vachttint 3 is samengevoegd met D
d=(a!=bm)
zones={'silhouet (transparant anders)':int(((a==0)!=(b==0)).sum()),
 'gezicht (na 3->D)':int(sum(d[y,x] for x,y in FACE)),
 'toren (index anders)':int(sum(d[y,x] for y in range(64) for x in range(64) if toren(x,y))),
 'toren: zwart/transparant anders':int(sum(((a[y,x] in (0,1))!=(b[y,x] in (0,1))) for y in range(64) for x in range(64) if toren(x,y))),
 'hout':int(d[hout].sum()),'kop/nek':int((d&kop&~hout).sum()),
 'rest':int(sum(d[y,x] for y in range(64) for x in range(64) if not toren(x,y) and not hout[y,x] and not kop[y,x] and (x,y) not in FACE)),
 'kleuren':len(set(a.flatten()))}
print(json.dumps(zones,ensure_ascii=False))
rest=[(x,y,int(b[y,x]),int(a[y,x])) for y in range(64) for x in range(64) if d[y,x] and not toren(x,y) and not hout[y,x] and not kop[y,x] and (x,y) not in FACE]
print('rest:',rest)
