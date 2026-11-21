# afwijking per zone t.o.v. de kale reductie
import numpy as np; from collections import Counter
K=np.loadtxt('kaal.txt',dtype=int); o=np.loadtxt('vlieg_r1.txt',dtype=int); z=np.load('zone.npy')
d=(K!=o); c=Counter(z[d]); print('totaal afwijkend',d.sum(),'van',(o>0).sum()|(K>0).sum()); print(dict(c))
