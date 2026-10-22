"""dump: png -> f1.txt f2.txt ; load: f1.txt f2.txt -> map/anim_front.png + normal.pal"""
import sys, numpy as np
from PIL import Image
sys.path.insert(0,'.'); 
CH='.123456789ABCDEF'
if sys.argv[1]=='dump':
    a=np.array(Image.open(sys.argv[2]))
    for k in (0,1):
        with open('f%d.txt'%(k+1),'w') as f:
            for y in range(64):
                f.write('|'+''.join(CH[v] if v else ' ' for v in a[k*64+y])+'|\n')
else:
    import build
    fr=[]
    for k in (1,2):
        rows=[l.rstrip('\n') for l in open('f%d.txt'%k)]
        assert len(rows)==64,len(rows)
        g=np.zeros((64,64),np.uint8)
        for y,l in enumerate(rows):
            l=l[1:-1]; assert len(l)==64,(k,y,len(l))
            for x,c in enumerate(l):
                g[y,x]=0 if c==' ' else CH.index(c)
        fr.append(g)
    import os; os.makedirs(sys.argv[2],exist_ok=True)
    build.save(fr,sys.argv[2])
