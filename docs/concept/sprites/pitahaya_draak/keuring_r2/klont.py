import sys; from PIL import Image; import numpy as np
for f in sys.argv[1:]:
    im=Image.open(f).convert('P') if Image.open(f).mode!='P' else Image.open(f)
    a=np.array(im)[:64,:64]; pal=np.array(im.getpalette()[:768]).reshape(-1,3); L=(pal*[.299,.587,.114]).sum(1)
    used=[i for i in np.unique(a) if i!=0]; dark=min(used,key=lambda i:L[i])
    D=a==dark; k=[(x,y) for y in range(63) for x in range(63) if D[y:y+2,x:x+2].all()]
    print(f.split('/')[-2] if 'graphics' in f else f.split('/')[-1], '2x2 zwart:',len(k), k if 'pitahaya' in f else '')
