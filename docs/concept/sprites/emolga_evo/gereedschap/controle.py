# controle.py: technische checks op een 64x64 klassen/indexraster.
import numpy as np
from gemeen import label
def enkel(o):
    # vulpixels zonder 8-buur van dezelfde index (losse tintpixels), en clusters < 3 px per index
    los=[];klein=[]
    for v in range(2,16):
        lab,n=label(o==v)
        for i in range(1,n+1):
            m=lab==i; k=m.sum()
            if k==1: y,x=np.argwhere(m)[0]; los.append((int(x),int(y),v))
            elif k<3: klein.append([(int(x),int(y),v) for y,x in np.argwhere(m)])
    return los,klein
def rapport(o,naam):
    from opschoon import losse_zwart
    los,klein=enkel(o)
    print(naam,'| kleuren:',sorted(set(o.ravel().tolist())),'n=',len(set(o.ravel().tolist())),'| fig px',(o>0).sum(),
          '| zwart %.1f%%'%(100*(o==1).sum()/(o>0).sum()))
    print('  losse zwart:',losse_zwart(o)); print('  losse tintpixels:',los); print('  clusters 2px:',klein)
