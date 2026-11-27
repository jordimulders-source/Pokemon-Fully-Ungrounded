# r5 = r4 met 8-verbonden buitenlijn: zwarte binnenhoekjes van trapjes (zwart naast zwarte rand,
# zelf niet aan de achtergrond) krijgen de vulling van hun binnenbuur. Silhouet gelijk.
import os; from PIL import Image; import numpy as np; from collections import Counter
d=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(d,'../r4/zandloper_fase2_r4.png')); a=np.array(im); b=a.copy()
op=a>0; p=np.pad(op,1); rand=op&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
zw=a==1; zr=np.pad(zw&rand,1)
dub=op&~rand&zw&(zr[:-2,1:-1]|zr[2:,1:-1]|zr[1:-1,:-2]|zr[1:-1,2:])
LIJN={0,1,2,7}
n=0
for y,x in zip(*np.where(dub)):
    if 21<=y<=27 and 22<=x<=37: continue   # ogen blijven
    c=Counter(int(a[y+dy,x+dx]) for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and int(a[y+dy,x+dx]) not in LIJN)
    if not c: continue
    b[y,x]=c.most_common(1)[0][0]; n+=1
o=Image.fromarray(b,'P'); o.putpalette(im.getpalette()); o.save(os.path.join(d,'zandloper_fase2_r5.png'),transparency=0)
print('gewijzigd',n,'alpha-diff',int(((a>0)!=(b>0)).sum()))
