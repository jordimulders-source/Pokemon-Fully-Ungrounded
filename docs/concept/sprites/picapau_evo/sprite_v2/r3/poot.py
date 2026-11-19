# 7 rechterpoot: zelfde tinten als de linkerpoot (h aan de randen, G in het midden, teenlijn zwart zoals links x21); geen g meer.
import numpy as np
P=[(27,48,11),(28,48,10),(29,48,11),(26,49,11),(27,49,10),(28,49,10),(29,49,11),(26,50,11),(27,50,10),(28,50,1),(29,50,11),(27,51,10),(29,51,11)]
def run(o):
    n=o.copy()
    for x,y,v in P: n[y,x]=v
    return n
if __name__=='__main__':
    o=np.load('_tmp/s6.npy'); n=run(o); np.save('_tmp/s7.npy',n); print('poot px',(n!=o).sum())
