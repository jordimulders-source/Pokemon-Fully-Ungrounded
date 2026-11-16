# metingen: zwart, vulvlakjes < 3 px, dambord, buitenlijn-kanten
import sys,numpy as np;from PIL import Image;from scipy import ndimage as nd
for f in sys.argv[1:]:
    o=np.asarray(Image.open(f)).astype(int); m=o>0
    pad=np.pad(m,1); rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
    zw=(o==1); kl=0
    for v in (3,4,5,9,10,11):
        lab,n=nd.label(o==v); kl+=sum(1 for i in range(1,n+1) if (lab==i).sum()<3)
    db=0
    for y in range(63):
        for x in range(63):
            q=o[y:y+2,x:x+2]
            if (q>0).all() and q[0,0]==q[1,1] and q[0,1]==q[1,0] and q[0,0]!=q[0,1]: db+=1
    print(f, 'px',m.sum(),'zwart %.1f%%'%(100*zw.sum()/m.sum()),'zwart binnen %.1f%%'%(100*(zw&~rand).sum()/m.sum()),'vulvlakjes<3',kl,'dambord',db,
          'tinten',{v:int((o==v).sum()) for v in range(1,15)})
