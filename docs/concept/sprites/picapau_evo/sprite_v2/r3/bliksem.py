# 5 bliksem bovenste tak: wigvorm uit het model (vulling rij 33 x2-3, rij 34 x3-4, rij 35 x3-5; buitenlijn eromheen), licht C bovenaan zoals r2.
# 8 overgang bliksem->koord: (11,48),(12,48) en (10,49) weg; koord loopt (9,48)->(9,49)->(9,50)->(10,51).
import numpy as np
def run(o):
    n=o.copy()
    for x,y,v in [(1,33,1),(2,33,5),(4,34,12),(5,34,1),(2,35,1),(3,35,5),(5,35,12),(6,35,1),
                  (11,48,0),(12,48,0),(10,49,0)]: n[y,x]=v
    return n
if __name__=='__main__':
    o=np.load('_tmp/s4.npy'); n=run(o); np.save('_tmp/s5.npy',n); print('bliksem px',(n!=o).sum())
