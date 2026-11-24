# k11 = k10 zonder putjes in wandstenen < 6 px (geen ring/"@"); alleen bergwand
import sys, numpy as np
sys.path.insert(0,'../k1')
from gereedschap import *
a10,pal=laad('../k10/tempel.png'); a=a10.copy()
PUTJES=[(50,23),(51,23),(50,24),   # boven, steen 4 hoog
        (50,36),(51,36),(50,37),   # midden links, steen 4 breed
        (57,44),(58,44),(57,45),   # onder rechtsboven, steen 5 breed
        (50,53),(51,53),(50,54)]   # onder links, steen 4 breed
for x,y in PUTJES:
    assert a10[y,x]==14; a[y,x]=15
bewaar(a,pal,'tempel.png')
