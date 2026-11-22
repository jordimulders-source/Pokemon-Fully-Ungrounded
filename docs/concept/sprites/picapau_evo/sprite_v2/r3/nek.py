# 6 achterhoofd: buitenlijn volgt het model (lijnmidden x 28,0 op rij 11 -> 28,8 vanaf rij 13,5 -> 29,1 op rij 20):
# rijen 11-13 zwart op x28, vanaf rij 14 (modelvulling tot x 28,69) wordt x28 bruin m en ligt de lijn op x29.
import numpy as np
def run(o):
    n=o.copy()
    for y in range(14,20): n[y,28]=3; n[y,29]=1
    return n
if __name__=='__main__':
    o=np.load('_tmp/s5.npy'); n=run(o); np.save('_tmp/s6.npy',n); print('nek px',(n!=o).sum())
