# r4 = r3 + reparaties 1-8 uit r3/eindkeuring/EINDKEURING.md (alleen tintwissels, beide frames)
import sys; sys.path.insert(0,'r1'); from pal import *
from PIL import Image
src=Image.open('r3/anim_front.png'); full=np.array(src).astype(int); r3=full.copy()
g=full[:64]; log=[]; fout=[]
def w(nr,pts,van,naar):
    for x,y in pts:
        if g[y,x]!=van: fout.append((nr,(x,y),'verwacht',S[van],'staat',S[g[y,x]])); continue
        g[y,x]=naar; log.append((nr,x,y,van,naar))
# 1 armen
w(1,[(32,y) for y in range(42,49)],5,4)
w(1,[(23,42),(23,43),(22,44),(22,45),(22,46),(21,47),(21,48)],4,5)
w(1,[(23,44),(22,47)],3,4)
# 2 voetstrook
w(2,[(x,54) for x in range(21,25)],5,3)
# 3 staartkrul rechts
w(3,[(49,y) for y in range(35,39)],5,4)
# 4 binnenlijnen romp
w(4,[(34,y) for y in range(43,49)]+[(31,y) for y in range(43,48)],1,2)
# 5 verre oog
w(5,[(17,31)],11,14); w(5,[(17,32)],9,14); w(5,[(17,33)],9,10); w(5,[(18,33)],11,10); w(5,[(18,34)],9,11)
# 6 linkerkoprand
w(6,[(14,30),(15,31),(16,32)],1,2)
# 7 rechterwang
w(7,[(33,32),(32,33),(29,36),(28,37)],7,6)
# 8 nabije oog
w(8,[(27,31)],11,14)
full[64:]=g
np.save('r4/r4.npy',g)
im=Image.fromarray(full.astype('uint8'),'P'); im.putpalette(src.getpalette()); im.save('r4/anim_front.png',transparency=0)
d=(full!=r3); print('alpha-diff met r3:',int(((full>0)!=(r3>0)).sum()),'| pixels gewijzigd (beide frames):',int(d.sum()),'| frame1:',int(d[:64].sum()),'| lijst:',len(log))
gezet={(x,y) for _,x,y,_,_ in log}; buiten=[(x,y) for y,x in zip(*np.where(d[:64])) if (x,y) not in gezet]; print('diff buiten lijst:',len(buiten))
from collections import Counter; print(dict(Counter(n for n,*_ in log)))
print('niet toegepast (van klopt niet):',fout)
