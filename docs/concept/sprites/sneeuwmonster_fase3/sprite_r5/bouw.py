# r5 = r4 met het gezichtsgebied (rij 20-32, x 23-40) terug naar r2 (Jordi: "r4 is gewoon 3 stappen achteruit tov 2").
# Stenen en palet blijven zoals r4 (= uit r3). Geen nieuwe pixels.
from PIL import Image
import numpy as np
r2=Image.open('sprite_r2/sauna_yeti_r2.png'); r4=Image.open('sprite_r4/sauna_yeti_r4.png')
p2=np.array(r2.convert('RGBA')); a4=np.array(r4); pal4=np.array(r4.getpalette()[:48]).reshape(16,3)
out=a4.copy(); n=0
for y in range(20,33):
    for x in range(23,41):
        c=p2[y,x]
        if c[3]==0: idx=0
        else:
            m=np.where((pal4==c[:3]).all(1))[0]; assert len(m), (x,y,c)
            idx=m[0] if m[0]!=0 or len(m)==1 else m[1]
        if out[y,x]!=idx: n+=1
        out[y,x]=idx
im=Image.fromarray(out.astype('uint8'),'P'); im.putpalette(r4.getpalette()); im.save('sprite_r5/sauna_yeti_r5.png',transparency=0)
rgb=np.array(im.convert('RGBA')); d=(rgb!=p2).any(2)
print('gezichtspixels terug naar r2:',n,'| verschil met r2 in totaal:',d.sum())
