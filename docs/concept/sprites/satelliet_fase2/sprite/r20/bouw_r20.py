# r20 = r19 (rechtercontour) met de linkerkant (x0-24) terug naar r18.
from PIL import Image
import numpy as np
a=Image.open('../r19/sprite.png'); b=Image.open('../r18/sprite.png')
assert a.getpalette()==b.getpalette()
A=np.array(a); B=np.array(b)
A[:, :25]=B[:, :25]
o=Image.fromarray(A,'P'); o.putpalette(a.getpalette()); o.save('sprite.png',transparency=0)
print('verschil met r18:',(A!=B).sum(),'met r19:',(A!=np.array(a)).sum())
